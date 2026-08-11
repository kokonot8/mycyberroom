# Personal Site V1 — hallway + rooms

The implemented structure is:

`particle landing → welcome → something i made → diary → something i record for life → random area`

Every square on the hallway opens a room. Rooms use the same visual system and contain the actual entries.

## Everyday updating: only edit ONE file

Open `data/content.json`. You normally do **not** need to edit HTML, CSS, or JavaScript.

Each room is an array:

- `tools`
- `music`
- `engproject`
- `diary`
- `poet`
- `visual-memory`
- `misc`
- `random`

Copy an existing object and change it:

```json
{
  "title": "my new thing",
  "date": "2026-08-12",
  "text": "what I want to say",
  "link": "https://example.com"
}
```

For diary, put the newest entry first. The hallway automatically shows the first 3 diary entries.

## Images / visual memory

1. Upload the image to `assets/`, for example `summer.jpg`.
2. Add `"image": "summer.jpg"` to the entry:

```json
{
  "title": "summer evening",
  "date": "2026-08-12",
  "text": "somewhere I wanted to remember",
  "image": "summer.jpg",
  "link": ""
}
```

## Phone-friendly GitHub workflow

Once this folder is in a GitHub repository and GitHub Pages is enabled:

1. Open the repo on your phone.
2. Edit `data/content.json` directly on GitHub (or github.dev).
3. Upload new photos to `assets/` when needed.
4. Commit changes.
5. GitHub Pages updates the site automatically.

So ordinary content updates are: **edit JSON → commit**. Layout/code stays untouched.

## Preview

Do not double-click `index.html`, because browsers block local JSON fetches. Use GitHub Pages, github.dev preview tooling, or a tiny local server:

```bash
python -m http.server 8000
```

Then open `http://localhost:8000`.

## Files

- `index.html` — hallway page
- `room.html` — shared room page
- `style.css` — all visual styling
- `app.js` — hallway + particles
- `room.js` — room rendering
- `data/site.json` — hallway square names/icons
- `data/content.json` — **your content; edit this most often**
- `assets/` — images
