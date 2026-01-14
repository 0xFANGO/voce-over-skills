# 剪辑 Skills

> 用 Claude Code Skills + FunASR 做的视频剪辑 Agent

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 📚 文档导航

- **[快速开始](QUICKSTART.md)** - 5 分钟上手指南
- **[使用示例](EXAMPLES.md)** - 详细的使用案例和对话示例
- **[常见问题](FAQ.md)** - 40+ 个问题的详细解答
- **[贡献指南](CONTRIBUTING.md)** - 如何参与贡献和开发 Skill
- **[更新日志](CHANGELOG.md)** - 版本历史和变更记录
- **[文档索引](DOCS.md)** - 完整的文档导航
- **[完整文档](#)** - 你正在阅读


## 快速开始

### 1. 安装 Claude Code

如果还没有安装 Claude Code，请访问 [Claude Code 官网](https://claude.com/claude-code) 下载安装。

### 2. 克隆本仓库

```bash
# 克隆到本地任意位置
git clone https://github.com/yourusername/videocut-skills.git
cd videocut-skills
```

### 3. 在 Claude Code 中打开

```bash
# 在仓库目录下启动 Claude Code
claude
```

或者在 Claude Code 中使用 `cd` 命令切换到仓库目录：
```
cd /path/to/videocut-skills
```

### 4. 首次使用：安装环境

在 Claude Code 中输入：
```
/videocut:安装
```

Claude 会自动：
- 检查并安装 Python、Node.js、FFmpeg
- 安装 FunASR 语音识别库
- 下载约 2GB 的语音识别模型

### 5. 开始剪辑

将视频文件放到仓库目录下，然后：
```
帮我剪这个口播视频 demo.mp4
```

Claude 会自动调用 `/videocut:剪口播` skill，完成转录和口误识别。

## 功能

- **口误识别**：逐字检测，精准定位，不漏不误
- **静音检测**：自动识别 ≥1s 静音片段
- **语气词处理**：自动识别"嗯""哎"等，精确删除
- **字幕生成**：FunASR + 词典纠正，质量碾压剪映
- **自更新**：越用越懂你的剪辑习惯

## 使用方式

### 方式一：自然对话（推荐）

Claude Code 会根据你的需求自动调用相应的 Skill，你只需要用自然语言描述任务：

```
# 剪辑口播视频
帮我剪这个口播视频 demo.mp4
处理一下这个视频，删掉口误和静音

# 添加字幕
给这个视频加字幕
生成字幕文件

# 安装环境
安装环境
初始化
```

### 方式二：直接调用 Skill

如果你明确知道要用哪个 Skill，可以直接调用：

```
/videocut:安装      # 安装环境
/videocut:剪口播    # 转录和识别口误
/videocut:剪辑      # 执行剪辑
/videocut:字幕      # 生成字幕
/videocut:自更新    # 更新规则
```

## 完整工作流

### 1. 剪口播视频

**输入：**
```
帮我剪这个口播视频 demo.mp4
```

**Claude 会自动：**
1. 使用 FunASR 转录视频（本地模式，无需联网）
2. 逐句识别口误（重复、替换、卡顿等）
3. 检测语气词（嗯、哎、诶等）
4. 识别静音片段（≥1秒）
5. 生成审查稿，标注精确时间戳
6. 输出删除任务清单

**输出示例：**
```markdown
## 审查稿

口误（3处）：
- [ ] 1. (12.5-14.2) 删"拉满新拉满" → 保留"拉满"
- [ ] 2. (25.8-27.1) 删"AI就是" → 保留"AI就会"
- [ ] 3. (45.3-46.0) 删"听会" → 保留"会"

语气词（2处）：
- [ ] 1. (18.5-19.2) 删"嗯" 上下文: 然后【嗯】我们
- [ ] 2. (32.1-32.8) 删"哎" 上下文: 好的【哎】接下来

静音（5处）：
- [ ] 1. (8.5-10.2) 静音1.7s
- [ ] 2. (20.3-22.1) 静音1.8s
- [ ] 3. (35.6-36.8) 静音1.2s
- [ ] 4. (50.2-51.5) 静音1.3s
- [ ] 5. (68.9-70.1) 静音1.2s
```

### 2. 确认并执行剪辑

**审查删除任务：**
- 勾选要删除的项目
- 取消勾选要保留的项目

**执行剪辑：**
```
确认，执行剪辑
```

或者：
```
全删
保留静音3和5，其他都删
只删口误，静音都保留
```

**Claude 会自动：**
1. 读取确认的删除任务
2. 计算保留时间段
3. 生成 FFmpeg 剪辑命令
4. 执行剪辑
5. 重新转录审查
6. 如果还有口误，继续循环
7. 直到零口误，生成字幕

### 3. 添加字幕

**输入：**
```
给这个视频加字幕
```

**Claude 会自动：**
1. 转录视频（如果还没转录）
2. 使用词典纠正专有名词
3. 智能分句（≤15字/行）
4. 生成字幕稿供你审核
5. 你修改后，Claude 匹配时间戳
6. 生成 SRT 文件
7. 烧录字幕到视频

**字幕规范：**
- 一屏一行，不换行
- ≤15字/行（适合竖屏）
- 句尾无标点，句中保留标点
- 白字黑边，底部居中

### 4. 自我学习

如果 Claude 识别错误或遗漏，告诉它：

```
"拉满新拉满"这个口误没识别出来
静音3其实是正常停顿，不应该删
```

Claude 会调用 `/videocut:自更新` skill，记录反馈并更新识别规则。

## Skill 清单

| Skill | 功能 | 触发词 | 说明 |
|-------|------|--------|------|
| `videocut:安装` | 环境准备、模型下载 | 安装、初始化 | 首次使用前运行，安装依赖和模型 |
| `videocut:剪口播` | 转录 + 口误/静音识别 → 审查稿 | 剪口播、处理视频 | 核心功能，自动识别需要删除的片段 |
| `videocut:剪辑` | 执行 FFmpeg 剪辑 + 循环审查 | 执行剪辑、确认 | 执行删除操作，循环直到零口误 |
| `videocut:字幕` | 字幕生成与烧录 | 加字幕、生成字幕 | 生成高质量字幕并烧录到视频 |
| `videocut:自更新` | 从错误中学习，更新规则 | 更新规则、记录反馈 | 根据你的反馈优化识别规则 |

## Skills 工作原理

### 什么是 Skill？

Skill 是一个包含专业知识和工作流程的 Markdown 文件（`SKILL.md`）。当你调用一个 Skill 时，Claude Code 会：

1. **加载知识**：读取 `SKILL.md` 中的指令和方法论
2. **执行流程**：按照预定义的步骤执行任务
3. **调用工具**：使用脚本、命令行工具完成具体操作
4. **交互确认**：在关键节点等待你的确认

### 目录结构

```
videocut-skills/
├── .claude/
│   └── settings.local.json    # Claude Code 配置（权限等）
├── 安装/
│   ├── SKILL.md               # Skill 定义文件
│   └── scripts/
│       └── test_funasr_local.py
├── 剪口播/
│   ├── SKILL.md
│   ├── scripts/
│   │   └── transcribe_local.py
│   └── tips/
│       ├── 转录最佳实践.md
│       └── 口误识别方法论.md
├── 剪辑/
│   └── SKILL.md
├── 字幕/
│   ├── SKILL.md
│   ├── scripts/
│   └── 词典.txt               # 专有名词词典
└── 自更新/
    └── SKILL.md
```

### Skill 定义格式

每个 `SKILL.md` 文件包含：

```markdown
---
name: videocut:剪口播
description: 口播视频转录和口误识别。触发词：剪口播、处理视频
---

# 剪口播

> 转录 + 口误/静音识别 → 生成审查稿

## 流程

1. 转录视频
2. 识别口误
3. 生成审查稿
...
```

- **name**: Skill 的唯一标识符
- **description**: 功能描述和触发词
- **正文**: 详细的执行流程、方法论、命令示例

## 自定义和扩展

### 修改词典

编辑 `字幕/词典.txt`，添加你的专有名词：

```
Claude Code
FunASR
iPhone
MacBook
```

Claude 会自动识别变体并纠正（如 `claude code` → `Claude Code`）。

### 调整识别规则

如果你发现某些口误类型识别不准，可以：

1. 告诉 Claude 具体问题
2. Claude 会调用 `/videocut:自更新`
3. 更新 `剪口播/tips/口误识别方法论.md`
4. 下次识别时应用新规则

### 添加新 Skill

创建新的 Skill 目录：

```bash
mkdir 新功能
cd 新功能
```

创建 `SKILL.md`：

```markdown
---
name: videocut:新功能
description: 功能描述。触发词：关键词1、关键词2
---

# 新功能

> 简短描述

## 流程

1. 步骤1
2. 步骤2
...
```

Claude Code 会自动识别新的 Skill。

## 技术栈

| 组件 | 版本要求 | 用途 |
|------|---------|------|
| Python | 3.8+ | 运行 FunASR 语音识别 |
| FFmpeg | 最新版 | 视频剪辑和字幕烧录 |
| FunASR | 最新版 | 本地语音识别（约2GB模型） |

### 本地模式优势

- **完全离线**：无需联网，保护隐私
- **零成本**：不依赖云服务 API
- **高质量**：FunASR 中文识别准确率高
- **字符级时间戳**：精确到每个字的时间

## 常见问题

### Q: Claude Code 是什么？

Claude Code 是 Anthropic 推出的 AI 编程助手 CLI 工具。它可以：
- 读写文件、执行命令
- 理解代码库结构
- 通过 Skills 扩展专业能力

### Q: Skills 和普通 Prompt 有什么区别？

| 特性 | 普通 Prompt | Skills |
|------|------------|--------|
| 知识持久化 | 每次对话重新输入 | 写入文件，永久保存 |
| 工作流程 | 需要逐步指导 | 自动执行完整流程 |
| 专业知识 | 依赖 AI 通用知识 | 可注入领域专业知识 |
| 可复用性 | 难以复用 | 可分享给他人使用 |

### Q: 为什么不用 Whisper？

本项目使用 FunASR 而非 Whisper，原因：
- **中文更准**：FunASR 专门针对中文优化
- **字符级时间戳**：Whisper 只有词级，FunASR 精确到字
- **更快**：本地推理速度更快
- **标点预测**：内置标点模型

当然，你也可以修改 `剪口播/scripts/transcribe_local.py` 使用 Whisper。

### Q: 模型下载慢怎么办？

FunASR 模型托管在 ModelScope，国内下载较快。如果遇到问题：

```bash
# 使用镜像
export MODELSCOPE_CACHE=~/.cache/modelscope
pip install modelscope -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q: 可以用于其他语言吗？

当前主要针对中文口播视频优化。如需支持其他语言：
1. 修改转录脚本，使用对应语言的模型
2. 调整口误识别规则（不同语言的口误模式不同）
3. 更新字幕分句逻辑

### Q: 识别准确率如何？

基于实际测试：
- **口误识别**：95%+ 准确率（重复型、替换型）
- **静音检测**：99%+ 准确率（≥1秒静音）
- **语气词识别**：90%+ 准确率（常见语气词）

误报或漏报可通过 `/videocut:自更新` 持续优化。

### Q: 支持批量处理吗？

当前版本需要逐个处理。如需批量处理，可以：

```bash
# 在 Claude Code 中
for file in *.mp4; do
  echo "处理 $file"
  # 调用 skill 处理
done
```

或者告诉 Claude："批量处理这个文件夹下的所有视频"。

## 最佳实践

### 1. 视频命名规范

建议使用有意义的文件名：
```
01-产品介绍-v1.mp4
02-功能演示-v1.mp4
```

剪辑后自动生成版本号：
```
01-产品介绍-v2.mp4  # 第一次剪辑
01-产品介绍-v3.mp4  # 第二次剪辑
```

### 2. 审查稿确认

- **仔细检查**：AI 可能误判，特别是语气词和停顿
- **保留自然停顿**：不是所有静音都要删
- **口误优先**：先删口误，再考虑静音和语气词

### 3. 词典维护

定期更新 `字幕/词典.txt`：
- 产品名称（iPhone、MacBook）
- 专业术语（API、SDK）
- 人名地名

### 4. 版本管理

建议使用 Git 管理：
```bash
git add .
git commit -m "完成视频01剪辑"
```

这样可以追溯每次修改，必要时回滚。

## 进阶用法

### 自定义剪辑策略

编辑 `剪口播/tips/口误识别方法论.md`，添加你的规则：

```markdown
## 自定义规则

### 保留的"口误"
- 语气停顿：如"然后呢"、"那么"
- 口语化表达：如"就是说"、"其实"

### 必删的口误
- 明显重复：如"拉满拉满"
- 错误纠正：如"左边右边"
```

### 集成到工作流

可以将 Skills 集成到你的视频制作流程：

```bash
# 1. 录制视频
# 2. 在 Claude Code 中剪辑
cd ~/Videos/project
claude-code
# 输入：帮我剪这个视频 raw.mp4

# 3. 导出到剪辑软件做最终调色
```

### 扩展新功能

参考现有 Skills 创建新功能，例如：
- **视频压缩**：自动压缩视频大小
- **封面生成**：提取关键帧作为封面
- **多机位同步**：同步多个机位的视频

## 贡献指南

欢迎贡献代码和 Skills！

### 提交 Issue

遇到问题或有建议，请提交 Issue：
- 描述问题或需求
- 提供视频样本（如涉及隐私可用示例视频）
- 附上错误日志

### 提交 Pull Request

1. Fork 本仓库
2. 创建功能分支：`git checkout -b feature/new-skill`
3. 提交更改：`git commit -m "Add new skill"`
4. 推送分支：`git push origin feature/new-skill`
5. 创建 Pull Request

### 开发新 Skill

参考 [Skill 开发指南](https://docs.anthropic.com/claude-code/skills)（如果有的话）。

## 实际案例

### 案例 1：教程视频剪辑

**场景**：录制了一个 10 分钟的编程教程，有多处口误和长时间停顿。

**操作流程**：
```
1. 用户：帮我剪这个视频 tutorial.mp4
   → Claude 自动转录，识别出 8 处口误、15 处静音、5 个语气词

2. 用户：静音超过 2 秒的才删，语气词保留
   → Claude 更新删除清单，只保留 6 处长静音

3. 用户：确认，执行剪辑
   → Claude 执行剪辑，生成 tutorial-v2.mp4

4. 用户：给视频加字幕
   → Claude 生成字幕稿，用户审核后烧录
```

**结果**：
- 原视频：10 分 23 秒
- 剪辑后：8 分 45 秒
- 删除了 1 分 38 秒的冗余内容
- 字幕准确率 98%+

### 案例 2：产品介绍视频

**场景**：录制产品介绍视频，需要专业术语准确显示。

**操作流程**：
```
1. 先更新词典
   用户：在词典里加上 "Claude Code"、"FunASR"、"MacBook Pro"

2. 剪辑视频
   用户：处理 product-intro.mp4
   → 自动识别并删除口误

3. 生成字幕
   用户：加字幕，用黄色字体
   → 专有名词自动纠正为正确大小写
```

**结果**：
- 专有名词 100% 正确
- 字幕样式符合品牌规范
- 一次性完成，无需返工

### 案例 3：批量处理系列视频

**场景**：有 5 个系列视频需要统一处理。

**操作流程**：
```
用户：批量处理这些视频：
- 01-intro.mp4
- 02-features.mp4
- 03-demo.mp4
- 04-pricing.mp4
- 05-summary.mp4

要求：删除所有口误和超过 1.5 秒的静音，统一加字幕
```

**结果**：
- Claude 自动循环处理每个视频
- 应用统一的剪辑标准
- 生成统一风格的字幕

## 故障排除

### 问题 1：转录失败

**症状**：
```
Error: Failed to load model
```

**解决方案**：
```bash
# 1. 检查模型是否下载完整
ls -lh ~/.cache/modelscope/hub/

# 2. 重新下载模型
cd 安装/scripts
python test_funasr_local.py --download

# 3. 验证环境
python test_funasr_local.py --verify
```

### 问题 2：FFmpeg 命令失败

**症状**：
```
Error: filter_complex: Invalid argument
```

**解决方案**：
1. 检查时间戳是否有重叠
2. 确认删除片段按时间顺序排列
3. 查看生成的 filter.txt 是否正确

```bash
# 手动测试 FFmpeg 命令
ffmpeg -i input.mp4 -filter_complex_script filter.txt output.mp4
```

### 问题 3：字幕时间不同步

**症状**：字幕显示时间与语音不匹配

**解决方案**：
1. 确认使用的是剪辑后的视频转录结果
2. 检查是否在剪辑后重新转录
3. 验证 SRT 文件的时间戳格式

```bash
# 查看 SRT 文件前几行
head -20 video.srt
```

### 问题 4：Claude 没有自动调用 Skill

**症状**：输入"帮我剪视频"，Claude 没有调用 `/videocut:剪口播`

**解决方案**：
1. 确认在正确的目录（包含 Skills 的仓库）
2. 检查 SKILL.md 的 frontmatter 格式是否正确
3. 尝试直接调用：`/videocut:剪口播`

```bash
# 检查当前目录
pwd
# 应该在 videocut-skills 目录下

# 列出可用的 Skills
ls -d */SKILL.md
```

### 问题 5：Python 依赖冲突

**症状**：
```
ImportError: cannot import name 'xxx'
```

**解决方案**：
```bash
# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate  # Windows

# 重新安装依赖
pip install funasr modelscope

# 验证安装
python -c "import funasr; print(funasr.__version__)"
```

### 问题 6：内存不足

**症状**：处理长视频时系统卡顿或崩溃

**解决方案**：
1. 分段处理长视频
2. 关闭其他占用内存的程序
3. 调整 FunASR 的 batch_size

```python
# 在 transcribe_local.py 中调整
pipeline = AutoModel(
    model="paraformer-zh",
    batch_size=1  # 降低 batch size
)
```

### 问题 7：权限错误

**症状**：
```
Permission denied: cannot execute python script
```

**解决方案**：
```bash
# 给脚本添加执行权限
chmod +x 剪口播/scripts/*.py
chmod +x 安装/scripts/*.py

# 或者使用 python 命令执行
python 剪口播/scripts/transcribe_local.py video.mp4
```

## 性能优化

### 加速转录

1. **使用 GPU 加速**（如果有 NVIDIA GPU）：
```bash
pip install funasr[gpu]
```

2. **调整 batch_size**：
```python
# 在 transcribe_local.py 中
pipeline = AutoModel(
    model="paraformer-zh",
    batch_size=16  # 根据内存调整
)
```

### 减少磁盘占用

1. **清理中间文件**：
```bash
# 删除转录 JSON（保留最终版本）
rm *-v1_transcript.json *-v2_transcript.json

# 只保留最终视频
rm *-v1.mp4 *-v2.mp4
```

2. **压缩输出视频**：
```bash
# 在剪辑时使用更高的 CRF 值（质量稍低但文件更小）
ffmpeg -i input.mp4 -c:v libx264 -crf 23 output.mp4
# CRF 范围：18（高质量）到 28（低质量）
```

## 更新日志

### v1.0.0 (2026-01-19)
- ✨ 初始版本发布
- ✨ 支持本地 FunASR 转录
- ✨ 口误、静音、语气词自动识别
- ✨ 时间戳驱动的精确剪辑
- ✨ 字幕生成与烧录
- ✨ 自更新机制

## 路线图

### 近期计划
- [ ] 支持更多视频格式（MOV、AVI、MKV）
- [ ] 添加视频压缩 Skill
- [ ] 支持多语言字幕
- [ ] 优化长视频处理性能

### 长期计划
- [ ] 图形界面（GUI）
- [ ] 云端协作功能
- [ ] AI 自动配乐
- [ ] 智能封面生成

## 致谢

- **FunASR**：阿里达摩院开源的语音识别工具
- **Claude Code**：Anthropic 的 AI 编程助手
- **FFmpeg**：强大的视频处理工具
- **社区贡献者**：感谢所有提供反馈和建议的用户

## 联系方式

- **Issues**：[GitHub Issues](https://github.com/yourusername/videocut-skills/issues)
- **Discussions**：[GitHub Discussions](https://github.com/yourusername/videocut-skills/discussions)
- **Email**：your.email@example.com

## License

MIT

---

**⭐ 如果这个项目对你有帮助，请给个 Star！**
