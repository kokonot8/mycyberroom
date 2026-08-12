from pathlib import Path
import json, re, subprocess
from datetime import datetime

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / 'content'
OUTPUT = ROOT / 'data' / 'content.json'
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
    commands=[
        ['git','log','--diff-filter=A','--follow','--format=%as','--',rel],
        ['git','log','-1','--format=%as','--',rel],
    ]
    for cmd in commands:
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
    # Optional title: front matter > first H1 > filename. H1 is removed from body.
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
    if raw_images:
        if isinstance(raw_images,str):
            for s in re.split(r'\s*[,;]\s*',raw_images):
                if s: images.append(resolve_image(path,s))
    if meta.get('image'): images.insert(0,resolve_image(path,str(meta['image'])))
    # A markdown file inside its own folder automatically collects sibling images.
    if path.parent != CONTENT/room:
        siblings=sorted(p for p in path.parent.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_EXTS)
        for p in siblings:
            rp=str(p.relative_to(ROOT)).replace('\\','/')
            if rp not in images: images.append(rp)
    item={'id':str(path.relative_to(CONTENT/room).with_suffix('')).replace('\\','/'),
          'title':title,'date':date,'text':body,'link':str(meta.get('link') or ''),
          'source':str(path.relative_to(ROOT)).replace('\\','/'),'images':images}
    if meta.get('order') not in ('',None):
        try:item['order']=int(meta['order'])
        except:pass
    return item


def gallery_folder(folder: Path, room: str):
    images=sorted(p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_EXTS)
    if not images:return None
    notes=[p for p in folder.iterdir() if p.is_file() and p.suffix.lower()=='.md']
    if notes:return None # handled by markdown item, which collects sibling images
    title=pretty_name(folder.name)
    date=git_date(images[0]) if images else ''
    return {'id':str(folder.relative_to(CONTENT/room)).replace('\\','/'), 'title':title,'date':date,'text':'','link':'',
            'source':str(folder.relative_to(ROOT)).replace('\\','/'),
            'images':[str(p.relative_to(ROOT)).replace('\\','/') for p in images]}


def sort_key(item):
    if item.get('order') is not None:return (0,item['order'],'')
    try: ts=datetime.fromisoformat(item.get('date','')).timestamp()
    except: ts=0
    return (1,-ts,item.get('title','').lower())


data={}
for room in ROOMS:
    folder=CONTENT/room; folder.mkdir(parents=True,exist_ok=True)
    items=[item_from_md(p,room) for p in folder.rglob('*.md') if not p.name.startswith('_')]
    if room=='visual-memory':
        for d in sorted(p for p in folder.rglob('*') if p.is_dir()):
            g=gallery_folder(d,room)
            if g:items.append(g)
    items.sort(key=sort_key); data[room]=items
OUTPUT.parent.mkdir(parents=True,exist_ok=True)
OUTPUT.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Built {OUTPUT.relative_to(ROOT)} from {sum(map(len,data.values()))} items.')
