#!/usr/bin/env python3
"""Assign English (pinyin-based) slugs to each beast and rewrite manifest.json.

Run once whenever the beast list changes. Slugs are hand-mapped below to avoid
depending on a pinyin library; every beast name in the HTML source must have
an entry here.
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifest.json"

# name(中文) -> slug(英文，url-safe，全小写，短横线分隔)
SLUG_MAP = {
    "鹿白蜀": "lu-bai-shu",
    "玄甲渡": "xuan-jia-du",
    "珠泪哀歌": "zhu-lei-ai-ge",
    "承平鸾": "cheng-ping-luan",
    "青羽": "qing-yu",
    "文鳐": "wen-yao",
    "乘雾银鳞": "cheng-wu-yin-lin",
    "朱千岁": "zhu-qian-sui",
    "不害": "bu-hai",
    "丰年": "feng-nian",
    "精卫": "jing-wei",
    "冉遗鱼": "ran-yi-yu",
    "天马": "tian-ma",
    "祥落": "xiang-luo",
    "当扈": "dang-hu",
    "壤开途": "rang-kai-tu",
    "角端": "jiao-duan",
    "青鸾": "qing-luan",
    "灵鹿": "ling-lu",
    "鲲": "kun",
    "九尾狐": "jiu-wei-hu",
    "独足": "du-zu",
    "白泽": "bai-ze",
    "英招": "ying-zhao",
    "司天人": "si-tian-ren",
    "赤五尾": "chi-wu-wei",
    "食虎": "shi-hu",
    "蛊雕": "gu-diao",
    "唤水人蛇": "huan-shui-ren-she",
    "天狗": "tian-gou",
    "归山狐": "gui-shan-hu",
    "重明鸟": "chong-ming-niao",
    "鹿之白": "lu-zhi-bai",
    "独角断": "du-jiao-duan",
    "同风起": "tong-feng-qi",
    "桃花一处": "tao-hua-yi-chu",
    "螭": "chi-long",
    "天禄": "tian-lu",
    "朱雀玄奇": "zhu-que-xuan-qi",
    "九凤": "jiu-feng",
    "应许龙": "ying-xu-long",
    "凤衔": "feng-xian",
    "麒麟心": "qi-lin-xin",
    "无富奇": "wu-fu-qi",
    "号虎": "hao-hu",
    "开明兽": "kai-ming-shou",
    "九烛": "jiu-zhu",
    "帝江": "di-jiang",
    "红玉": "hong-yu",
}


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    missing = []
    for beast in manifest["beasts"]:
        slug = SLUG_MAP.get(beast["name"])
        if not slug:
            missing.append(beast["name"])
            continue
        beast["slug"] = slug
    if missing:
        raise SystemExit(f"Missing slug mapping for: {missing}")

    manifest["naming"] = {
        "small": "{slug}-small.jpg",
        "large": "{slug}-large.jpg",
    }
    MANIFEST.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"updated {len(manifest['beasts'])} beasts with slugs")


if __name__ == "__main__":
    main()
