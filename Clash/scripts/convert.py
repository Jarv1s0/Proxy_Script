import os
import subprocess
import requests
import gzip
import shutil
import stat

# --- 配置区域 ---
SOURCE_DIR = "Clash"              # 本地规则目录
OUTPUT_DIR = "Clash/rule-set"     # 编译输出目录
SCRIPT_DIR = "Clash/scripts"      # 脚本所在目录

# 定义需要自动下载的远程规则 (你可以随时在这里添加更多)
UPSTREAM_RULES = [
    {
        "url": "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/SteamCN/SteamCN.yaml",
        "filename": "SteamCN.yaml"
    },
    # 示例：你还可以添加其他的，比如：
    # { "url": "...", "filename": "Google.yaml" }
]

# Mihomo 内核下载地址
MIHOMO_URL = "https://github.com/MetaCubeX/mihomo/releases/download/v1.18.1/mihomo-linux-amd64-v1.18.1.gz"
BINARY_NAME = os.path.join(SCRIPT_DIR, "mihomo")
# ----------------

def download_mihomo():
    if os.path.exists(BINARY_NAME):
        return
    print(f"⬇️  正在下载 Mihomo 内核...")
    try:
        response = requests.get(MIHOMO_URL, stream=True, timeout=30)
        with open(f"{BINARY_NAME}.gz", "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print("📦 解压内核...")
        with gzip.open(f"{BINARY_NAME}.gz", "rb") as f_in:
            with open(BINARY_NAME, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
        st = os.stat(BINARY_NAME)
        os.chmod(BINARY_NAME, st.st_mode | stat.S_IEXEC)
    except Exception as e:
        print(f"❌ 内核准备失败: {e}")
        exit(1)

def fetch_upstream_rules():
    print("🌍 正在拉取远程规则...")
    for rule in UPSTREAM_RULES:
        url = rule["url"]
        path = os.path.join(SOURCE_DIR, rule["filename"])
        try:
            print(f"   -> 下载: {rule['filename']}")
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            with open(path, "wb") as f:
                f.write(resp.content)
        except Exception as e:
            print(f"   ⚠️ 下载失败 {rule['filename']}: {e}")

def convert_rules():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # 遍历目录 (包括刚刚下载的文件)
    for root, _, files in os.walk(SOURCE_DIR):
        if "rule-set" in root or "scripts" in root:
            continue
        for file in files:
            if file.lower().endswith(('.yaml', '.yml')):
                src_path = os.path.join(root, file)
                file_name_no_ext = os.path.splitext(file)[0]
                dst_path = os.path.join(OUTPUT_DIR, f"{file_name_no_ext}.mrs")
                
                # 智能识别类型
                rule_type = "ipcidr" if "ip" in file_name_no_ext.lower() else "domain"
                
                print(f"🔄 编译中 [{rule_type}]: {file} -> .mrs")
                try:
                    subprocess.run(
                        [BINARY_NAME, "convert-ruleset", rule_type, src_path, dst_path],
                        check=True,
                        stdout=subprocess.DEVNULL
                    )
                except subprocess.CalledProcessError:
                    print(f"❌ 编译失败: {file}")

if __name__ == "__main__":
    download_mihomo()
    fetch_upstream_rules() # 新增步骤：先下载远程文件
    convert_rules()
    
    # 清理内核文件
    if os.path.exists(f"{BINARY_NAME}.gz"): os.remove(f"{BINARY_NAME}.gz")
    if os.path.exists(BINARY_NAME): os.remove(BINARY_NAME)
    print("🎉 所有任务完成")
