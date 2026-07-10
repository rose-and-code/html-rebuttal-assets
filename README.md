# html-rebuttal-assets

《山海封灵录》神兽立绘资源库，供 HTML 通过 jsDelivr CDN 引用。

## CDN 地址

图片文件名统一用英文 slug（拼音），避免中文路径的编码/兼容问题：

```
https://cdn.jsdelivr.net/gh/rose-and-code/html-rebuttal-assets@main/beasts/{slug}-small.jpg
https://cdn.jsdelivr.net/gh/rose-and-code/html-rebuttal-assets@main/beasts/{slug}-large.jpg
```

示例（九尾狐 → slug: `jiu-wei-hu`）：

```
https://cdn.jsdelivr.net/gh/rose-and-code/html-rebuttal-assets@main/beasts/jiu-wei-hu-small.jpg
https://cdn.jsdelivr.net/gh/rose-and-code/html-rebuttal-assets@main/beasts/jiu-wei-hu-large.jpg
```

`manifest.json` 里每只神兽都带 `slug` 字段；HTML 端维护一份「中文名 → slug」映射表（`BEAST_SLUG`）来拼接 URL。

push 到 GitHub 后，jsDelivr 通常几分钟内生效。

## 目录

```
beasts/           49×2 张 JPEG（{slug}-small.jpg / {slug}-large.jpg，英文文件名）
manifest.json     49 只神兽清单（name/title/tag/slug）与 CDN 配置
scripts/generate-beasts.py        批量生图脚本（按 slug 命名文件，自动压缩为 JPEG）
scripts/build_manifest_slugs.py   为 manifest.json 补充/重建 slug 字段
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

## 3D 模型（models/）

Echo Spire 项目的 GLB 素材库（meshopt 压缩，Three.js 加载时需配 `MeshoptDecoder`）：

```
models/mv/        10 个纪念碑谷风格雕塑建筑
models/gothic/    62 个哥特教堂零件（塔/大厅/墙/尖顶/拱门…）
models/dkf/       110 个 Dark Fantasy 零件（大中小建筑/塔/雕像/门窗…）
models/scenes/    4 个整体场景（hogwarts / elven-city / island-1 / island-2）
models/manifest.json  各套件零件清单
```

CDN 引用示例：

```
https://cdn.jsdelivr.net/gh/rose-and-code/html-rebuttal-assets@main/models/mv/mv-01.glb
https://cdn.jsdelivr.net/gh/rose-and-code/html-rebuttal-assets@main/models/gothic/tower_001.glb
```

## 3D 模型（models/）

Echo Spire 项目的 GLB 素材库（meshopt 压缩，Three.js 加载时需配 `MeshoptDecoder`）：

```
models/mv/        10 个纪念碑谷风格雕塑建筑
models/gothic/    62 个哥特教堂零件（塔/大厅/墙/尖顶/拱门…）
models/dkf/       110 个 Dark Fantasy 零件（大中小建筑/塔/雕像/门窗…）
models/scenes/    4 个整体场景（hogwarts / elven-city / island-1 / island-2）
models/manifest.json  各套件零件清单
```

CDN 引用示例：

```
https://cdn.jsdelivr.net/gh/rose-and-code/html-rebuttal-assets@main/models/mv/mv-01.glb
https://cdn.jsdelivr.net/gh/rose-and-code/html-rebuttal-assets@main/models/gothic/tower_001.glb
```
