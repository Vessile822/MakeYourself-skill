#!/usr/bin/env python3
"""版本存檔與回滾管理器

Usage:
    python version_manager.py --action <backup|rollback|list> --slug <slug> --base-dir <path> [--version <v>]
"""

import argparse
import os
import sys
import shutil
import json
from datetime import datetime


def backup(base_dir: str, slug: str):
    """備份目前版本"""
    skill_dir = os.path.join(base_dir, slug)
    versions_dir = os.path.join(skill_dir, 'versions')
    meta_path = os.path.join(skill_dir, 'meta.json')

    if not os.path.exists(meta_path):
        print(f"錯誤：meta.json 不存在", file=sys.stderr)
        sys.exit(1)

    with open(meta_path, 'r', encoding='utf-8') as f:
        meta = json.load(f)

    current_version = meta.get('version', 'v0')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f"{current_version}_{timestamp}"
    backup_dir = os.path.join(versions_dir, backup_name)

    os.makedirs(backup_dir, exist_ok=True)

    # 備份核心檔案
    for fname in ['self.md', 'persona.md', 'SKILL.md', 'meta.json']:
        src = os.path.join(skill_dir, fname)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(backup_dir, fname))

    print(f"已備份版本 {backup_name} 至 {backup_dir}")
    return backup_name


def rollback(base_dir: str, slug: str, version: str):
    """回滾到指定版本"""
    skill_dir = os.path.join(base_dir, slug)
    versions_dir = os.path.join(skill_dir, 'versions')

    # 尋找符合的版本
    target_dir = None
    for vname in os.listdir(versions_dir):
        if vname.startswith(version) or vname == version:
            target_dir = os.path.join(versions_dir, vname)
            break

    if not target_dir or not os.path.isdir(target_dir):
        print(f"錯誤：找不到版本 {version}", file=sys.stderr)
        list_versions(base_dir, slug)
        sys.exit(1)

    # 先備份目前版本
    backup(base_dir, slug)

    # 復原檔案
    for fname in ['self.md', 'persona.md', 'SKILL.md', 'meta.json']:
        src = os.path.join(target_dir, fname)
        dst = os.path.join(skill_dir, fname)
        if os.path.exists(src):
            shutil.copy2(src, dst)

    print(f"已回滾到版本 {version}")


def list_versions(base_dir: str, slug: str):
    """列出所有版本"""
    versions_dir = os.path.join(base_dir, slug, 'versions')

    if not os.path.isdir(versions_dir):
        print("沒有歷史版本。")
        return

    versions = sorted(os.listdir(versions_dir), reverse=True)
    if not versions:
        print("沒有歷史版本。")
        return

    print(f"歷史版本（共 {len(versions)} 個）：\n")
    for v in versions:
        print(f"  {v}")


def main():
    parser = argparse.ArgumentParser(description='版本管理器')
    parser.add_argument('--action', required=True, choices=['backup', 'rollback', 'list'])
    parser.add_argument('--slug', required=True, help='自我代號')
    parser.add_argument('--base-dir', default=os.path.expanduser('~/.openclaw/workspace/skills'), help='基础目录（默認: ~/.openclaw/workspace/skills）')
    parser.add_argument('--version', help='回滚目标版本')

    args = parser.parse_args()

    if args.action == 'backup':
        backup(args.base_dir, args.slug)
    elif args.action == 'rollback':
        if not args.version:
            print("錯誤：rollback 需要 --version 參數", file=sys.stderr)
            sys.exit(1)
        rollback(args.base_dir, args.slug, args.version)
    elif args.action == 'list':
        list_versions(args.base_dir, args.slug)


if __name__ == '__main__':
    main()
