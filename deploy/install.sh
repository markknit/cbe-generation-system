#!/usr/bin/env bash
# =============================================================================
# install.sh — provision one ARES school server with the CBE lesson-plan payload
# =============================================================================
# These ~100 servers are independently managed and do NOT run this git repo.
# They receive a zip built by scripts/build_school_payload.sh, unpack it, and
# run this script.
#
#   sudo ./install.sh --dry-run     show every change, touch nothing
#   sudo ./install.sh               apply
#
# What it does, all idempotent (safe to re-run):
#   1. Installs the mDNS alias service so `ares.local` resolves and survives
#      both reboot and a new DHCP lease.
#   2. Adds `ares.local` to nginx's server_name, without disturbing the
#      existing ares.edu / www.ares.edu names.
#   3. Deploys the PDF tree (255 documents + index.html) to the web root.
#   4. Installs the deployed variant of generate_teacher_index.js beside the
#      PDFs so the browse page can be rebuilt on the box.
#   5. Deploys index.htmlf (module landing page) only if the payload has one.
#
# Every step backs up what it replaces and reports what it did.
# =============================================================================
set -euo pipefail

PAYLOAD_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DRY_RUN=0
WEB_ROOT=""
STAMP="$(date +%Y%m%d_%H%M%S)"
BACKUP_DIR="/var/backups/ares-cbe-$STAMP"
CHANGES=(); SKIPS=(); WARNS=()

usage() {
    cat <<EOF
Usage: sudo ./install.sh [--dry-run] [--web-root PATH]

  --dry-run          Print intended changes, modify nothing.
  --web-root PATH    Where the PDF tree should be served from. Auto-detected
                     from the nginx config if omitted.
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --dry-run) DRY_RUN=1; shift ;;
        --web-root) WEB_ROOT="${2:-}"; shift 2 ;;
        -h|--help) usage; exit 0 ;;
        *) echo "Unknown argument: $1" >&2; usage; exit 2 ;;
    esac
done

say()   { echo "  $*"; }
note()  { CHANGES+=("$*"); echo "  [CHANGE] $*"; }
skip()  { SKIPS+=("$*");   echo "  [ok]     $*"; }
warn()  { WARNS+=("$*");   echo "  [WARN]   $*" >&2; }
die()   { echo "  [FATAL]  $*" >&2; exit 1; }

run() {
    if (( DRY_RUN )); then echo "  [dry-run] $*"; else eval "$@"; fi
}

backup() {
    local f="$1"
    [[ -e "$f" ]] || return 0
    run "mkdir -p '$BACKUP_DIR'"
    run "cp -a '$f' '$BACKUP_DIR/'"
    say "backed up $f -> $BACKUP_DIR/"
}

# --- Pre-flight --------------------------------------------------------------
echo "=== ARES CBE payload installer ==============================="
(( DRY_RUN )) && echo "*** DRY RUN - nothing will be modified ***"
[[ $EUID -eq 0 ]] || die "must run as root (sudo ./install.sh)"

[[ -d "$PAYLOAD_DIR/PDF" ]] || die "payload incomplete: no PDF/ directory beside install.sh"
PDF_COUNT="$(find "$PAYLOAD_DIR/PDF" -name '*.pdf' | wc -l)"
(( PDF_COUNT > 0 )) || die "payload PDF/ contains no .pdf files"
say "payload: $PDF_COUNT PDFs at $PAYLOAD_DIR/PDF"

[[ -f "$PAYLOAD_DIR/PDF/index.html" ]] \
    || warn "payload has no PDF/index.html - teachers get no browse page"

# The whole point of the payload: links must be ares.local, not ares.edu.
# A payload built without ARES_HOST=ares.local silently ships dead links
# (this happened corpus-wide between 2026-07-30 and 2026-08-02).
if grep -rqI 'ares\.edu' "$PAYLOAD_DIR/PDF" 2>/dev/null; then
    warn "payload PDFs still reference ares.edu - these links will NOT resolve"
    warn "  behind a school router. Rebuild with scripts/build_school_payload.sh"
    warn "  and re-check before rolling this out widely."
fi

# --- 1. mDNS alias service ---------------------------------------------------
echo
echo "--- 1/5  mDNS alias (ares.local) ---"
command -v avahi-publish-address >/dev/null 2>&1 \
    || warn "avahi-utils missing - ares.local will not publish. Install avahi-utils."
systemctl is-active --quiet avahi-daemon 2>/dev/null \
    || warn "avahi-daemon is not active - enable it or ares.local will not resolve"

if [[ -f "$PAYLOAD_DIR/ares-mdns-alias.sh" && -f "$PAYLOAD_DIR/ares-mdns-alias.service" ]]; then
    backup /usr/local/bin/ares-mdns-alias.sh
    run "install -m 0755 '$PAYLOAD_DIR/ares-mdns-alias.sh' /usr/local/bin/ares-mdns-alias.sh"
    backup /etc/systemd/system/ares-mdns-alias.service
    run "install -m 0644 '$PAYLOAD_DIR/ares-mdns-alias.service' /etc/systemd/system/ares-mdns-alias.service"
    run "systemctl daemon-reload"
    run "systemctl enable ares-mdns-alias.service"
    run "systemctl restart ares-mdns-alias.service"
    note "installed + started ares-mdns-alias.service"
else
    warn "mDNS files missing from payload - skipping step 1"
fi

# --- 2. nginx server_name ----------------------------------------------------
echo
echo "--- 2/5  nginx server_name ---"
# The active config filename VARIES between boxes - do not assume `default`.
# Resolve whatever is actually symlinked into sites-enabled.
NGINX_CONF=""
if [[ -d /etc/nginx/sites-enabled ]]; then
    while IFS= read -r f; do
        if grep -qE '^\s*server_name\b' "$f" 2>/dev/null; then NGINX_CONF="$f"; break; fi
    done < <(find -L /etc/nginx/sites-enabled -maxdepth 1 -type f | sort)
fi

if [[ -z "$NGINX_CONF" ]]; then
    warn "no nginx config with a server_name found in /etc/nginx/sites-enabled - skipping step 2"
elif grep -qE '^\s*server_name\b.*\bares\.local\b' "$NGINX_CONF"; then
    skip "ares.local already in server_name ($NGINX_CONF)"
else
    say "patching $NGINX_CONF"
    backup "$NGINX_CONF"
    # Append ares.local to the existing server_name line, preserving the rest.
    run "sed -i -E 's/^([[:space:]]*server_name[[:space:]]+)(.*);/\1\2 ares.local;/' '$NGINX_CONF'"
    if (( DRY_RUN )); then
        note "would add ares.local to server_name in $NGINX_CONF"
    elif nginx -t >/dev/null 2>&1; then
        run "systemctl reload nginx"
        note "added ares.local to server_name and reloaded nginx"
    else
        say "nginx -t FAILED after patch - rolling back"
        cp -a "$BACKUP_DIR/$(basename "$NGINX_CONF")" "$NGINX_CONF"
        nginx -t || true
        die "nginx config test failed; original restored from $BACKUP_DIR"
    fi
fi

# --- 3. Web root + PDF deploy ------------------------------------------------
echo
echo "--- 3/5  deploy PDF tree ---"
if [[ -z "$WEB_ROOT" && -n "$NGINX_CONF" ]]; then
    WEB_ROOT="$(grep -oP '^\s*root\s+\K[^;]+' "$NGINX_CONF" 2>/dev/null | head -1 | tr -d '"'"'"' ' || true)"
    [[ -n "$WEB_ROOT" ]] && say "web root auto-detected from nginx: $WEB_ROOT"
fi
if [[ -z "$WEB_ROOT" ]]; then
    warn "could not determine the web root - skipping PDF deploy."
    warn "  Re-run with: sudo ./install.sh --web-root /path/to/webroot"
else
    [[ -d "$WEB_ROOT" ]] || die "web root does not exist: $WEB_ROOT"
    DEST="$WEB_ROOT/PDF"
    say "deploying $PDF_COUNT PDFs -> $DEST"
    if (( DRY_RUN )); then
        echo "  [dry-run] rsync -a --delete '$PAYLOAD_DIR/PDF/' '$DEST/'"
    else
        mkdir -p "$DEST"
        # --delete so renamed/removed sub-strands do not leave orphans behind
        # (sub-strand prefixes have been renamed before - the Phase 3 change).
        rsync -a --delete "$PAYLOAD_DIR/PDF/" "$DEST/"
    fi
    note "deployed PDF tree to $DEST"
fi

# --- 4. Deployed teacher-index script ---------------------------------------
echo
echo "--- 4/5  generate_teacher_index.js (deployed variant) ---"
# This copy uses PDF_ROOT = __dirname because it sits INSIDE the PDF folder on
# the server, unlike the repo copy which walks up to data/outputs/v2/PDF.
# That difference is permanent and intentional - see STATUS.md.
if [[ -f "$PAYLOAD_DIR/generate_teacher_index.js" && -n "$WEB_ROOT" ]]; then
    run "install -m 0644 '$PAYLOAD_DIR/generate_teacher_index.js' '$WEB_ROOT/PDF/generate_teacher_index.js'"
    note "installed generate_teacher_index.js into $WEB_ROOT/PDF/"
    command -v node >/dev/null 2>&1 \
        || warn "node not installed - index.html cannot be rebuilt on this box (the shipped one still works)"
else
    skip "no deployed teacher-index script in payload, or no web root - skipping"
fi

# --- 5. Module landing page --------------------------------------------------
echo
echo "--- 5/5  index.htmlf module landing page ---"
if [[ -f "$PAYLOAD_DIR/index.htmlf" && -n "$WEB_ROOT" ]]; then
    backup "$WEB_ROOT/index.htmlf"
    run "install -m 0644 '$PAYLOAD_DIR/index.htmlf' '$WEB_ROOT/index.htmlf'"
    note "deployed index.htmlf"
else
    skip "no index.htmlf in payload - leaving the existing landing page alone"
fi

# --- Summary -----------------------------------------------------------------
echo
echo "=== Summary ================================================="
printf '  changes: %d\n  already ok: %d\n  warnings: %d\n' \
    "${#CHANGES[@]}" "${#SKIPS[@]}" "${#WARNS[@]}"
if (( ${#WARNS[@]} )); then
    echo "  --- warnings ---"
    for w in "${WARNS[@]}"; do echo "   ! $w"; done
fi
[[ -d "$BACKUP_DIR" ]] && echo "  backups: $BACKUP_DIR"
if (( DRY_RUN )); then
    echo "  DRY RUN - nothing changed. Re-run without --dry-run to apply."
else
    cat <<'EOF'
  Verify on this box:
    systemctl status ares-mdns-alias
    ping -c1 ares.local
    curl -sI http://ares.local/PDF/index.html | head -1
  And from a DIFFERENT device on the same network (this is the test that
  actually matters - ares.local resolving on the server itself proves little):
    ping ares.local
EOF
fi
echo "============================================================="
