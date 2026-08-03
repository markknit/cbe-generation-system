#!/usr/bin/env bash
# ares-mdns-alias.sh — publish `ares.local` over mDNS, and re-publish on IP change.
#
# Why this exists (see STATUS.md "ares.edu -> ares.local hostname migration"):
#   `ares.edu` only ever resolved via a dnsmasq instance on a box that controls
#   DHCP. Plugged into an existing school router it fails silently. mDNS resolves
#   `.local` by broadcast regardless of who runs DHCP, so it works in both
#   deployment modes (own-hotspot and behind-a-school-router).
#
#   A one-off `avahi-publish` does NOT survive reboot, and does not survive the
#   box getting a new DHCP lease. Either failure is silent: name resolution just
#   stops working and nothing logs an error. Hence a systemd service plus this
#   IP-change watch loop.
#
# Requires: avahi-daemon + avahi-utils. Both have been in the Clonezilla golden
# image since Dec 2024 (confirmed from dpkg.log on tsavo3), so there is no
# install step and no internet dependency.
set -uo pipefail

ALIAS_NAME="${ALIAS_NAME:-ares.local}"
CHECK_INTERVAL="${CHECK_INTERVAL:-30}"
PUBLISH_PID=""

log() { echo "[ares-mdns-alias] $*"; }

primary_ip() {
    # Address the box would use to reach off-link traffic. Works whether this
    # machine is its own hotspot or a DHCP client behind a school router.
    ip -4 route get 1.1.1.1 2>/dev/null | awk '{for(i=1;i<=NF;i++) if($i=="src"){print $(i+1); exit}}'
}

stop_publish() {
    if [[ -n "$PUBLISH_PID" ]] && kill -0 "$PUBLISH_PID" 2>/dev/null; then
        kill "$PUBLISH_PID" 2>/dev/null || true
        wait "$PUBLISH_PID" 2>/dev/null || true
    fi
    PUBLISH_PID=""
}

trap 'log "shutting down"; stop_publish; exit 0' TERM INT

command -v avahi-publish-address >/dev/null 2>&1 || {
    log "FATAL: avahi-publish-address not found. Install avahi-utils."
    exit 1
}

CURRENT_IP=""
while true; do
    IP="$(primary_ip)"

    if [[ -z "$IP" ]]; then
        # No route yet (boot race, cable out). Keep waiting rather than exiting,
        # so systemd does not thrash restarting us.
        if [[ -n "$PUBLISH_PID" ]]; then
            log "lost primary IP; withdrawing $ALIAS_NAME"
            stop_publish
            CURRENT_IP=""
        fi
        sleep "$CHECK_INTERVAL"
        continue
    fi

    # Republish if the IP changed, or if the publisher died for any reason.
    if [[ "$IP" != "$CURRENT_IP" ]] || { [[ -n "$PUBLISH_PID" ]] && ! kill -0 "$PUBLISH_PID" 2>/dev/null; }; then
        stop_publish
        log "publishing $ALIAS_NAME -> $IP"
        avahi-publish-address -R "$ALIAS_NAME" "$IP" &
        PUBLISH_PID=$!
        CURRENT_IP="$IP"
    fi

    sleep "$CHECK_INTERVAL"
done
