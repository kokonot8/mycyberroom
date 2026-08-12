# Personal Site V3 — drop things in, metadata optional

这版解决三个问题：**不想填 title/date、每个资源独立打开、Visual Memory 支持图片系列。**

## 1. 最简单的文字上传：只写正文

例如在 `content/diary/` 新建 `今天想到的.md`：

```md
今天突然想到……

后面继续写。
```

就够了。`title` 自动取文件名（`今天想到的`），`date` 自动取这个文件第一次进入 Git 的日期。

如果你愿意，也可以第一行写 Markdown 标题：

```md
# 人类社会是一座屎山

正文……
```

这时标题自动使用第一行，第一行不会在正文里重复显示。

原来的 `--- title/date ---` 仍然支持，但**完全不是必填项**。

## 2. 每个资源现在都是独立页面

`room.html?room=diary` 只显示 Diary 的目录/入口。

点击某一条后进入 `item.html`，页面里**只显示这一条资源**，不会再把同目录的其他 Diary 一起排出来。

主页 Recent Posts 也直接进入对应的单篇页面。

## 3. 图片集 / 一个系列多个图片

最省事的方法：在 `content/visual-memory/` 里建一个文件夹，然后直接把多张图片上传进去：

```text
content/visual-memory/
└── 2026-summer/
    ├── IMG_001.jpg
    ├── IMG_002.jpg
    ├── IMG_003.jpg
    └── IMG_004.jpg
```

**不需要 Markdown。** 网站自动把这个文件夹识别成一个 Visual Memory 系列：

- 标题：`2026 summer`（来自文件夹名）
- 日期：自动读取 Git 日期
- 点击后：四张图片出现在同一个独立页面

如果这个系列还想配文字，只需要在同一个文件夹放一个任意名字的 `.md`：

```text
2026-summer/
├── note.md
├── IMG_001.jpg
├── IMG_002.jpg
└── IMG_003.jpg
```

`note.md`：

```md
# summer fragments

那段时间留下来的一些东西。
```

系统会自动把同文件夹所有图片归到这篇内容里。

## 4. 日常手机维护

### Diary / Poet / Music / Tool

```text
GitHub → content → 对应文件夹 → Add file → Create new file
```

只写正文，文件名就是默认标题，然后 Commit。

### Visual Memory 单个系列

```text
GitHub → content/visual-memory → 建一个系列文件夹 → Upload files
```

直接从手机相册一次选择多张图片上传。**只想存图片的话，到这里已经完成。**

想加说明，再补一个 `.md` 即可。

## 5. 自动生成规则

```text
title:
front matter title
  ↓ 没有
第一行 # Markdown 标题
  ↓ 没有
文件名 / 文件夹名

 date:
front matter date
  ↓ 没有
Git 中首次加入该资源的日期
```

GitHub Action 会在 `content/**` 变化后自动运行 `build_content.py` 并更新 `data/content.json`。

第一次使用 Action 时，如果不能自动 push：

`Settings → Actions → General → Workflow permissions → Read and write permissions`

## 6. 文件结构

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

日常原则就是：**想留下什么，就往对应抽屉里丢。元数据能不写就不写。**
