import os
import subprocess
import requests
import gzip
import shutil
import stat

# --- 核心配置 ---
# 获取当前脚本所在的绝对路径，以此为基准定位其他目录
# 这样无论在哪个目录下运行，路径永远是正确的
CURRENT_SCRIPT_PATH = os.path.abspath(__file__)
SCRIPT_DIR = os.path.dirname(CURRENT_SCRIPT_PATH)         # .../Clash/scripts
ROOT_DIR = os.path.dirname(SCRIPT_DIR)                    # .../Clash
OUTPUT_DIR = os.path.join(ROOT_DIR, "rule-set")           # .../Clash/rule-set

# 远程规则
UPSTREAM_RULES = [
    {
        "url": "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/SteamCN/SteamCN.yaml",
        "filename": "SteamCN.yaml"
    }
]

# 内核设置 (依然推荐 v1.17 避坑，但核心改动是下面的路径处理)
MIHOMO_URL = "https://github.com/MetaCubeX/mihomo/releases/download/v1.17.0/mihomo-linux-amd64-v1.17.0.gz"
BINARY_PATH = os.path.join(SCRIPT_DIR, "mihomo")

def setup_environment():
    # 强制清理旧内核，防止残留
    if os.path.exists(BINARY_PATH):
        try:
            os.remove(BINARY_PATH)
        except:
            pass

    print(f"⬇️  下载内核至绝对路径: {BINARY_PATH}")
    try:
        with requests.get(MIHOMO_URL, stream=True, timeout=30) as r:
            r.raise_for_status()
            with open(f"{BINARY_PATH}.gz", "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        
        with gzip.open(f"{BINARY_PATH}.gz", "rb") as f_in:
            with open(BINARY_PATH, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        # 赋予执行权限
        st = os.stat(BINARY_PATH)
        os.chmod(BINARY_PATH, st.st_mode | stat.S_IEXEC)
        
        # 测试内核是否响应 (打印版本)
        print("⚙️  内核版本测试:")
        subprocess.run([BINARY_PATH, "-v"], check=True)
        
    except Exception as e:
        print(f"❌ 环境准备失败: {e}")
        exit(1)

def fetch_rules():
    print("🌍 下载规则...")
    for rule in UPSTREAM_RULES:
        try:
            resp = requests.get(rule["url"], timeout=15)
            if resp.status_code == 200:
                # 同样使用绝对路径保存
                save_path = os.path.join(ROOT_DIR, rule["filename"])
                with open(save_path, "wb") as f:
                    f.write(resp.content)
            else:
                print(f"   ⚠️ 下载失败 {resp.status_code}: {rule['filename']}")
        except Exception as e:
            print(f"   ⚠️ 网络错误: {e}")

def convert_rules():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    print("🔄 开始编译 (使用绝对路径)...")
    
    # 遍历 ROOT_DIR
    for root, _, files in os.walk(ROOT_DIR):
        # 跳过输出目录和脚本目录
        if os.path.abspath(root) == os.path.abspath(OUTPUT_DIR) or os.path.abspath(root) == os.path.abspath(SCRIPT_DIR):
            continue
            
        for file in files:
            if file.lower().endswith(('.yaml', '.yml')):
                # 获取文件的绝对路径
                src_abs = os.path.join(root, file)
                dst_abs = os.path.join(OUTPUT_DIR, os.path.splitext(file)[0] + ".mrs")
                
                rule_type = "ipcidr" if "ip" in file.lower() else "classical"
                
                print(f"   ⚙️  处理: {file} -> .mrs ... ", end="", flush=True)
                
                try:
                    # 使用 shell=True 确保参数被当作完整的命令行字符串解析
                    # 这能解决某些环境参数传递失效的问题
                    cmd = f"'{BINARY_PATH}' convert-ruleset {rule_type} '{src_abs}' '{dst_abs}'"
                    
                    subprocess.run(
                        cmd,
                        shell=True,  # 关键修改：用 Shell 模式执行
                        check=True,
                        stdout=subprocess.DEVNULL,
                        timeout=30
                    )
                    print("✅")
                except subprocess.TimeoutExpired:
                    print("❌ 超时")
                except subprocess.CalledProcessError:
                    print("❌ 失败")

if __name__ == "__main__":
    setup_environment()
    fetch_rules()
    convert_rules()
    
    # 清理
    if os.path.exists(f"{BINARY_PATH}.gz"): os.remove(f"{BINARY_PATH}.gz")
    if os.path.exists(BINARY_PATH): os.remove(BINARY_PATH)
    print("🎉 全部完成")
