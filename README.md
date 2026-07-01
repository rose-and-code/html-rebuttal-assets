# html-rebuttal-assets

《山海封灵录》神兽立绘资源库，供 HTML 通过 jsDelivr CDN 引用。

## CDN 地址

```
https://cdn.jsdelivr.net/gh/rose-and-code/html-rebuttal-assets@main/beasts/{神兽名}-small.jpg
https://cdn.jsdelivr.net/gh/rose-and-code/html-rebuttal-assets@main/beasts/{神兽名}-large.jpg
```

示例（九尾狐）：

```
https://cdn.jsdelivr.net/gh/rose-and-code/html-rebuttal-assets@main/beasts/九尾狐-small.jpg
https://cdn.jsdelivr.net/gh/rose-and-code/html-rebuttal-assets@main/beasts/九尾狐-large.jpg
```

push 到 GitHub 后，jsDelivr 通常几分钟内生效。

## 目录

```
beasts/           49×2 张 JPEG（{name}-small.jpg / {name}-large.jpg）
manifest.json     49 只神兽清单与 CDN 配置
scripts/generate-beasts.py   批量生图脚本（自动压缩为 JPEG）
```

## 规格

图片实际展示尺寸远小于 API 生成尺寸，脚本会自动缩放 + 转 JPEG 压缩，体积可降低 80%+。

| 形态 | 文件名后缀 | API 生成尺寸 | 压缩后规格 | HTML 用途 |
|------|-----------|-------------|-----------|-----------|
| 小形态 | `-small.jpg` | 1024×1024 | ≤800×800，质量 82 | 卡牌 `.stage` 立绘（最大 360×360，2x 视网膜够用） |
| 本体 | `-large.jpg` | 1536×1024 | ≤1600px 长边，质量 82 | 点击后全屏横屏展示 |

参考：九尾狐样图压缩前后对比（原 PNG → 压缩 JPEG）：

| 形态 | 压缩前 | 压缩后 | 降幅 |
|------|--------|--------|------|
| small | 2.53 MB | 172 KB | ↓ 93% |
| large | 3.00 MB | 647 KB | ↓ 78% |

## 批量生图

依赖 Pillow 做压缩：

```bash
pip install pillow
export YUNWU__API_KEY='your-key'
python3 scripts/generate-beasts.py              # 缺啥补啥，自动压缩
python3 scripts/generate-beasts.py --only 九尾狐,鹿白蜀
python3 scripts/generate-beasts.py --form small --force
```

## 发布

```bash
git add beasts manifest.json
git commit -m "Add beast images"
git push origin main
```

JPEG 体积已经很小，无需 Git LFS，直接用普通 Git 提交即可。
