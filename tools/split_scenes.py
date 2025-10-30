import re
from pathlib import Path
import uuid
import math


CHAPTERS_DIR = Path("chapters")
SCENES_DIR = Path("scenes")


def slugify(text: str) -> str:
    import re as _re
    s = text.strip().lower()
    s = _re.sub(r"[^a-z0-9]+", "-", s)
    s = _re.sub(r"-+", "-", s)
    return s.strip("-")


def read_lines(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return f.readlines()


def split_front_matter(lines):
    if not lines or not lines[0].strip().startswith("---"):
        return None, None, None
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip().startswith("---"):
            end_idx = i
            break
    if end_idx is None:
        return None, None, None
    header_lines = lines[1:end_idx]
    body_lines = lines[end_idx + 1 :]
    return 0, header_lines, body_lines


def parse_simple_yaml(header_lines):
    data = {}
    for idx, raw in enumerate(header_lines):
        line = raw.rstrip("\n")
        if not line.strip() or ":" not in line:
            continue
        key, val = line.split(":", 1)
        key = key.strip()
        val = val.strip()
        if len(val) >= 2 and ((val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'"))):
            val = val[1:-1]
        data[key] = val
    return data


def compute_metrics(body_lines):
    text = "".join(body_lines)
    words = re.findall(r"\b\w+\b", text)
    wc = len(words)
    rt = max(1, math.ceil(wc / 250)) if wc else 0
    tokens = int(round(wc * 1.3))
    return wc, rt, tokens


def find_scene_splits(body_lines):
    # Returns list of scene blocks: each is dict with keys: start, end (exclusive), title (optional), drop_first_line (bool)
    scene_heading_re = re.compile(r"^\s*#{2,6}\s*Scene\s*:\s*(.+?)\s*$", re.IGNORECASE)
    separator_re = re.compile(r"^\s*\*\*\*\s*$")
    markers = []
    for i, line in enumerate(body_lines):
        m_h = scene_heading_re.match(line)
        if m_h:
            markers.append((i, "heading", m_h.group(1).strip()))
            continue
        if separator_re.match(line):
            markers.append((i, "sep", None))
    if not markers:
        # Single block: whole body
        return [{"start": 0, "end": len(body_lines), "title": None, "drop": False}]

    # Build blocks
    blocks = []
    cur_start = 0
    cur_title = None
    for idx, (line_idx, kind, title) in enumerate(markers):
        # Close current block up to marker line
        blocks.append({"start": cur_start, "end": line_idx, "title": cur_title, "drop": False})
        # Prepare next block start
        if kind == "heading":
            # Next block should start after heading line, with title from heading
            cur_start = line_idx + 1
            cur_title = title
        else:
            # Separator: next block starts after separator, no explicit title
            cur_start = line_idx + 1
            cur_title = None

    # Final block to EOF
    blocks.append({"start": cur_start, "end": len(body_lines), "title": cur_title, "drop": False})
    # Remove any empty blocks (e.g., leading marker)
    blocks = [b for b in blocks if b["end"] > b["start"]]
    return blocks


def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def write_scene_file(out_path: Path, meta: dict, body_lines):
    header = [
        "---\n",
        f"id: \"{meta['id']}\"\n",
        f"chapter: {meta['chapter']}\n",
        f"scene: {meta['scene']}\n",
        f"order: {meta['order']}\n",
        f"slug: \"{meta['slug']}\"\n",
        f"title: \"{meta['title']}\"\n",
        f"parent_chapter: \"{meta['parent_chapter']}\"\n",
        f"chapter_title: \"{meta['chapter_title']}\"\n",
        f"chapter_slug: \"{meta['chapter_slug']}\"\n",
        f"prev: {('"'+meta['prev']+'"') if meta['prev'] else 'null'}\n",
        f"next: {('"'+meta['next']+'"') if meta['next'] else 'null'}\n",
        f"word_count: {meta['word_count']}\n",
        f"reading_time_min: {meta['reading_time_min']}\n",
        f"est_tokens: {meta['est_tokens']}\n",
        "---\n",
        "\n",
    ]
    with out_path.open("w", encoding="utf-8", newline="\n") as f:
        f.writelines(header)
        f.writelines(body_lines)


def main():
    ensure_dir(SCENES_DIR)
    chapter_files = sorted(CHAPTERS_DIR.glob("chapter-*.md"))
    all_scenes = []
    # First pass: collect scenes per chapter
    for ch_fp in chapter_files:
        lines = read_lines(ch_fp)
        start, header_lines, body_lines = split_front_matter(lines)
        if header_lines is None:
            continue
        meta = parse_simple_yaml(header_lines)
        ch_num = int(meta.get("chapter", 0))
        ch_title = meta.get("title", ch_fp.stem)
        ch_slug = meta.get("slug", slugify(ch_title))
        ch_stem = ch_fp.stem

        blocks = find_scene_splits(body_lines)
        # Assign scene numbers
        for i, blk in enumerate(blocks, start=1):
            scene_title = blk["title"] if blk["title"] else ("Scene " + str(i))
            # For single scene per chapter with no explicit title, use chapter title
            if len(blocks) == 1 and blk["title"] is None:
                scene_title = ch_title
            scene_slug = slugify(scene_title)
            out_name = f"ch{ch_num:02d}-sc{i:02d}-{scene_slug}.md"
            out_path = SCENES_DIR / out_name
            scene_body = body_lines[blk["start"]: blk["end"]]
            wc, rt, tokens = compute_metrics(scene_body)
            all_scenes.append({
                "path": out_path,
                "chapter": ch_num,
                "scene": i,
                "title": scene_title,
                "slug": scene_slug,
                "parent_chapter": ch_stem,
                "chapter_title": ch_title,
                "chapter_slug": ch_slug,
                "body": scene_body,
                "word_count": wc,
                "reading_time_min": rt,
                "est_tokens": tokens,
            })

    # Order scenes globally by chapter then scene
    all_scenes.sort(key=lambda s: (s["chapter"], s["scene"]))
    # Second pass: write files with prev/next and order
    for idx, sc in enumerate(all_scenes):
        prev_stem = all_scenes[idx - 1]["path"].stem if idx > 0 else None
        next_stem = all_scenes[idx + 1]["path"].stem if idx + 1 < len(all_scenes) else None
        order = sc["chapter"] * 100 + sc["scene"]
        meta = {
            "id": str(uuid.uuid4()),
            "chapter": sc["chapter"],
            "scene": sc["scene"],
            "order": order,
            "slug": sc["slug"],
            "title": sc["title"],
            "parent_chapter": sc["parent_chapter"],
            "chapter_title": sc["chapter_title"],
            "chapter_slug": sc["chapter_slug"],
            "prev": prev_stem,
            "next": next_stem,
            "word_count": sc["word_count"],
            "reading_time_min": sc["reading_time_min"],
            "est_tokens": sc["est_tokens"],
        }
        write_scene_file(sc["path"], meta, sc["body"])

    print(f"Created {len(all_scenes)} scene file(s) in '{SCENES_DIR}'.")


if __name__ == "__main__":
    main()

