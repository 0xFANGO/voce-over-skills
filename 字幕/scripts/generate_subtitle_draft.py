#!/usr/bin/env python3
"""
从转录结果生成分句字幕稿
"""
import json
import re

# 读取转录文件
with open('/Users/fengge/coding/videocut-skills/DEMO/一些生日感受_v1_transcript.json', 'r') as f:
    data = json.load(f)

chars = data['chars']

# 分句参数
max_len = 15  # 每行最大字数
pause_threshold = 0.5  # 停顿阈值（秒）

def split_to_subtitles(chars, max_len=15, pause_threshold=0.5):
    """将字符数组分割为字幕句"""
    subtitles = []
    current = {'text': '', 'start': 0, 'end': 0}

    for i, char_info in enumerate(chars):
        char = char_info['char']
        start = char_info['start']
        end = char_info['end']

        # 计算与前一个字符的间隔
        prev_end = chars[i-1]['end'] if i > 0 else 0
        gap = start - prev_end

        # 分句条件：标点 / 停顿 / 超长
        is_punc = re.match(r'[，。？！、：；]', char)
        is_pause = gap >= pause_threshold
        is_too_long = len(current['text']) >= max_len

        if (is_punc or is_pause or is_too_long) and current['text']:
            # 如果是标点，加上标点再分句
            if is_punc:
                current['text'] += char
                current['end'] = end
            subtitles.append(dict(current))
            current = {'text': '', 'start': start, 'end': end}
            if is_punc:
                continue

        if not current['text']:
            current['start'] = start
        current['text'] += char
        current['end'] = end

    # 最后一句
    if current['text']:
        subtitles.append(current)

    return subtitles

# 分句
subtitles = split_to_subtitles(chars, max_len, pause_threshold)

# 输出字幕稿（去掉句尾标点）
print("=== 字幕稿（纯文本，≤15字/行）===\n")

subtitle_text_lines = []
for sub in subtitles:
    text = sub['text']
    # 去掉句尾标点
    text = re.sub(r'[，。？！、：；]$', '', text)
    print(text)
    subtitle_text_lines.append(text)

# 保存字幕稿
with open('/Users/fengge/coding/videocut-skills/DEMO/一些生日感受_字幕稿.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(subtitle_text_lines))

print(f"\n共 {len(subtitles)} 行")
print(f"字幕稿已保存: 一些生日感受_字幕稿.txt")
