import re
import os
from pathlib import Path


MANUSCRIPT = Path("THE_VERDANT_ACCORD_MANUSCRIPT.md")
OUT_DIR = Path("chapters")


WORD_TO_NUM = {
    "ONE": 1,
    "TWO": 2,
    "THREE": 3,
    "FOUR": 4,
    "FIVE": 5,
    "SIX": 6,
    "SEVEN": 7,
    "EIGHT": 8,
    "NINE": 9,
    "TEN": 10,
    "ELEVEN": 11,
    "TWELVE": 12,
    "THIRTEEN": 13,
    "FOURTEEN": 14,
    "FIFTEEN": 15,
    "SIXTEEN": 16,
    "SEVENTEEN": 17,
    "EIGHTEEN": 18,
    "NINETEEN": 19,
    "TWENTY": 20,
}


def parse_chapter_number(label: str) -> int:
    s = label.strip().upper()
    # Remove any trailing punctuation
    s = re.sub(r"[^A-Z0-9 ]+", "", s)
    # Try integer first
    m = re.search(r"(\d+)", s)
    if m:
        return int(m.group(1))
    # Try word mapping
    return WORD_TO_NUM.get(s, None)


def slugify(text: str) -> str:
    s = text.strip().lower()
    # Replace non-alphanumeric with spaces
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s.strip("-")


def read_lines(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return f.readlines()


def find_chapter_blocks(lines):
    # Find indices of chapter markers
    chapter_re = re.compile(r"^\s*CHAPTER\s+(.+?)\s*$", re.IGNORECASE)
    markers = []  # list of (idx, label)
    for i, line in enumerate(lines):
        m = chapter_re.match(line)
        if m:
            markers.append((i, m.group(1)))

    blocks = []
    for idx, (start, label) in enumerate(markers):
        # Title is the next non-empty line after start
        title_line_index = None
        j = start + 1
        while j < len(lines):
            if lines[j].strip():
                title_line_index = j
                break
            j += 1
        title = lines[title_line_index].strip() if title_line_index is not None else f"Chapter {label.strip()}"

        # Content starts after title line
        content_start = (title_line_index + 1) if title_line_index is not None else (start + 1)

        # End is the line before next chapter marker or EOF
        end = (markers[idx + 1][0] if idx + 1 < len(markers) else len(lines))

        blocks.append({
            "heading_index": start,
            "label": label,
            "title_index": title_line_index,
            "title": title,
            "content_start": content_start,
            "content_end": end,
        })
    return blocks


def ensure_out_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def write_chapter_file(ch_num: int, title: str, body_lines, out_dir: Path):
    num_str = f"{ch_num:02d}"
    filename = f"chapter-{num_str}-{slugify(title)}.md"
    out_path = out_dir / filename
    yaml_header = [
        "---\n",
        f"chapter: {ch_num}\n",
        f"title: \"{title}\"\n",
        "---\n",
        "\n",
    ]
    with out_path.open("w", encoding="utf-8", newline="\n") as f:
        f.writelines(yaml_header)
        f.writelines(body_lines)
    return out_path


def main():
    if not MANUSCRIPT.exists():
        raise SystemExit(f"Manuscript not found: {MANUSCRIPT}")
    lines = read_lines(MANUSCRIPT)
    blocks = find_chapter_blocks(lines)
    if not blocks:
        raise SystemExit("No chapters found (no lines starting with 'CHAPTER').")

    ensure_out_dir(OUT_DIR)

    created = []
    for blk in blocks:
        ch_num = parse_chapter_number(blk["label"]) or 0
        title = blk["title"]
        body = lines[blk["content_start"]: blk["content_end"]]
        path = write_chapter_file(ch_num, title, body, OUT_DIR)
        created.append(path)

    print(f"Created {len(created)} chapter files in '{OUT_DIR}'.")
    for p in created:
        print(p)


if __name__ == "__main__":
    main()

