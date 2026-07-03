#!/usr/bin/env python3
"""One-off regen for 珠泪哀歌 (zhu-lei-ai-ge) with custom prompts."""

from __future__ import annotations

import importlib.util
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]

_spec = importlib.util.spec_from_file_location(
    "generate_beasts", ROOT / "scripts" / "generate-beasts.py"
)
_gb = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(_gb)

generate = _gb.generate
compress_to_jpeg = _gb.compress_to_jpeg
api_key = _gb.api_key
COMPRESS = _gb.COMPRESS

BEASTS = ROOT / "beasts"
SLUG = "zhu-lei-ai-ge"

SMALL_PROMPT = """新国风插画，水墨晕染+工笔细线，宣纸质感，正方形构图，特写大头近景，脸部占满画面大半，
适合嵌入360x360卡牌立绘框。守护神兽「珠泪哀歌」（含悲成海）日常小形态：完全是一个普通可爱小女孩的人类形象，
绝非怪物、绝非鱼尾、绝非动物，没有鳞片没有异形元素，就是活泼呆萌的小女孩，又圆又大的脸蛋，胖乎乎婴儿肥，
正对镜头呆呆张望，一双眼睛略带斗鸡眼、略微对视聚焦感，眼神呆滞天真、傻乎乎有点笨拙的可爱，嘴巴微张呆萌表情，
看起来智商不太高但憨厚可爱有灵魂，绝非精致美型网红脸，浅紫粉色渐变双马尾头发，简单发带，
唯一的装饰是一只小小的珍珠耳环，眼角下方点缀一点点类似鱼鳞纹路的淡色妆容图案（像小贴纸彩绘一样精致小巧，
不要大面积鳞片、不要额外的珍珠泪痕、不要贝壳堆、不要满身珠饰），穿浅色简单小裙子，
背景是简洁的浅色庭院或草地，温润雅致的传统水墨绘本风格，蠢萌憨态无威压，单角色，无文字，留适当边距"""

LARGE_PROMPT = """新国风插画，水墨晕染+工笔重彩，唯美人物立绘风格。横屏宽幅构图，适合全屏横屏展示。
守护神兽「珠泪哀歌」（含悲成海）本体真身：一位纯人类形态的绝美少女，体型硕大如神祇，矗立于浩瀚暗黑海域中巡游，
占满整个画面，绝非鱼尾、绝非鳞片怪物，是完整的人类身形，身着华丽飘逸的古风长裙，长发随海风与浪涛翻涌飘散，
仰头朝天，脸庞望向漆黑天空，五官精致柔美，姿态优雅庄严又带着一丝哀伤，眼角垂泪化作串串悬浮的珍珠，
背景是电闪雷鸣的暴风夜空，紫金色闪电劈开乌云，照亮脚下翻涌的巨浪与破碎水花，海面泛着幽蓝冷光与雷光交织的
戏剧性强对比光影，气势磅礴又充满哀愁美感，细节繁复华丽，无文字，无殿宇建筑"""


def main() -> None:
    key = api_key()
    jobs = [
        ("large", "1536x1024", LARGE_PROMPT),
    ]
    for form, size, prompt in jobs:
        out = BEASTS / f"{SLUG}-{form}.jpg"
        print(f"gen {out.name} ({size})...")
        raw = generate(prompt, size, key)
        cfg = COMPRESS[form]
        jpeg_bytes = compress_to_jpeg(raw, cfg["max_size"], cfg["quality"])
        out.write_bytes(jpeg_bytes)
        print(f"  -> {out.stat().st_size} bytes (raw {len(raw)} bytes)")


if __name__ == "__main__":
    main()
