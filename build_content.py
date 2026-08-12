from pathlib import Path
import json, re, subprocess, html, shutil
from datetime import datetime

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / 'content'
OUTPUT = ROOT / 'data' / 'content.json'
ITEMS_DIR = ROOT / 'items'
ROOMS = ['tools','music','engproject','diary','poet','visual-memory','misc','random']
IMAGE_EXTS = {'.jpg','.jpeg','.png','.webp','.gif','.avif','.svg'}


def scalar(value: str):
    value=value.strip()
    if len(value)>=2 and value[0]==value[-1] and value[0] in "\"'": value=value[1:-1]
    if value.lower()=='true': return True
    if value.lower()=='false': return False
    if value.lower() in {'null','none','~'}: return None
    return value


def git_date(path: Path):
    rel=str(path.relative_to(ROOT)).replace('\\','/')
    for cmd in [
        ['git','log','--diff-filter=A','--follow','--format=%as','--',rel],
        ['git','log','-1','--format=%as','--',rel],
    ]:
        try:
            out=subprocess.check_output(cmd,cwd=ROOT,text=True,stderr=subprocess.DEVNULL).strip().splitlines()
            if out: return out[-1] if '--diff-filter=A' in cmd else out[0]
        except Exception: pass
    try: return datetime.fromtimestamp(path.stat().st_mtime).date().isoformat()
    except Exception: return ''


def pretty_name(stem):
    return re.sub(r'[_-]+',' ',stem).strip()


def parse_text_file(path: Path):
    text=path.read_text(encoding='utf-8')
    meta={}; body=text
    if text.startswith('---'):
        parts=text.split('---',2)
        if len(parts)==3:
            for line in parts[1].splitlines():
                if line.strip() and not line.lstrip().startswith('#') and ':' in line:
                    k,v=line.split(':',1); meta[k.strip()]=scalar(v)
            body=parts[2].lstrip('\r\n')
    h1=re.match(r'^\s*#\s+(.+?)\s*(?:\n|$)',body)
    if h1 and not meta.get('title'):
        meta['title']=h1.group(1).strip(); body=body[h1.end():].lstrip()
    title=str(meta.get('title') or pretty_name(path.stem))
    date=str(meta.get('date') or git_date(path))
    return meta,body.strip(),title,date


def resolve_image(path: Path, image: str):
    if re.match(r'^(https?://|/)',image): return image
    p=(path.parent/image)
    try: return str(p.relative_to(ROOT)).replace('\\','/')
    except Exception: return image


def item_from_md(path: Path, room: str):
    meta,body,title,date=parse_text_file(path)
    images=[]
    raw_images=meta.get('images')
    if raw_images and isinstance(raw_images,str):
        for s in re.split(r'\s*[,;]\s*',raw_images):
            if s: images.append(resolve_image(path,s))
    if meta.get('image'): images.insert(0,resolve_image(path,str(meta['image'])))
    if path.parent != CONTENT/room:
        siblings=sorted(p for p in path.parent.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_EXTS)
        for p in siblings:
            rp=str(p.relative_to(ROOT)).replace('\\','/')
            if rp not in images: images.append(rp)
    return {
        'id':str(path.relative_to(CONTENT/room).with_suffix('')).replace('\\','/'),
        'title':title,'date':date,'text':body,'link':str(meta.get('link') or ''),
        'source':str(path.relative_to(ROOT)).replace('\\','/'),'images':images
    }


def gallery_folder(folder: Path, room: str):
    images=sorted(p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_EXTS)
    if not images:return None
    notes=[p for p in folder.iterdir() if p.is_file() and p.suffix.lower()=='.md']
    if notes:return None
    return {
        'id':str(folder.relative_to(CONTENT/room)).replace('\\','/'),
        'title':pretty_name(folder.name),
        'date':git_date(images[0]),'text':'','link':'',
        'source':str(folder.relative_to(ROOT)).replace('\\','/'),
        'images':[str(p.relative_to(ROOT)).replace('\\','/') for p in images]
    }


def slug_for(item_id: str):
    slug=re.sub(r'[^a-zA-Z0-9._-]+','--',item_id.strip('/'))
    return slug or 'item'


def sort_key(item):
    try: ts=datetime.fromisoformat(item.get('date','')).timestamp()
    except: ts=0
    return (-ts,item.get('title','').lower())


def body_html(text):
    if not text: return ''
    paras=re.split(r'\n\s*\n', text.strip())
    return ''.join(f'<p>{html.escape(p).replace(chr(10),"<br>")}</p>' for p in paras)


def image_src_for_static(src):
    if re.match(r'^(https?://|/)',src): return src
    return '../../../' + src


def write_item_page(room,item):
    slug=slug_for(item['id'])
    item['url']=f'items/{room}/{slug}/'
    out=ITEMS_DIR/room/slug/'index.html'
    out.parent.mkdir(parents=True,exist_ok=True)
    gallery=''
    if item.get('images'):
        figs=[]
        total=len(item['images'])
        for i,src in enumerate(item['images'],1):
            cap=f'<figcaption>{i} / {total}</figcaption>' if total>1 else ''
            figs.append(f'<figure><img src="{html.escape(image_src_for_static(src),quote=True)}" alt="{html.escape(item["title"],quote=True)} {i}" loading="lazy">{cap}</figure>')
        gallery=f'<div class="gallery {"gallery-series" if total>1 else ""}">{"".join(figs)}</div>'
    link=''
    if item.get('link'):
        link=f'<a class="section-link" href="{html.escape(item["link"],quote=True)}" target="_blank" rel="noopener">open external link →</a>'
    page=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(item['title'])} — my hallway</title><link rel="stylesheet" href="../../../style.css"></head>
<body class="room-page"><nav class="room-nav"><a href="../../../room.html?room={html.escape(room,quote=True)}">← {html.escape(room)}</a><a href="../../../index.html#hallway">hallway</a></nav>
<main class="room-shell"><article class="single-item"><header class="single-head"><span class="date">{html.escape(item.get('date',''))}</span><h1>{html.escape(item['title'])}</h1></header>{gallery}<div class="single-body">{body_html(item.get('text',''))}</div>{link}</article></main></body></html>'''
    out.write_text(page,encoding='utf-8')


if ITEMS_DIR.exists(): shutil.rmtree(ITEMS_DIR)
data={}
for room in ROOMS:
    folder=CONTENT/room; folder.mkdir(parents=True,exist_ok=True)
    items=[item_from_md(p,room) for p in folder.rglob('*.md') if not p.name.startswith('_')]
    if room=='visual-memory':
        for d in sorted(p for p in folder.rglob('*') if p.is_dir()):
            g=gallery_folder(d,room)
            if g:items.append(g)
    items.sort(key=sort_key)
    for item in items: write_item_page(room,item)
    data[room]=items
OUTPUT.parent.mkdir(parents=True,exist_ok=True)
OUTPUT.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Built {sum(map(len,data.values()))} atomic item pages + {OUTPUT.relative_to(ROOT)}.')
