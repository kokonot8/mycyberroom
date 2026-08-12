# Personal Site V4 — Atomic Content

这一版的核心变化：**每一条资源都会在构建时生成自己的独立 HTML 页面。**

因此：

- `diary` 房间只负责列出 diary 条目。
- 点击某一条后，进入 `items/diary/xxx/`。
- 该详情页只包含这一条资源，不会加载同分类中的其他资源。
- tools / music / engproject / poet / visual-memory / misc 同理。

## 最省事的上传方式

### 文字
直接新建文件即可，不需要 title/date：

`content/diary/今天想到的.md`

内容可以只有：

```md
今天突然想到一些东西。

继续写正文。
```

标题会自动用文件名 `今天想到的`，日期自动取 GitHub 中该文件第一次提交的日期。

如果想自己指定标题，可以第一行写：

```md
# 我真正想显示的标题

正文……
```

仍然不需要写 date。

## 图片系列 / Visual Memory

一个系列 = 一个文件夹。

例如：

```text
content/visual-memory/amsterdam-night/
├── 01.jpg
├── 02.jpg
├── 03.jpg
└── 04.jpg
```

不用创建 md。构建后它会自动成为一个独立条目：`amsterdam night`。点击进去后，一个网页按顺序显示这四张图。

如果想给整个系列写说明，在同一个文件夹放一个 md：

```text
content/visual-memory/amsterdam-night/
├── note.md
├── 01.jpg
├── 02.jpg
└── 03.jpg
```

`note.md`：

```md
# Amsterdam at night

下班以后随手留下的一些画面。
```

这个 md 和同目录所有图片会被组成**一个**独立资源页。

## GitHub Action

每次 `content/**` 变化后，Action 会运行 `build_content.py`，自动完成两件事：

1. 更新 `data/content.json`（给 hallway / room 索引用）。
2. 生成 `items/<room>/<item>/index.html`（真正的原子详情页）。

你日常不需要编辑 `data/` 或 `items/`。

如果 Action 无法自动提交，检查：

`Settings → Actions → General → Workflow permissions → Read and write permissions`
