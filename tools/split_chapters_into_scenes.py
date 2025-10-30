#!/usr/bin/env python3
"""
Split chapter Markdown files into scene files based on explicit scene markers.

Usage examples:
  python tools/split_chapters_into_scenes.py           # process all chapters
  python tools/split_chapters_into_scenes.py --chapter 1
  python tools/split_chapters_into_scenes.py --overwrite
  python tools/split_chapters_into_scenes.py --dry-run

How it works:
- Looks for chapters in ./chapters named like chapter-01-*.md
- Expects scene break markers in chapter body like:
    <!-- SCENE: Title or short note -->
- Writes scenes into ./scenes using your existing pattern:
    ch{chapter:02}-sc{scene:02}-{chapter_slug}.md
- Skips writing a scene file that already exists unless --overwrite is set.

Notes:
- The first scene starts at the first <!-- SCENE: ... --> marker. Content before
  the first marker is ignored to avoid duplicating existing sc01 files.
- Front matter is preserved only for needed metadata (chapter, title, slug).
- Safe defaults: no network, no deps, Windows-friendly paths.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHAPTERS_DIR = ROOT / "chapters"
SCENES_DIR = ROOT / "scenes"


FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?", re.DOTALL)
# Accept either `<!-- SCENE: Title -->` or `<!-- SCENE -->` (case-insensitive)
SCENE_MARK_RE = re.compile(
    r"^\s*<!--\s*SCENE(?:\s*:\s*(.*?))?\s*-->\s*$",
    re.MULTILINE | re.IGNORECASE,
)


def parse_front_matter(text: str) -> tuple[dict, str]:
    """Return (front_matter_dict, body_text)."""
    m = FRONT_MATTER_RE.match(text)
    fm: dict[str, str] = {}
    if not m:
        return fm, text
    raw = m.group(1)
    body = text[m.end() :]
    for line in raw.splitlines():
        # naive YAML-ish parsing: key: value or key: "value"
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        key = key.strip()
        val = val.strip().strip('"')
        fm[key] = val
    return fm, body


def chapter_iter(chapter_filter: int | None):
    if not CHAPTERS_DIR.exists():
        return
    for p in sorted(CHAPTERS_DIR.glob("chapter-*.md")):
        # Expect chapter-XX-*.md
        name = p.name
        m = re.match(r"chapter-(\d{2})-", name)
        if not m:
            continue
        ch_num = int(m.group(1))
        if chapter_filter is not None and ch_num != chapter_filter:
            continue
        yield ch_num, p


def existing_scene_numbers_for(chapter_num: int) -> set[int]:
    out: set[int] = set()
    pattern = f"ch{chapter_num:02d}-sc*.md"
    for p in SCENES_DIR.glob(pattern):
        m = re.match(rf"ch{chapter_num:02d}-sc(\d{{2}})-", p.name)
        if m:
            out.add(int(m.group(1)))
    return out


def safe_slug(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")
    return s or "scene"


def split_chapter(ch_num: int, path: Path, overwrite: bool, dry_run: bool) -> int:
    text = path.read_text(encoding="utf-8")
    fm, body = parse_front_matter(text)

    chapter_title = fm.get("title", "").strip('"') if fm else ""
    chapter_slug = fm.get("slug", "") if fm else ""
    if not chapter_slug:
        # derive from filename if missing
        m = re.match(r"chapter-\d{2}-(.*)\.md$", path.name)
        chapter_slug = m.group(1) if m else f"chapter-{ch_num:02d}"

    # Find scene markers
    markers = list(SCENE_MARK_RE.finditer(body))
    if not markers:
        print(f"[skip] Chapter {ch_num:02d}: no scene markers found in {path.name}")
        return 0

    # Prepare segments: from each marker to next marker (or end)
    segments: list[tuple[str, str]] = []  # (scene_title, scene_text)
    for i, m in enumerate(markers):
        start = m.end()
        end = markers[i + 1].start() if i + 1 < len(markers) else len(body)
        raw_title = m.group(1) if m.lastindex else None
        title = (raw_title or "").strip() or f"Scene {i+1}"
        content = body[start:end].lstrip("\n").rstrip() + "\n"
        segments.append((title, content))

    SCENES_DIR.mkdir(parents=True, exist_ok=True)

    existing = existing_scene_numbers_for(ch_num)
    created = 0
    next_scene_num = 1

    for idx, (title, content) in enumerate(segments, start=1):
        # Try to align numbering to avoid overwriting existing files.
        # If idx exists, skip unless overwrite; otherwise use idx.
        scene_num = idx
        if not overwrite and scene_num in existing:
            print(f"[skip] ch{ch_num:02d}-sc{scene_num:02d} exists; not overwriting")
            continue

        # Keep your existing naming convention: chapter slug only
        filename = f"ch{ch_num:02d}-sc{scene_num:02d}-{chapter_slug}.md"
        out_path = SCENES_DIR / filename

        # Compose scene file with minimal front matter
        scene_fm = (
            "---\n"
            f"chapter: {ch_num}\n"
            f"scene: {scene_num}\n"
            f"chapter_title: \"{chapter_title}\"\n"
            f"title: \"{title}\"\n"
            f"slug: \"{chapter_slug}\"\n"
            f"order: {scene_num}\n"
            "---\n\n"
        )
        data = scene_fm + content

        if dry_run:
            print(f"[dry-run] Would write {out_path}")
        else:
            out_path.write_text(data, encoding="utf-8")
            print(f"[write] {out_path.relative_to(ROOT)}")
            created += 1
        next_scene_num += 1

    return created


def main():
    ap = argparse.ArgumentParser(description="Split chapters into scenes.")
    ap.add_argument("--chapter", type=int, help="Only process one chapter number, e.g., 1", default=None)
    ap.add_argument("--overwrite", action="store_true", help="Overwrite existing scene files")
    ap.add_argument("--dry-run", action="store_true", help="Show actions without writing files")
    args = ap.parse_args()

    if not CHAPTERS_DIR.exists():
        print(f"No chapters directory found at {CHAPTERS_DIR}")
        return

    total_created = 0
    for ch_num, p in chapter_iter(args.chapter):
        created = split_chapter(ch_num, p, overwrite=args.overwrite, dry_run=args.dry_run)
        total_created += created

    if total_created:
        print(f"Done. Created {total_created} scene file(s).")
    else:
        print("No new scene files created.")


if __name__ == "__main__":
    main()
