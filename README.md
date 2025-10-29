# The Verdant Accord Manuscript

A working repository for the Verdant Accord novel manuscript. The main manuscript lives in a single source file and is split into per‑chapter Markdown files with helpful YAML metadata to support critique, revision, and compilation workflows.

## Layout

- `THE_VERDANT_ACCORD_MANUSCRIPT.md` — master manuscript source
- `chapters/` — per‑chapter `.md` files with YAML headers
- `tools/` — utilities for splitting and updating metadata

## Tools

### Split manuscript into chapters

- File: `tools/split_chapters.py`
- Detects lines beginning with `CHAPTER <label>` (case‑insensitive), treats the next non‑blank line as the title, then writes chapter files to `chapters/`.
- Usage:

```bash
python tools/split_chapters.py
```

### Update chapter metadata

- File: `tools/update_chapter_metadata.py`
- Scans `chapters/` and auto‑populates fields in each chapter’s YAML front matter. Safe to re‑run; it preserves existing fields and only adds `id` if missing.
- Usage:

```bash
python tools/update_chapter_metadata.py
```

## Metadata schema (current)

Auto‑generated fields per chapter:

- `chapter` — numeric chapter number (from manuscript)
- `title` — chapter title (from manuscript)
- `slug` — slugified title (stable filename‑friendly id)
- `order` — numeric ordering (same as `chapter`)
- `prev` / `next` — neighboring chapter filename stems
- `word_count` — body word count
- `reading_time_min` — estimated reading time (250 wpm)
- `est_tokens` — coarse token estimate (~1.3 × words)
- `id` — stable UUIDv4 (added once, not overwritten)

Recommended editorial fields (manual, optional):

- `synopsis`, `pov`, `person`, `tense`, `distance`
- `goals_conflict_stakes` (nested keys: `goal`, `conflict`, `stakes`)
- `themes` (list), `timeline`, `locations`, `onstage_characters`, `mentioned`
- `status`, `revision`, `last_updated`, `priority`, `todos`, `content_warnings`

## Typical workflow

1) Regenerate chapter files (only when manuscript source changes):

```bash
python tools/split_chapters.py
```

2) Refresh metadata (any time after edits):

```bash
python tools/update_chapter_metadata.py
```

3) Commit changes:

```bash
git add -A && git commit -m "Update chapters/metadata"
```

## Requirements

- Python 3.8+ (tested with 3.13)

## Notes

- The updater is idempotent and safe to run repeatedly. It won’t overwrite existing `id` values.
- If chapter order or titles change, re‑run the updater to refresh `slug`, `order`, `prev`, `next` and counts.

