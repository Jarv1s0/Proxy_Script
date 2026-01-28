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

# 远程规则
UPSTREAM_RULES = [
    {
        "url": "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/SteamCN/SteamCN.yaml",
        "filename": "SteamCN.yaml"
    }
]

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
                
                # --- 核心修复 ---
                # 只有文件名明确包含 'ip' 才用 ipcidr
                # 其他所有情况（包括 SteamCN）都强制使用 classical (混合模式)
                # classical 模式可以同时处理域名和IP，不会卡死
                if "ip" in file_name_no_ext.lower():
                    rule_type = "ipcidr"
                else:
                    rule_type = "classical"  # <--- 这里改成了 classical
                
                print(f"🔄 编译中 [{rule_type}]: {file} ...", end="", flush=True)
                
                try:
                    # 增加30秒超时限制，防止卡死
                    subprocess.run(
                        [BINARY_NAME, "convert-ruleset", rule_type, src_path, dst_path],
                        check=True,
                        capture_output=True,
                        timeout=30 
                    )
                    print(" ✅ 成功")
                except subprocess.TimeoutExpired:
                    print(" ❌ 超时 (跳过)")
                except subprocess.CalledProcessError:
                    print(" ❌ 失败 (格式错误)")

if __name__ == "__main__":
    download_mihomo()
    fetch_upstream_rules()
    convert_rules()
    if os.path.exists(f"{BINARY_NAME}.gz"): os.remove(f"{BINARY_NAME}.gz")
    if os.path.exists(BINARY_NAME): os.remove(BINARY_NAME)
    print("🎉 所有任务完成")
