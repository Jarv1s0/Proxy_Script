import os
import subprocess
import requests
import gzip
import shutil
import stat

# --- 配置区域 ---
SOURCE_DIR = "Clash"              
OUTPUT_DIR = "Clash/rule-set"     
SCRIPT_DIR = "Clash/scripts"      

# 远程规则列表
UPSTREAM_RULES = [
    {
        "url": "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/SteamCN/SteamCN.yaml",
        "filename": "SteamCN.yaml"
    }
]

# 内核地址
MIHOMO_URL = "https://github.com/MetaCubeX/mihomo/releases/download/v1.18.1/mihomo-linux-amd64-v1.18.1.gz"
BINARY_NAME = os.path.join(SCRIPT_DIR, "mihomo")
# ----------------

def download_mihomo():
    if os.path.exists(BINARY_NAME):
        return
    print(f"⬇️  正在下载 Mihomo 内核...")
    try:
        with requests.get(MIHOMO_URL, stream=True, timeout=30) as r:
            r.raise_for_status()
            with open(f"{BINARY_NAME}.gz", "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        
        print("📦 解压内核...")
        with gzip.open(f"{BINARY_NAME}.gz", "rb") as f_in:
            with open(BINARY_NAME, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        st = os.stat(BINARY_NAME)
        os.chmod(BINARY_NAME, st.st_mode | stat.S_IEXEC)
        
        # 测试内核是否能运行
        version_check = subprocess.run([BINARY_NAME, "--version"], capture_output=True, text=True)
        print(f"✅ 内核就绪: {version_check.stdout.strip()}")
        
    except Exception as e:
        print(f"❌ 内核准备失败: {e}")
        exit(1)

def fetch_upstream_rules():
    print("🌍 正在拉取远程规则...")
    for rule in UPSTREAM_RULES:
        try:
            print(f"   -> 下载: {rule['filename']}")
            resp = requests.get(rule["url"], timeout=15)
            resp.raise_for_status()
            path = os.path.join(SOURCE_DIR, rule["filename"])
            with open(path, "wb") as f:
                f.write(resp.content)
        except Exception as e:
            print(f"   ⚠️ 下载失败 {rule['filename']}: {e}")

def convert_rules():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    for root, _, files in os.walk(SOURCE_DIR):
        if "rule-set" in root or "scripts" in root:
            continue
            
        for file in files:
            if file.lower().endswith(('.yaml', '.yml')):
                src_path = os.path.join(root, file)
                file_name_no_ext = os.path.splitext(file)[0]
                dst_path = os.path.join(OUTPUT_DIR, f"{file_name_no_ext}.mrs")
                
                # --- 关键修改：逻辑优化 ---
                # 如果文件名含 ip -> ipcidr
                # 其他情况默认用 classical (混合模式)，这比 domain 更安全，不容易卡死
                if "ip" in file_name_no_ext.lower():
                    rule_type = "ipcidr"
                else:
                    rule_type = "classical" 
                
                print(f"🔄
