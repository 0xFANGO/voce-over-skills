#!/usr/bin/env python3
"""
从字幕稿生成SRT字幕文件
"""
import json
import re

# 读取转录文件
with open('/Users/fengge/coding/videocut-skills/DEMO/一些生日感受_v1_transcript.json', 'r') as f:
    data = json.load(f)

chars = data['chars']

# 读取字幕稿
with open('/Users/fengge/coding/videocut-skills/DEMO/一些生日感受_字幕稿.txt', 'r', encoding='utf-8') as f:
    subtitle_lines = [line.strip() for line in f if line.strip()]

def format_time(seconds):
    """格式化时间为SRT时间戳"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

# 匹配字幕稿到时间戳
def match_subtitle_to_time(subtitle_text, chars):
    """将字幕文本匹配到时间戳"""
    # 从字幕稿中移除标点符号来匹配
    clean_text = subtitle_text.replace('，', '').replace('。', '').replace('？', '').replace('！', '')

    # 在chars中查找匹配
    best_match = None
    best_score = 0

    for i in range(len(chars)):
        # 提取从当前位置开始的字符
        extracted = ''
        for j in range(i, min(i + len(clean_text) * 2, len(chars))):
            extracted += chars[j]['char']

        # 检查是否包含目标文本
        if clean_text in extracted:
            start_time = chars[i]['start']

            # 找结束时间
            end_idx = i + len(clean_text) - 1
            if end_idx < len(chars):
                end_time = chars[end_idx]['end']

                if best_match is None:
                    best_match = (start_time, end_time)
                    break

    if best_match:
        return best_match

    # 如果没找到精确匹配，尝试模糊匹配
    words = list(clean_text)
    char_idx = 0

    for i, char_info in enumerate(chars):
        if char_idx < len(words) and char_info['char'] == words[char_idx]:
            if char_idx == 0:
                start_time = char_info['start']
            char_idx += 1
            if char_idx == len(words):
                end_time = char_info['end']
                return (start_time, end_time)

    return None

# 生成SRT
srt_content = []
for i, subtitle_text in enumerate(subtitle_lines):
    time_range = match_subtitle_to_time(subtitle_text, chars)

    if time_range:
        start, end = time_range
        srt_content.append(f"{i + 1}")
        srt_content.append(f"{format_time(start)} --> {format_time(end)}")
        srt_content.append(subtitle_text)
        srt_content.append("")
    else:
        print(f"警告：无法匹配时间戳: {subtitle_text}")

# 保存SRT文件
srt_text = '\n'.join(srt_content)
with open('/Users/fengge/coding/videocut-skills/DEMO/一些生日感受.srt', 'w', encoding='utf-8') as f:
    f.write(srt_text)

print(f"✅ SRT字幕文件已生成: 一些生日感受.srt")
print(f"共 {len(subtitle_lines)} 行字幕")
