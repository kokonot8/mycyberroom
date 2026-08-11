from pathlib import Path
import json, re
from datetime import datetime

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
OUTPUT = ROOT / "data" / "content.json"
ROOMS = ["tools", "music", "engproject", "diary", "poet", "visual-memory", "misc", "random"]


def scalar(value: str):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1]
    if value.lower() == "true": return True
    if value.lower() == "false": return False
    if value.lower() in {"null", "none", "~"}: return None
    return value


def parse_markdown(path: Path):
    text = path.read_text(encoding="utf-8")
    meta = {}
    body = text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            front = parts[1]
            body = parts[2].lstrip("\r\n")
            for line in front.splitlines():
                if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
                    continue
                k, v = line.split(":", 1)
                meta[k.strip()] = scalar(v)

    title = str(meta.get("title") or path.stem.replace("-", " "))
    date = str(meta.get("date") or "")
    link = str(meta.get("link") or "")
    image = str(meta.get("image") or "")
    order = meta.get("order", "")

    item = {
        "title": title,
        "date": date,
        "text": body.strip(),
        "link": link,
        "source": str(path.relative_to(ROOT)).replace("\\", "/"),
    }
    if image:
        # Relative image names are resolved next to the markdown file.
        if not re.match(r"^(https?://|/)", image) and "/" not in image:
            image = str((path.parent / image).relative_to(ROOT)).replace("\\", "/")
        item["image"] = image
    if order != "":
        try: item["order"] = int(order)
        except Exception: pass
    return item


def sort_key(item):
    # Explicit order wins; otherwise newest dated entries first.
    order = item.get("order")
    if order is not None:
        return (0, order, "")
    d = item.get("date", "")
    try:
        dt = datetime.fromisoformat(d).timestamp()
    except Exception:
        dt = 0
    return (1, -dt, item.get("title", "").lower())


data = {}
for room in ROOMS:
    folder = CONTENT / room
    items = [parse_markdown(p) for p in folder.glob("*.md") if not p.name.startswith("_")]
    items.sort(key=sort_key)
    data[room] = items

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Built {OUTPUT.relative_to(ROOT)} from {sum(len(v) for v in data.values())} markdown files.")
