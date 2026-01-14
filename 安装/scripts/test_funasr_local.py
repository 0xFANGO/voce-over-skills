#!/usr/bin/env python
"""
FunASR 本地模式安装验证脚本

用法:
    python test_funasr_local.py           # 快速验证
    python test_funasr_local.py --full    # 完整验证（含模型加载）
    python test_funasr_local.py --download # 下载模型

验证内容:
    1. Python 版本
    2. funasr 包安装
    3. modelscope 包安装
    4. FFmpeg 安装
    5. 模型下载状态
    6. 简单转录测试（可选）
"""

import sys
import os
import subprocess
import shutil


def print_header(text):
    print(f"\n{'='*50}")
    print(f" {text}")
    print(f"{'='*50}")


def print_ok(msg):
    print(f"✅ {msg}")


def print_fail(msg):
    print(f"❌ {msg}")


def print_warn(msg):
    print(f"⚠️  {msg}")


def print_info(msg):
    print(f"   {msg}")


def test_python_version():
    """测试 1: Python 版本"""
    print("\n📌 测试1: Python 版本")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    if version.major >= 3 and version.minor >= 8:
        print_ok(f"Python {version_str} (需要 ≥3.8)")
        return True
    else:
        print_fail(f"Python {version_str} 版本太低，需要 ≥3.8")
        return False


def test_funasr_installed():
    """测试 2: funasr 包安装"""
    print("\n📌 测试2: funasr 包")
    
    try:
        import funasr
        version = getattr(funasr, '__version__', '未知')
        print_ok(f"funasr 已安装 (版本: {version})")
        return True
    except ImportError as e:
        print_fail(f"funasr 未安装")
        print_info(f"请运行: pip install funasr")
        print_info(f"错误: {e}")
        return False


def test_modelscope_installed():
    """测试 3: modelscope 包安装"""
    print("\n📌 测试3: modelscope 包")
    
    try:
        import modelscope
        version = getattr(modelscope, '__version__', '未知')
        print_ok(f"modelscope 已安装 (版本: {version})")
        return True
    except ImportError as e:
        print_fail(f"modelscope 未安装")
        print_info(f"请运行: pip install modelscope")
        print_info(f"错误: {e}")
        return False


def test_ffmpeg_installed():
    """测试 4: FFmpeg 安装"""
    print("\n📌 测试4: FFmpeg")
    
    ffmpeg_path = shutil.which('ffmpeg')
    ffprobe_path = shutil.which('ffprobe')
    
    if ffmpeg_path and ffprobe_path:
        # 获取版本
        try:
            result = subprocess.run(
                ['ffmpeg', '-version'],
                capture_output=True, text=True
            )
            version_line = result.stdout.split('\n')[0]
            print_ok(f"FFmpeg 已安装")
            print_info(f"{version_line}")
            return True
        except Exception as e:
            print_warn(f"FFmpeg 已安装但无法获取版本: {e}")
            return True
    else:
        print_fail("FFmpeg 未安装")
        print_info("macOS: brew install ffmpeg")
        print_info("Ubuntu: sudo apt install ffmpeg")
        return False


def test_model_cache():
    """测试 5: 模型缓存状态"""
    print("\n📌 测试5: 模型缓存")
    
    cache_dir = os.path.expanduser("~/.cache/modelscope/hub")
    
    if not os.path.exists(cache_dir):
        print_warn("模型缓存目录不存在")
        print_info(f"目录: {cache_dir}")
        print_info("首次运行时会自动下载模型（约2GB）")
        return True  # 不算失败，只是提示
    
    # 检查关键模型
    models = {
        'paraformer-zh': 'iic/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch',
        'fsmn-vad': 'iic/speech_fsmn_vad_zh-cn-16k-common-pytorch',
        'ct-punc': 'iic/punc_ct-transformer_zh-cn-common-vocab272727-pytorch',
    }
    
    found_models = []
    missing_models = []
    
    for name, model_id in models.items():
        # 简化的模型路径检查
        model_path = os.path.join(cache_dir, model_id.replace('/', os.sep))
        if os.path.exists(model_path):
            found_models.append(name)
        else:
            # 尝试其他可能的路径格式
            alt_path = os.path.join(cache_dir, 'damo', model_id.split('/')[-1])
            if os.path.exists(alt_path):
                found_models.append(name)
            else:
                missing_models.append(name)
    
    if found_models:
        print_ok(f"已下载模型: {', '.join(found_models)}")
    
    if missing_models:
        print_warn(f"未下载模型: {', '.join(missing_models)}")
        print_info("首次使用时会自动下载")
    
    # 计算缓存大小
    try:
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(cache_dir):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        
        size_gb = total_size / (1024 ** 3)
        print_info(f"缓存目录大小: {size_gb:.2f} GB")
    except Exception:
        pass
    
    return True


def test_model_load():
    """测试 6: 模型加载（可选，较慢）"""
    print("\n📌 测试6: 模型加载测试")
    
    try:
        print_info("正在加载模型（可能需要下载，请稍候）...")
        
        from funasr import AutoModel
        
        model = AutoModel(
            model="paraformer-zh",
            disable_update=True
        )
        
        print_ok("模型加载成功")
        return True
        
    except Exception as e:
        print_fail(f"模型加载失败: {e}")
        return False


def download_models():
    """下载所有需要的模型"""
    print_header("下载 FunASR 模型")
    
    try:
        from funasr import AutoModel
    except ImportError:
        print_fail("funasr 未安装，请先运行: pip install funasr modelscope")
        return False
    
    models = [
        {
            'name': 'paraformer-zh (语音识别)',
            'config': {'model': 'paraformer-zh'}
        },
        {
            'name': 'fsmn-vad (语音活动检测)',
            'config': {'model': 'fsmn-vad'}
        },
        {
            'name': 'ct-punc (标点预测)',
            'config': {'model': 'ct-punc'}
        }
    ]
    
    success_count = 0
    
    for i, model_info in enumerate(models, 1):
        print(f"\n📥 [{i}/{len(models)}] 下载 {model_info['name']}...")
        
        try:
            model = AutoModel(**model_info['config'])
            print_ok(f"{model_info['name']} 下载完成")
            success_count += 1
            # 释放内存
            del model
        except Exception as e:
            print_fail(f"{model_info['name']} 下载失败: {e}")
    
    print()
    if success_count == len(models):
        print_ok(f"所有模型下载完成 ({success_count}/{len(models)})")
        
        # 显示缓存大小
        cache_dir = os.path.expanduser("~/.cache/modelscope/hub")
        try:
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(cache_dir):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    total_size += os.path.getsize(fp)
            size_gb = total_size / (1024 ** 3)
            print_info(f"模型缓存目录: {cache_dir}")
            print_info(f"总大小: {size_gb:.2f} GB")
        except Exception:
            pass
        
        return True
    else:
        print_warn(f"部分模型下载失败 ({success_count}/{len(models)})")
        return False


def verify_and_test():
    """综合验证：加载所有模型并测试转录"""
    print_header("综合验证测试")
    
    try:
        from funasr import AutoModel
        
        print_info("加载完整模型（语音识别 + VAD + 标点）...")
        
        model = AutoModel(
            model="paraformer-zh",
            vad_model="fsmn-vad",
            punc_model="ct-punc",
            disable_update=True
        )
        
        print_ok("模型加载成功")
        print_info("模型组件: paraformer-zh + fsmn-vad + ct-punc")
        
        # 释放内存
        del model
        
        print()
        print("🎉 本地模式完全就绪！可以使用以下命令转录：")
        print()
        print("   python 剪口播/scripts/transcribe_local.py video.mp4")
        print()
        
        return True
        
    except Exception as e:
        print_fail(f"验证失败: {e}")
        return False


def show_help():
    """显示帮助信息"""
    print("""
FunASR 本地模式安装验证脚本

用法:
    python test_funasr_local.py [选项]

选项:
    (无参数)    快速验证（检查依赖，不加载模型）
    --full      完整验证（包含模型加载测试）
    --download  下载所有模型（约2GB）
    --verify    综合验证（加载完整模型）
    --help      显示此帮助

示例:
    # 快速检查环境
    python test_funasr_local.py
    
    # 下载模型
    python test_funasr_local.py --download
    
    # 完整验证
    python test_funasr_local.py --verify
""")


def main():
    # 处理命令行参数
    if '--help' in sys.argv or '-h' in sys.argv:
        show_help()
        return
    
    if '--download' in sys.argv:
        # 下载模式
        success = download_models()
        if not success:
            sys.exit(1)
        return
    
    if '--verify' in sys.argv:
        # 综合验证模式
        success = verify_and_test()
        if not success:
            sys.exit(1)
        return
    
    # 默认：验证模式
    print_header("FunASR 本地模式安装验证")
    
    results = []
    
    # 基础测试
    results.append(("Python 版本", test_python_version()))
    results.append(("funasr 包", test_funasr_installed()))
    results.append(("modelscope 包", test_modelscope_installed()))
    results.append(("FFmpeg", test_ffmpeg_installed()))
    results.append(("模型缓存", test_model_cache()))
    
    print("\n" + "-"*50)
    
    # 检查是否有 --full 参数
    if '--full' in sys.argv:
        results.append(("模型加载", test_model_load()))
    else:
        print_info("跳过模型加载测试")
        print_info("添加 --full 可进行完整测试")
        print_info("添加 --download 可下载模型")
    
    # 汇总结果
    print_header("测试结果汇总")
    
    all_passed = True
    for name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"  {name}: {status}")
        if not passed:
            all_passed = False
    
    print()
    if all_passed:
        print("🎉 所有测试通过！")
        if '--full' not in sys.argv:
            print()
            print("下一步:")
            print("  python test_funasr_local.py --download  # 下载模型")
            print("  python test_funasr_local.py --verify    # 综合验证")
    else:
        print("⚠️  部分测试未通过，请根据提示修复问题")
        sys.exit(1)


if __name__ == '__main__':
    main()
