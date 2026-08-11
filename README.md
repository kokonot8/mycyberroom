# Personal Site V0

A simple static personal site: particle landing → hallway → icon rooms.

## The only files you normally edit

### 1. Add/update content: `data/content.json`
Each room is a list. Copy an existing item and change it:

```json
{"title":"my new thing","date":"2026-08-10","text":"description","link":"https://..."}
```

Rooms: `tools`, `music`, `engproject`, `diary`, `poet`, `visual-memory`, `misc`, `random`.

The homepage automatically shows the first 3 items in `diary`. Put newest diary items first.

### 2. Add images: `assets/`
Copy the image into `assets`, e.g. `summer.jpg`, then use:

```json
{"title":"summer","date":"2026-08-10","text":"","image":"summer.jpg","link":""}
```

### 3. Change homepage room icons/names: `data/site.json`
You normally do not need to touch HTML/CSS/JS.

## Preview locally
Because the site loads JSON, use a tiny local server instead of double-clicking index.html.

Python if available:

```bash
python -m http.server 8000
```

Then open `http://localhost:8000`.

## Publish / update with GitHub Pages
1. Create a GitHub repository.
2. Upload everything in this folder to the repository root.
3. In repository Settings → Pages, deploy from the main branch/root.
4. For future updates, normally only edit `data/content.json` and upload new files to `assets/`, then commit/push.

This separation is intentional: layout/code stays stable; your content is data.
