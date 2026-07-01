#!/usr/bin/env python3
"""Batch-generate beast images (small + large) via YUNWU gpt-image-2."""

from __future__ import annotations

import argparse
import base64
import io
import json
import os
import pathlib
import time
import urllib.error
import urllib.request

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifest.json"
BEASTS = ROOT / "beasts"
API = "https://api.yunwu.ai/v1/images/generations"

# 展示尺寸远小于生成尺寸：小形态最大只在 360px 容器内显示（2x 视网膜屏 800px 足够），
# 本体全屏展示，横向不需要超过 1600px。统一转 JPEG（原图均无透明通道）大幅省体积。
COMPRESS = {
    "small": {"max_size": 800, "quality": 82},
    "large": {"max_size": 1600, "quality": 82},
}


def compress_to_jpeg(raw: bytes, max_size: int, quality: int) -> bytes:
    img = Image.open(io.BytesIO(raw)).convert("RGB")
    w, h = img.size
    scale = min(1.0, max_size / max(w, h))
    if scale < 1.0:
        img = img.resize((round(w * scale), round(h * scale)), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=quality, optimize=True)
    return buf.getvalue()

SMALL_PROMPT = """新国风插画，中式山海经灵兽绘本风，非日系动漫。正方形构图，主体居中，适合嵌入360x360卡牌立绘框。
守护神兽「{name}」（{title}）日常小形态：圆滚滚、胖乎乎、憨态可掬，像家养瑞兽一样亲近可人，符合《山海经》设定，
趴在青草地小憩，水墨晕染+工笔细线，宣纸质感，温润雅致，可爱慵懒无威压，单角色，无文字，留适当边距"""

LARGE_PROMPT = """新国风插画，中式山海经神兽立像风，非日系动漫。横屏宽幅构图，适合全屏横屏展示。
守护神兽「{name}」（{title}）本体真身：巨大神圣，符合《山海经》设定，横向展开占满画面，
额间赤金神纹，眼神慈悲威严，周身祥光护佑，神性庄严温柔，伏于中式殿宇与祥云之间，金碧暖光，
水墨晕染+工笔重彩，敦煌瑞兽气质，无人物，无文字"""


def api_key() -> str:
    key = os.environ.get("YUNWU__API_KEY") or os.environ.get("YUNWU_API_KEY")
    if not key:
        raise SystemExit("Set YUNWU__API_KEY in environment")
    return key


def generate(prompt: str, size: str, key: str) -> bytes:
    payload = json.dumps(
        {"model": "gpt-image-2", "prompt": prompt, "n": 1, "size": size},
        ensure_ascii=False,
    ).encode()
    req = urllib.request.Request(
        API,
        data=payload,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"},
        method="POST",
    )
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                data = json.loads(resp.read().decode())
            if "error" in data:
                raise RuntimeError(data["error"])
            item = data["data"][0]
            if "b64_json" in item:
                return base64.b64decode(item["b64_json"])
            with urllib.request.urlopen(item["url"], timeout=60) as img:
                return img.read()
        except (urllib.error.URLError, TimeoutError, RuntimeError) as err:
            if attempt == 2:
                raise
            print(f"  retry {attempt + 1}: {err}")
            time.sleep(4)
    raise RuntimeError("unreachable")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", help="comma-separated beast names")
    parser.add_argument("--form", choices=("small", "large", "both"), default="both")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    sizes = manifest["sizes"]
    beasts = manifest["beasts"]
    if args.only:
        names = {n.strip() for n in args.only.split(",")}
        beasts = [b for b in beasts if b["name"] in names]

    key = api_key()
    BEASTS.mkdir(exist_ok=True)

    for beast in beasts:
        name, title, slug = beast["name"], beast["title"], beast.get("slug")
        if not slug:
            raise SystemExit(f"beast {name!r} missing 'slug'; run build_manifest_slugs.py first")
        jobs: list[tuple[str, str, str]] = []
        if args.form in ("small", "both"):
            jobs.append(("small", sizes["small"], SMALL_PROMPT.format(name=name, title=title)))
        if args.form in ("large", "both"):
            jobs.append(("large", sizes["large"], LARGE_PROMPT.format(name=name, title=title)))

        for form, size, prompt in jobs:
            out = BEASTS / f"{slug}-{form}.jpg"
            if out.exists() and not args.force:
                print(f"skip {out.name}")
                continue
            print(f"gen {out.name} ({size})...")
            raw = generate(prompt, size, key)
            cfg = COMPRESS[form]
            jpeg_bytes = compress_to_jpeg(raw, cfg["max_size"], cfg["quality"])
            out.write_bytes(jpeg_bytes)
            print(f"  -> {out.stat().st_size} bytes (raw {len(raw)} bytes)")

    print("done")


if __name__ == "__main__":
    main()
