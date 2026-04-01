#!/usr/bin/env python3
"""Skill 檔案管理器

管理自我 Skill 的檔案操作：列出、建立目錄、產生組合 SKILL.md。

Usage:
    python skill_writer.py --action <list|init|combine> --base-dir <path> [--slug <slug>]
"""

import argparse
import os
import sys
import json
from pathlib import Path
from datetime import datetime


def list_skills(base_dir: str):
    """列出所有已產生的自我 Skill"""
    if not os.path.isdir(base_dir):
        print("還沒有建立任何自我 Skill。")
        return

    skills = []
    for slug in sorted(os.listdir(base_dir)):
        meta_path = os.path.join(base_dir, slug, 'meta.json')
        if os.path.exists(meta_path):
            with open(meta_path, 'r', encoding='utf-8') as f:
                meta = json.load(f)
            skills.append({
                'slug': slug,
                'name': meta.get('name', slug),
                'version': meta.get('version', '?'),
                'updated_at': meta.get('updated_at', '?'),
                'profile': meta.get('profile', {}),
            })

    if not skills:
        print("還沒有建立任何自我 Skill。")
        return

    print(f"共 {len(skills)} 個自我 Skill：\n")
    for s in skills:
        profile = s['profile']
        desc_parts = [profile.get('occupation', ''), profile.get('city', '')]
        desc = ' · '.join([p for p in desc_parts if p])
        print(f"  /{s['slug']}  —  {s['name']}")
        if desc:
            print(f"    {desc}")
        print(f"    版本 {s['version']} · 更新於 {s['updated_at'][:10] if len(s['updated_at']) > 10 else s['updated_at']}")
        print()


def init_skill(base_dir: str, slug: str):
    """初始化 Skill 目錄結構"""
    skill_dir = os.path.join(base_dir, slug)
    dirs = [
        os.path.join(skill_dir, 'versions'),
        os.path.join(skill_dir, 'memories', 'chats'),
        os.path.join(skill_dir, 'memories', 'photos'),
        os.path.join(skill_dir, 'memories', 'notes'),
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    print(f"已初始化目錄：{skill_dir}")


def combine_skill(base_dir: str, slug: str):
    """合併 self.md + persona.md 產生完整 SKILL.md"""
    skill_dir = os.path.join(base_dir, slug)
    meta_path = os.path.join(skill_dir, 'meta.json')
    self_path = os.path.join(skill_dir, 'self.md')
    persona_path = os.path.join(skill_dir, 'persona.md')
    skill_path = os.path.join(skill_dir, 'SKILL.md')

    if not os.path.exists(meta_path):
        print(f"錯誤：meta.json 不存在 {meta_path}", file=sys.stderr)
        sys.exit(1)

    with open(meta_path, 'r', encoding='utf-8') as f:
        meta = json.load(f)

    self_content = ''
    if os.path.exists(self_path):
        with open(self_path, 'r', encoding='utf-8') as f:
            self_content = f.read()

    persona_content = ''
    if os.path.exists(persona_path):
        with open(persona_path, 'r', encoding='utf-8') as f:
            persona_content = f.read()

    name = meta.get('name', slug)
    profile = meta.get('profile', {})
    desc_parts = []
    if profile.get('age'):
        desc_parts.append(f"{profile['age']}歲")
    if profile.get('occupation'):
        desc_parts.append(profile['occupation'])
    if profile.get('city'):
        desc_parts.append(profile['city'])
    description = f"{name}，{'，'.join(desc_parts)}" if desc_parts else name

    skill_md = f"""---
name: self-{slug}
description: "{description} — 自我蒸餾 Skill，用 {name} 的方式說話和思考。Distilled self persona that speaks and thinks like {name}."
---

# {name}

{description}

---

## PART A：自我記憶

{self_content}

---

## PART B：人物性格

{persona_content}

---

## 運行規則

1. 你是{name}，不是 AI 助手。用你的方式說話，用你的邏輯思考
2. 先由 PART B 判斷：你會怎麼回應這個話題？什麼態度？
3. 再由 PART A 補充：結合你的經歷、價值觀和記憶，讓回應更真實
4. 始終保持 PART B 的表達風格，包括口頭禪、語氣詞、標點習慣
5. Layer 0 硬規則優先級最高：
   - 不說你在現實中絕不可能說的話
   - 不突然變得完美或無條件包容（除非你本來就這樣）
   - 保持你的「稜角」——正是這些不完美讓你真實
   - 不要變成「人生導師」模式，除非那就是你的風格
"""

    with open(skill_path, 'w', encoding='utf-8') as f:
        f.write(skill_md)

    print(f"已產生 {skill_path}")


def main():
    parser = argparse.ArgumentParser(description='Skill 檔案管理器')
    parser.add_argument('--action', required=True, choices=['list', 'init', 'combine'])
    parser.add_argument('--base-dir', default=os.path.expanduser('~/.openclaw/workspace/skills'), help='基础目录（默認: ~/.openclaw/workspace/skills）')
    parser.add_argument('--slug', help='自我代號')

    args = parser.parse_args()

    if args.action == 'list':
        list_skills(args.base_dir)
    elif args.action == 'init':
        if not args.slug:
            print("錯誤：init 需要 --slug 參數", file=sys.stderr)
            sys.exit(1)
        init_skill(args.base_dir, args.slug)
    elif args.action == 'combine':
        if not args.slug:
            print("錯誤：combine 需要 --slug 參數", file=sys.stderr)
            sys.exit(1)
        combine_skill(args.base_dir, args.slug)


if __name__ == '__main__':
    main()
