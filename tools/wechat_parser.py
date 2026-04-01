#!/usr/bin/env python3
"""微信聊天記錄解析器

支援主流匯出工具的格式：
- WeChatMsg 匯出（txt/html/csv）
- 留痕匯出（json）
- PyWxDump 匯出（sqlite）
- 手動複製貼上（純文字）

Usage:
    python wechat_parser.py --file <path> --target <name> --output <output_path> [--format auto]
"""

import argparse
import json
import re
import os
import sys
from datetime import datetime
from typing import Optional
from pathlib import Path


def detect_format(file_path: str) -> str:
    """自動偵測檔案格式"""
    ext = Path(file_path).suffix.lower()

    if ext == '.json':
        return 'liuhen'  # 留痕匯出
    elif ext == '.csv':
        return 'wechatmsg_csv'
    elif ext == '.html' or ext == '.htm':
        return 'wechatmsg_html'
    elif ext == '.db' or ext == '.sqlite':
        return 'pywxdump'
    elif ext == '.txt':
        # 嘗試區分 WeChatMsg txt 和純文字
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            first_lines = f.read(2000)
        # WeChatMsg 格式通常有時間戳模式
        if re.search(r'\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}', first_lines):
            return 'wechatmsg_txt'
        return 'plaintext'
    else:
        return 'plaintext'


def parse_wechatmsg_txt(file_path: str, target_name: str) -> dict:
    """解析 WeChatMsg 匯出的 txt 格式

    典型格式：
    2024-01-15 20:30:45 張三
    今天好累啊

    2024-01-15 20:31:02 我
    怎麼了？
    """
    messages = []
    current_msg = None

    # WeChatMsg 時間戳 + 傳送者模式
    msg_pattern = re.compile(r'^(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+(.+)$')

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.rstrip('\n')
            match = msg_pattern.match(line)
            if match:
                if current_msg:
                    messages.append(current_msg)
                timestamp, sender = match.groups()
                current_msg = {
                    'timestamp': timestamp,
                    'sender': sender.strip(),
                    'content': ''
                }
            elif current_msg and line.strip():
                if current_msg['content']:
                    current_msg['content'] += '\n'
                current_msg['content'] += line

    if current_msg:
        messages.append(current_msg)

    return analyze_messages(messages, target_name)


def parse_liuhen_json(file_path: str, target_name: str) -> dict:
    """解析留痕匯出的 JSON 格式"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    messages = []
    # 留痕格式可能有多種結構，嘗試常見的
    msg_list = data if isinstance(data, list) else data.get('messages', data.get('data', []))

    for msg in msg_list:
        messages.append({
            'timestamp': msg.get('time', msg.get('timestamp', '')),
            'sender': msg.get('sender', msg.get('nickname', msg.get('from', ''))),
            'content': msg.get('content', msg.get('message', msg.get('text', '')))
        })

    return analyze_messages(messages, target_name)


def parse_plaintext(file_path: str, target_name: str) -> dict:
    """解析純文字貼上的聊天記錄"""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    return {
        'raw_text': content,
        'target_name': target_name,
        'format': 'plaintext',
        'message_count': 0,
        'analysis': {
            'note': '純文字格式，需要人工輔助分析'
        }
    }


def analyze_messages(messages: list, target_name: str) -> dict:
    """分析訊息列表，提取關鍵特徵"""
    target_msgs = [m for m in messages if target_name in m.get('sender', '')]
    other_msgs = [m for m in messages if target_name not in m.get('sender', '')]

    # 提取口頭禪（高頻詞分析）
    all_target_text = ' '.join([m['content'] for m in target_msgs if m.get('content')])

    # 提取語氣詞
    particles = re.findall(r'[哈嗯哦噢嘿唉嗚啊呀吧嘛呢嗎麼]+', all_target_text)
    particle_freq = {}
    for p in particles:
        particle_freq[p] = particle_freq.get(p, 0) + 1
    top_particles = sorted(particle_freq.items(), key=lambda x: -x[1])[:10]

    # 提取 emoji
    emoji_pattern = re.compile(
        r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF'
        r'\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF'
        r'\U00002702-\U000027B0\U0000FE00-\U0000FE0F'
        r'\U0001F900-\U0001F9FF]+', re.UNICODE
    )
    emojis = emoji_pattern.findall(all_target_text)
    emoji_freq = {}
    for e in emojis:
        emoji_freq[e] = emoji_freq.get(e, 0) + 1
    top_emojis = sorted(emoji_freq.items(), key=lambda x: -x[1])[:10]

    # 訊息長度統計
    msg_lengths = [len(m['content']) for m in target_msgs if m.get('content')]
    avg_length = sum(msg_lengths) / len(msg_lengths) if msg_lengths else 0

    # 標點習慣
    punctuation_counts = {
        '句號': all_target_text.count('。'),
        '驚嘆號': all_target_text.count('！') + all_target_text.count('!'),
        '問號': all_target_text.count('？') + all_target_text.count('?'),
        '刪節號': all_target_text.count('...') + all_target_text.count('…'),
        '波浪號': all_target_text.count('～') + all_target_text.count('~'),
    }

    return {
        'target_name': target_name,
        'total_messages': len(messages),
        'target_messages': len(target_msgs),
        'other_messages': len(other_msgs),
        'analysis': {
            'top_particles': top_particles,
            'top_emojis': top_emojis,
            'avg_message_length': round(avg_length, 1),
            'punctuation_habits': punctuation_counts,
            'message_style': 'short_burst' if avg_length < 20 else 'long_form',
        },
        'sample_messages': [m['content'] for m in target_msgs[:50] if m.get('content')],
    }


def main():
    parser = argparse.ArgumentParser(description='微信聊天記錄解析器')
    parser.add_argument('--file', required=True, help='輸入檔案路徑')
    parser.add_argument('--target', required=True, help='目標對象的名字/暱稱（如「我」）')
    parser.add_argument('--output', required=True, help='輸出檔案路徑')
    parser.add_argument('--format', default='auto', help='檔案格式 (auto/wechatmsg_txt/liuhen/pywxdump/plaintext)')

    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"錯誤：檔案不存在 {args.file}", file=sys.stderr)
        sys.exit(1)

    fmt = args.format
    if fmt == 'auto':
        fmt = detect_format(args.file)
        print(f"自動偵測格式：{fmt}")

    parsers = {
        'wechatmsg_txt': parse_wechatmsg_txt,
        'liuhen': parse_liuhen_json,
        'plaintext': parse_plaintext,
    }

    parse_func = parsers.get(fmt, parse_plaintext)
    result = parse_func(args.file, args.target)

    # 輸出分析結果
    os.makedirs(os.path.dirname(args.output) or '.', exist_ok=True)

    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(f"# 微信聊天記錄分析 — {args.target}\n\n")
        f.write(f"來源檔案：{args.file}\n")
        f.write(f"偵測格式：{fmt}\n")
        f.write(f"總訊息數：{result.get('total_messages', 'N/A')}\n")
        f.write(f"目標訊息數：{result.get('target_messages', 'N/A')}\n\n")

        analysis = result.get('analysis', {})

        if analysis.get('top_particles'):
            f.write("## 高頻語氣詞\n")
            for word, count in analysis['top_particles']:
                f.write(f"- {word}: {count}次\n")
            f.write("\n")

        if analysis.get('top_emojis'):
            f.write("## 高頻 Emoji\n")
            for emoji, count in analysis['top_emojis']:
                f.write(f"- {emoji}: {count}次\n")
            f.write("\n")

        if analysis.get('punctuation_habits'):
            f.write("## 標點習慣\n")
            for punct, count in analysis['punctuation_habits'].items():
                f.write(f"- {punct}: {count}次\n")
            f.write("\n")

        f.write(f"## 訊息風格\n")
        f.write(f"- 平均訊息長度：{analysis.get('avg_message_length', 'N/A')} 字\n")
        f.write(f"- 風格：{'短句連發型' if analysis.get('message_style') == 'short_burst' else '長段落型'}\n\n")

        if result.get('sample_messages'):
            f.write("## 訊息樣本（前50則）\n")
            for i, msg in enumerate(result['sample_messages'], 1):
                f.write(f"{i}. {msg}\n")

    print(f"分析完成，結果已寫入 {args.output}")


if __name__ == '__main__':
    main()
