"""
openai_engine.py - minimal OpenAI Responses + Batch client for the deck bake-off (presentations branch).

Raw HTTPS with the standard library, so no new dependency is installed. The API key is read from the file named by
OPENAI_KEY_FILE (default ~/.config/codex/secrets/api-key) at call time; it is never printed or logged.

Model under test (Mark, 2026-11-21): gpt-6.1-sol, reasoning effort high.
Prices are NOT available from the API. PRICE below is the third-party list price found 2026-11-21 ($2 in / $10 out
per MTok, cached input $0.10) and the batch discount is ASSUMED to be 50%. Treat every cost this module reports as an
estimate until checked against the OpenAI billing page.
"""
import io
import json
import os
import urllib.error
import urllib.request
import uuid

BASE = "https://api.openai.com/v1"
PRICE = {"in": 2.0, "out": 10.0, "cached": 0.10}  # $/MTok, UNVERIFIED
BATCH_DISCOUNT = 0.5  # UNVERIFIED


def _key():
    p = os.path.expanduser(os.environ.get("OPENAI_KEY_FILE", "~/.config/codex/secrets/api-key"))
    return open(p).read().strip()


def _req(method, path, body=None, headers=None, raw=None, timeout=300):
    h = {"Authorization": "Bearer " + _key(), **(headers or {})}
    data = raw
    if body is not None:
        data = json.dumps(body).encode("utf8"); h["Content-Type"] = "application/json"
    r = urllib.request.Request(BASE + path, data=data, headers=h, method=method)
    try:
        resp = urllib.request.urlopen(r, timeout=timeout)
        return resp.read()
    except urllib.error.HTTPError as e:
        msg = e.read().decode("utf8", "replace")[:800]
        raise RuntimeError(f"OpenAI {method} {path} -> HTTP {e.code}: {msg}") from None


def text_of(user):
    """Anthropic-style content blocks (or a string) -> one string."""
    if isinstance(user, str):
        return user
    return "\n\n".join(b["text"] for b in user)


def responses_body(model, system, user, schema, name, effort="high", max_output_tokens=80000):
    return {
        "model": model,
        "instructions": system,
        "input": text_of(user),
        "reasoning": {"effort": effort},
        "max_output_tokens": max_output_tokens,
        "text": {"format": {"type": "json_schema", "name": name, "schema": schema, "strict": True}},
        "store": False,
    }


def create_response(body):
    return json.loads(_req("POST", "/responses", body))


def parse_response(resp):
    """-> (json_obj, usage_dict). Raises if the response is incomplete or refused."""
    if resp.get("status") != "completed":
        raise RuntimeError(f"status={resp.get('status')} incomplete={resp.get('incomplete_details')} error={resp.get('error')}")
    text = None
    for item in resp.get("output", []):
        if item.get("type") == "message":
            for c in item.get("content", []):
                if c.get("type") == "refusal":
                    raise RuntimeError("refusal: " + str(c.get("refusal"))[:200])
                if c.get("type") == "output_text":
                    text = c["text"]
    if text is None:
        raise RuntimeError("no output_text in response")
    u = resp.get("usage", {})
    usage = {"input_tokens": u.get("input_tokens", 0), "output_tokens": u.get("output_tokens", 0),
             "cached_tokens": (u.get("input_tokens_details") or {}).get("cached_tokens", 0),
             "reasoning_tokens": (u.get("output_tokens_details") or {}).get("reasoning_tokens", 0)}
    return json.loads(text), usage


def cost(u, batch=False):
    fresh = u["input_tokens"] - u["cached_tokens"]
    c = (fresh * PRICE["in"] + u["cached_tokens"] * PRICE["cached"] + u["output_tokens"] * PRICE["out"]) / 1e6
    return c * (BATCH_DISCOUNT if batch else 1)


# ---- Batch API: JSONL of {custom_id, method, url, body} uploaded as a file, then a batch over it ----
def upload_jsonl(lines):
    boundary = uuid.uuid4().hex
    payload = "\n".join(json.dumps(x, ensure_ascii=False) for x in lines).encode("utf8")
    buf = io.BytesIO()
    buf.write(f'--{boundary}\r\nContent-Disposition: form-data; name="purpose"\r\n\r\nbatch\r\n'.encode())
    buf.write(f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="requests.jsonl"\r\nContent-Type: application/jsonl\r\n\r\n'.encode())
    buf.write(payload); buf.write(f"\r\n--{boundary}--\r\n".encode())
    r = _req("POST", "/files", raw=buf.getvalue(), headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}, timeout=600)
    return json.loads(r)["id"]


def create_batch(requests):
    """requests: [{custom_id, body}] for /v1/responses -> batch id."""
    fid = upload_jsonl([{"custom_id": r["custom_id"], "method": "POST", "url": "/v1/responses", "body": r["body"]} for r in requests])
    b = json.loads(_req("POST", "/batches", {"input_file_id": fid, "endpoint": "/v1/responses", "completion_window": "24h"}))
    return b["id"]


def retrieve_batch(bid):
    return json.loads(_req("GET", f"/batches/{bid}"))


def batch_results(batch):
    """Yield (custom_id, response_json_or_None, error_text_or_None) from the output and error files."""
    for key in ("output_file_id", "error_file_id"):
        fid = batch.get(key)
        if not fid:
            continue
        for line in _req("GET", f"/files/{fid}/content", timeout=600).decode("utf8").splitlines():
            if not line.strip():
                continue
            o = json.loads(line)
            resp = (o.get("response") or {})
            if o.get("error") or resp.get("status_code", 200) != 200:
                yield o["custom_id"], None, json.dumps(o.get("error") or resp.get("body"))[:400]
            else:
                yield o["custom_id"], resp["body"], None
