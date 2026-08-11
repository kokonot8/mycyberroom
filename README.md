# Personal Site — Markdown Content Version

这是目前推荐使用的版本：**网站代码与日常内容分离**。

你平时基本不用碰 `index.html`、`style.css`、`app.js` 或 `room.js`。

## 你以后主要使用的目录

```text
content/
├── diary/
├── poet/
├── music/
├── tools/
├── engproject/
├── visual-memory/
├── misc/
└── random/
```

**一个 Markdown 文件 = 网站里的一个条目。**

---

## 最常用：手机新增 Diary

进入 GitHub 仓库：

`content` → `diary` → `Add file` → `Create new file`

文件名例如：

```text
2026-08-20-random-thought.md
```

内容：

```md
---
title: random thought
date: 2026-08-20
---

今天突然想到……

这里直接写正文。
```

然后 Commit。

**完成。**

GitHub Action 会自动读取所有 Markdown，生成 `data/content.json`。主页的 Recent Posts 也会自动读取最新 Diary。

---

## 新增一首诗

在：

```text
content/poet/
```

新建：

```text
rain.md
```

```md
---
title: rain
date: 2026-08-21
---

第一行。
第二行。
第三行。
```

Commit 即可。

---

## 新增 Music / Tool / Engineering Project

格式都一样，例如：

```md
---
title: little sequencer
date: 2026-08-21
link: https://example.com
---

一个晚上做的小工具。

本来只是想试一下，后来越做越奇怪。
```

放在哪个目录，就自动出现在哪个 room。

---

## 新增 Visual Memory（图片）

最简单的方法是把 Markdown 和图片放在同一个目录：

```text
content/visual-memory/
├── tram-window.md
└── tram-window.jpg
```

`tram-window.md`：

```md
---
title: tram window
date: 2026-08-21
image: tram-window.jpg
---

回家的路上。
```

`image: tram-window.jpg` 会自动解析成正确的网站路径。

所以手机上可以：

1. 上传照片到 `content/visual-memory/`
2. 新建一个 `.md`
3. 写照片文件名
4. Commit

---

## Front Matter 支持的字段

```md
---
title: 标题
date: 2026-08-21
link: https://example.com
image: image.jpg
order: 1
---

正文……
```

其中只有 `title` 和正文是最常用的；其他都可以省略。

- `date`：用于自动排序，建议 `YYYY-MM-DD`
- `link`：外部链接
- `image`：图片
- `order`：手动指定顺序（数字越小越前面）；大多数时候不需要

---

## GitHub 自动更新原理

仓库里有：

```text
.github/workflows/build-content.yml
build_content.py
```

每次 `content/**` 有变化时，GitHub Actions 会自动：

```text
你新增 Markdown / 图片
        ↓
GitHub Action 运行
        ↓
扫描 content/ 文件夹
        ↓
生成 data/content.json
        ↓
网站读取新内容
```

所以 `data/content.json` 现在是**自动生成文件**，以后不要手动编辑它。

第一次使用时，如果 Action 无法 push，请在 GitHub 仓库：

`Settings → Actions → General → Workflow permissions`

选择：

**Read and write permissions**

然后保存。

---

## 如果你在电脑本地预览

修改 Markdown 后，可以手动运行：

```bash
python build_content.py
```

然后用本地 server 预览，例如：

```bash
python -m http.server 8000
```

访问：

```text
http://localhost:8000
```

不要直接双击 `index.html`，因为浏览器会限制 `fetch()` 本地 JSON。

---

## 日常维护，你只需要记住这个

```text
想写东西 → content/对应房间/新建 .md → Commit
想放照片 → 上传图片 + 新建 .md → Commit
想改网站本身 → 再去改 HTML/CSS/JS
```

这就是这版网站的核心。
