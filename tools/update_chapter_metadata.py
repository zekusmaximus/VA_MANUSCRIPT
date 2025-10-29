import re
from pathlib import Path
import math
import uuid


CHAPTERS_DIR = Path("chapters")


def slugify(text: str) -> str:
    s = text.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s.strip("-")


def read_file(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return f.readlines()


def write_file(path: Path, lines):
    with path.open("w", encoding="utf-8", newline="\n") as f:
        f.writelines(lines)


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
    order = []
    for idx, raw in enumerate(header_lines):
        line = raw.rstrip("\n")
        if not line.strip():
            continue
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        key = key.strip()
        val = val.strip()
        # Strip surrounding quotes if present
        if len(val) >= 2 and ((val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'"))):
            val_clean = val[1:-1]
        else:
            val_clean = val
        data[key] = {"value": val_clean, "raw_index": idx}
        order.append(key)
    return data, order


def update_or_append_header(header_lines, data_map, key, value, quote=False):
    val_text = f'"{value}"' if quote else str(value)
    line_text = f"{key}: {val_text}\n"
    if key in data_map:
        idx = data_map[key]["raw_index"]
        header_lines[idx] = line_text
    else:
        # Append at end (ensure a blank line before body preserved by caller)
        header_lines.append(line_text)


def compute_word_counts(body_lines):
    body_text = "".join(body_lines)
    # Remove YAML-like fences if any accidentally left (not expected here)
    words = re.findall(r"\b\w+\b", body_text)
    wc = len(words)
    # Reading time: 250 wpm, round up to at least 1 if any words
    rt = max(1, math.ceil(wc / 250)) if wc else 0
    # Estimated tokens (rough): 1.3x words
    tokens = int(round(wc * 1.3))
    return wc, rt, tokens


def collect_chapters():
    files = sorted(CHAPTERS_DIR.glob("chapter-*.md"))
    chapters = []
    for fp in files:
        lines = read_file(fp)
        start, header_lines, body_lines = split_front_matter(lines)
        if header_lines is None:
            continue
        data_map, _ = parse_simple_yaml(header_lines)
        # Prefer explicit chapter number in header; fallback to filename prefix
        ch_num = None
        if "chapter" in data_map:
            try:
                ch_num = int(str(data_map["chapter"]["value"]).strip())
            except Exception:
                ch_num = None
        if ch_num is None:
            m = re.match(r"chapter-(\d+)-", fp.stem)
            ch_num = int(m.group(1)) if m else 0
        # Title
        title = (data_map.get("title", {}).get("value")) or fp.stem
        # Slug (computed from title)
        slug = slugify(title)
        wc, rt, tokens = compute_word_counts(body_lines)
        chapters.append({
            "path": fp,
            "lines": lines,
            "header_lines": header_lines,
            "body_lines": body_lines,
            "data_map": data_map,
            "chapter": ch_num,
            "title": title,
            "slug": slug,
            "word_count": wc,
            "reading_time_min": rt,
            "est_tokens": tokens,
        })
    # Sort by chapter number then filename as tiebreaker
    chapters.sort(key=lambda x: (x["chapter"], x["path"].name))
    return chapters


def apply_updates(chapters):
    # Build prev/next references based on sorted order
    names = [c["path"].stem for c in chapters]
    for i, ch in enumerate(chapters):
        prev_ref = names[i - 1] if i > 0 else None
        next_ref = names[i + 1] if i + 1 < len(chapters) else None

        lines = ch["lines"]
        # Reconstruct header region
        start, header_lines, body_lines = split_front_matter(lines)
        data_map, _ = parse_simple_yaml(header_lines)

        # Ensure fields
        # Stable id: only set if missing, never overwrite
        if "id" not in data_map or not str(data_map["id"]["value"]).strip():
            new_id = str(uuid.uuid4())
            update_or_append_header(header_lines, data_map, "id", new_id, quote=True)
        update_or_append_header(header_lines, data_map, "slug", ch["slug"], quote=True)
        update_or_append_header(header_lines, data_map, "order", ch["chapter"], quote=False)
        if prev_ref is not None:
            update_or_append_header(header_lines, data_map, "prev", prev_ref, quote=True)
        else:
            # Remove if present by replacing with empty or ignoring; simplest: set to null
            update_or_append_header(header_lines, data_map, "prev", "null", quote=False)
        if next_ref is not None:
            update_or_append_header(header_lines, data_map, "next", next_ref, quote=True)
        else:
            update_or_append_header(header_lines, data_map, "next", "null", quote=False)
        update_or_append_header(header_lines, data_map, "word_count", ch["word_count"], quote=False)
        update_or_append_header(header_lines, data_map, "reading_time_min", ch["reading_time_min"], quote=False)
        update_or_append_header(header_lines, data_map, "est_tokens", ch["est_tokens"], quote=False)

        # Stitch back together
        out_lines = []
        out_lines.append("---\n")
        out_lines.extend(header_lines)
        out_lines.append("---\n")
        out_lines.extend(body_lines)
        write_file(ch["path"], out_lines)


def main():
    if not CHAPTERS_DIR.exists():
        raise SystemExit(f"Chapters directory not found: {CHAPTERS_DIR}")
    chapters = collect_chapters()
    if not chapters:
        raise SystemExit("No chapter files found to update.")
    apply_updates(chapters)
    print(f"Updated {len(chapters)} chapter file(s) with metadata.")


if __name__ == "__main__":
    main()
