#!/usr/bin/env python3
"""社群媒體內容解析器

解析朋友圈、微博、小紅書、Instagram 等社群媒體截圖或匯出檔案。
截圖透過 read 工具直接讀取（支援圖片），本工具處理文字匯出。

Usage:
    python social_parser.py --dir <screenshot_dir> --output <output_path>
"""

import argparse
import os
import sys
from pathlib import Path


def scan_directory(dir_path: str) -> dict:
    """掃描目錄，按類型分類檔案"""
    files = {'images': [], 'texts': [], 'other': []}

    image_exts = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}
    text_exts = {'.txt', '.md', '.json', '.csv'}

    for root, dirs, filenames in os.walk(dir_path):
        for fname in filenames:
            fpath = os.path.join(root, fname)
            ext = Path(fname).suffix.lower()
            if ext in image_exts:
                files['images'].append(fpath)
            elif ext in text_exts:
                files['texts'].append(fpath)
            else:
                files['other'].append(fpath)

    return files


def main():
    parser = argparse.ArgumentParser(description='社群媒體內容解析器')
    parser.add_argument('--dir', required=True, help='截圖/檔案目錄')
    parser.add_argument('--output', required=True, help='輸出檔案路徑')

    args = parser.parse_args()

    if not os.path.isdir(args.dir):
        print(f"錯誤：目錄不存在 {args.dir}", file=sys.stderr)
        sys.exit(1)

    files = scan_directory(args.dir)

    os.makedirs(os.path.dirname(args.output) or '.', exist_ok=True)
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write("# 社群媒體內容掃描結果\n\n")
        f.write(f"掃描目錄：{args.dir}\n\n")

        f.write(f"## 檔案統計\n")
        f.write(f"- 圖片檔案：{len(files['images'])} 個\n")
        f.write(f"- 文字檔案：{len(files['texts'])} 個\n")
        f.write(f"- 其他檔案：{len(files['other'])} 個\n\n")

        if files['images']:
            f.write("## 圖片列表（需用 read 工具逐一查看）\n")
            for img in sorted(files['images']):
                f.write(f"- {img}\n")
            f.write("\n")

        if files['texts']:
            f.write("## 文字內容\n")
            for txt in sorted(files['texts']):
                f.write(f"\n### {os.path.basename(txt)}\n")
                try:
                    with open(txt, 'r', encoding='utf-8', errors='ignore') as tf:
                        content = tf.read(5000)
                    f.write(f"```\n{content}\n```\n")
                except Exception as e:
                    f.write(f"讀取失敗：{e}\n")

    print(f"掃描完成，結果已寫入 {args.output}")
    print(f"提示：圖片截圖需使用 read 工具查看，本工具僅列出檔案路徑")


if __name__ == '__main__':
    main()
