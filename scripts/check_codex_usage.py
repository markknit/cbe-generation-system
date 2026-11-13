#!/usr/bin/env python3
"""Read Codex weekly allowance and latch a clean-stop request; no model turns.

Exit 0: above threshold and no pending pause; 10: clean pause requested;
20: usage unavailable/invalid. This is an explicit workflow checkpoint, not
an idle-time daemon. The agent performs /update at the clean stopping point.
"""
import argparse
from datetime import datetime, timezone
import json
import math
import os
from pathlib import Path
import selectors
import shutil
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]


def weekly_meter(result, config):
    buckets = result.get('rateLimitsByLimitId') or {}
    bucket = buckets.get(config['limit_id'])
    if bucket is None:
        fallback = result.get('rateLimits') or {}
        if fallback.get('limitId') not in (None, config['limit_id']):
            raise ValueError('Requested usage bucket unavailable')
        bucket = fallback
    windows = [bucket.get(k) for k in ('primary', 'secondary')]
    weekly = [w for w in windows if w and w.get('windowDurationMins') == config['weekly_window_minutes']]
    if not weekly:
        raise ValueError('No weekly allowance returned; do not infer it from another window')
    used = []
    for w in weekly:
        value = w.get('usedPercent')
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not 0 <= value <= 100:
            raise ValueError('Invalid weekly usage percentage')
        used.append(value)
    index = max(range(len(used)), key=used.__getitem__)
    return {'limit_id': config['limit_id'], 'remaining_percent': 100 - used[index],
            'used_percent': used[index], 'resets_at': weekly[index].get('resetsAt'),
            'window_minutes': config['weekly_window_minutes']}


def codex_binary():
    binary = shutil.which('codex')
    if not binary:
        raise RuntimeError('Codex executable unavailable')
    # The managed daemon can be newer than the CLI. No daemon restart/update.
    probe = subprocess.run([binary, 'app-server', 'daemon', 'version'],
                           capture_output=True, text=True, timeout=5)
    if probe.returncode == 0:
        try:
            managed = json.loads(probe.stdout).get('managedCodexPath')
            if managed and Path(managed).is_file():
                return managed
        except json.JSONDecodeError:
            pass
    return binary


def read_limits(timeout):
    # Fresh, short-lived stdio client: proxy initialization timed out on this
    # host. Reuse normal local authentication without reading/printing secrets.
    process = subprocess.Popen([codex_binary(), 'app-server', '--stdio'],
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.DEVNULL, cwd=tempfile.gettempdir())
    selector = selectors.DefaultSelector()
    selector.register(process.stdout, selectors.EVENT_READ)
    buffer = b''

    def send(message):
        process.stdin.write((json.dumps(message) + '\n').encode())
        process.stdin.flush()

    def receive(request_id):
        nonlocal buffer
        end = time.monotonic() + timeout
        while time.monotonic() < end:
            while b'\n' in buffer:
                line, buffer = buffer.split(b'\n', 1)
                message = json.loads(line)
                if message.get('id') == request_id:
                    if 'error' in message:
                        raise RuntimeError('Codex account request failed; verify local sign-in')
                    return message['result']
            if not selector.select(max(0, end - time.monotonic())):
                break
            block = os.read(process.stdout.fileno(), 65536)
            if not block:
                raise RuntimeError('Codex usage connection closed')
            buffer += block
        raise TimeoutError('Codex usage request timed out')

    try:
        send({'method': 'initialize', 'id': 0, 'params': {'clientInfo': {
            'name': 'cbe_usage_guard', 'title': 'CBE weekly usage checkpoint', 'version': '1.0.0'}}})
        receive(0)
        send({'method': 'initialized'})
        send({'method': 'account/rateLimits/read', 'id': 1})
        return receive(1)
    finally:
        selector.close()
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
        process.stdin.close()
        process.stdout.close()


def decision(meter, prior, threshold, resume=False):
    reached = meter['remaining_percent'] <= threshold
    latched = reached or (prior.get('pause_requested', False) and not resume)
    return {'pause_requested': bool(latched),
            'reason': 'threshold_reached' if reached else 'prior_pause_pending' if latched else 'above_threshold'}


def atomic_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode='w', dir=path.parent, delete=False) as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')
        temporary = stream.name
    os.replace(temporary, path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--read-only', action='store_true', help='Fresh verification without changing the saved latch (for /restart)')
    parser.add_argument('--resume', action='store_true', help='After explicit user resume, clear a prior latch only if live allowance is above threshold')
    args = parser.parse_args()
    if args.resume and args.read_only:
        parser.error('--resume and --read-only cannot be combined')
    config = json.loads((ROOT / 'config/codex_usage_guard.json').read_text())
    state_path = ROOT / config['state_file']
    try:
        prior = json.loads(state_path.read_text()) if state_path.exists() else {}
        meter = weekly_meter(read_limits(config['request_timeout_seconds']), config)
        state = {'checked_utc': datetime.now(timezone.utc).isoformat(), **meter,
                 'threshold_remaining_percent': config['weekly_remaining_threshold_percent'],
                 **decision(meter, prior, config['weekly_remaining_threshold_percent'], args.resume)}
        if not args.read_only:
            atomic_json(state_path, state)
        print(json.dumps(state, indent=2))
        return 10 if state['pause_requested'] else 0
    except (OSError, ValueError, KeyError, RuntimeError, TimeoutError, subprocess.SubprocessError):
        print(json.dumps({'status': 'usage_unavailable', 'action': config['on_unavailable']}))
        return 20


if __name__ == '__main__':
    raise SystemExit(main())
