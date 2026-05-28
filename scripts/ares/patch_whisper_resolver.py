# Patch to apply to run_whisper_batch.py on jhm-spark
# Run: python3 scripts/ares/patch_whisper_resolver.py

with open('scripts/ares/run_whisper_batch.py', 'r') as f:
    src = f.read()

old = '''def resolve_kolibri_file(content_id: str) -> Path | None:
    """Resolve a Kolibri content_id to its actual file path on disk."""
    if not content_id or len(content_id) < 2:
        return None
    # Kolibri stores files with hyphens stripped from the UUID
    file_id = content_id.replace("-", "")
    if len(file_id) < 2:
        return None
    storage_dir = KOLIBRI_STORAGE / file_id[0] / file_id[1]
    for ext in VIDEO_EXTENSIONS:
        candidate = storage_dir / f"{file_id}{ext}"
        if candidate.exists():
            return candidate
    return None'''

new = '''def resolve_kolibri_file(content_id: str) -> Path | None:
    """
    Resolve a Kolibri content_id to its actual file path on disk.
    Uses the checksum (stored in kolibri_checksum column) which matches
    the actual filename in storage, not the content node UUID.
    """
    if not content_id or len(content_id) < 2:
        return None
    storage_dir = KOLIBRI_STORAGE / content_id[0] / content_id[1]
    for ext in [".mp4", ".webm", ".ogv", ".m4v"]:
        candidate = storage_dir / f"{content_id}{ext}"
        if candidate.exists():
            return candidate
    return None'''

old2 = '''    for channel in sorted(PRIORITY_CHANNELS_ALL):
        rows = conn.execute(
            """SELECT kolibri_id, title FROM content
               WHERE kolibri_channel = ? AND content_type = 'video'
               AND kolibri_id IS NOT NULL AND kolibri_id != ''""",
            (channel,)
        ).fetchall()
        resolved = 0
        for row in rows:
            path = resolve_kolibri_file(row["kolibri_id"])
            if path:
                add(path)
                resolved += 1
        log.info(f"  {channel}: {len(rows):,} videos in DB, {resolved:,} resolved on disk")

    # STEM-only channels
    for channel in sorted(PRIORITY_CHANNELS_STEM_ONLY):
        rows = conn.execute(
            """SELECT kolibri_id, title FROM content
               WHERE kolibri_channel = ? AND content_type = 'video'
               AND kolibri_id IS NOT NULL AND kolibri_id != ''""",
            (channel,)
        ).fetchall()
        resolved = 0
        stem_matched = 0
        for row in rows:
            if not is_stem_title(row["title"] or ""):
                continue
            stem_matched += 1
            path = resolve_kolibri_file(row["kolibri_id"])
            if path:
                add(path)
                resolved += 1
        log.info(f"  {channel}: {len(rows):,} total, {stem_matched:,} STEM-matched, "
                 f"{resolved:,} resolved on disk")'''

new2 = '''    for channel in sorted(PRIORITY_CHANNELS_ALL):
        rows = conn.execute(
            """SELECT kolibri_checksum, title FROM content
               WHERE kolibri_channel = ? AND content_type = 'video'
               AND kolibri_checksum IS NOT NULL AND kolibri_checksum != ''""",
            (channel,)
        ).fetchall()
        resolved = 0
        for row in rows:
            path = resolve_kolibri_file(row["kolibri_checksum"])
            if path:
                add(path)
                resolved += 1
        log.info(f"  {channel}: {len(rows):,} videos in DB, {resolved:,} resolved on disk")

    # STEM-only channels
    for channel in sorted(PRIORITY_CHANNELS_STEM_ONLY):
        rows = conn.execute(
            """SELECT kolibri_checksum, title FROM content
               WHERE kolibri_channel = ? AND content_type = 'video'
               AND kolibri_checksum IS NOT NULL AND kolibri_checksum != ''""",
            (channel,)
        ).fetchall()
        resolved = 0
        stem_matched = 0
        for row in rows:
            if not is_stem_title(row["title"] or ""):
                continue
            stem_matched += 1
            path = resolve_kolibri_file(row["kolibri_checksum"])
            if path:
                add(path)
                resolved += 1
        log.info(f"  {channel}: {len(rows):,} total, {stem_matched:,} STEM-matched, "
                 f"{resolved:,} resolved on disk")'''

issues = []
if old not in src:
    issues.append("resolve_kolibri_file function not found")
if old2 not in src:
    issues.append("channel loop not found")

if issues:
    print("ERROR:", issues)
else:
    src = src.replace(old, new).replace(old2, new2)
    with open('scripts/ares/run_whisper_batch.py', 'w') as f:
        f.write(src)
    print("Patched OK")
