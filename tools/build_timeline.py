from pathlib import Path


SCENES_DIR = Path("scenes")
OUT = Path("timeline.md")


def read_file(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return f.readlines()


def split_front_matter(lines):
    if not lines or not lines[0].strip().startswith("---"):
        return None, None
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip().startswith("---"):
            end_idx = i
            break
    if end_idx is None:
        return None, None
    header_lines = lines[1:end_idx]
    return header_lines, lines[end_idx + 1 :]


def parse_simple_yaml(header_lines):
    data = {}
    for raw in header_lines:
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


def main():
    files = sorted(SCENES_DIR.glob("*.md"))
    rows = []
    for fp in files:
        lines = read_file(fp)
        header, body = split_front_matter(lines)
        if header is None:
            continue
        meta = parse_simple_yaml(header)
        ch = int(meta.get("chapter", 0)) if meta.get("chapter") else 0
        sc = int(meta.get("scene", 0)) if meta.get("scene") else 0
        title = meta.get("title", fp.stem)
        timeline = meta.get("timeline", "-")
        rows.append({
            "chapter": ch,
            "scene": sc,
            "title": title,
            "timeline": timeline,
            "file": fp.as_posix(),
        })
    # Sort with timeline when present, else by ch/sc
    rows.sort(key=lambda r: ("~" if r["timeline"] == "-" else r["timeline"], r["chapter"], r["scene"]))

    out = []
    out.append("# Timeline\n\n")
    out.append("Brief scene-by-scene timeline. Update each scene's `timeline` field to refine ordering.\n\n")
    out.append("| Timeline | Ch | Sc | Title | File |\n")
    out.append("|---|---:|---:|---|---|\n")
    for r in rows:
        out.append(f"| {r['timeline']} | {r['chapter']} | {r['scene']} | {r['title']} | [{r['file']}]({r['file']}) |\n")

    OUT.write_text("".join(out), encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()

