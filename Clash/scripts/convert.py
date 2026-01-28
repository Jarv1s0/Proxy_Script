import os
import subprocess
import requests
import gzip
import shutil
import stat

# --- 配置 ---
SOURCE_DIR = "Clash"
OUTPUT_DIR = "Clash/rule-set"
SCRIPT_DIR = "Clash/scripts"

# 注意：这里必须是 raw.githubusercontent.com 开头的地址，不能是 github.com/blob/...
UPSTREAM_RULES = [
    {
        "url": "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/SteamCN/SteamCN.yaml",
        "filename": "SteamCN.yaml"
    }
]

MIHOMO_URL = "https://github.com/MetaCubeX/mihomo/releases/download/v1.18.1/mihomo-linux-amd64-v1.18.1.gz"
BINARY_NAME = os.path.join(SCRIPT_DIR, "mihomo")

def download_mihomo():
    if os.path.exists(BINARY_NAME): return
    print("⬇️  下载内核...")
    try:
        with requests.get(MIHOMO_URL, stream=True, timeout=30) as r:
            r.raise_for_status()
            with open(f"{BINARY_NAME}.gz", "wb") as f:
                for chunk in r.iter_content(chunk_size=8192): f.write(chunk)
        print("📦 解压内核...")
        with gzip.open(f"{BINARY_NAME}.gz", "rb") as f_in:
            with open(BINARY_NAME, "wb") as f_out: shutil.copyfileobj(f_in, f_out)
        st = os.stat(BINARY_NAME)
        os.chmod(BINARY_NAME, st.st_mode | stat.S_IEXEC)
    except Exception as e:
        print(f"❌ 内核错误: {e}")
        exit(1)

def fetch_upstream_rules():
    print("🌍 下载规则...")
    for rule in UPSTREAM_RULES:
        try:
            resp = requests.get(rule["url"], timeout=10)
            if resp.status_code != 200:
                print(f"⚠️ 下载失败 HTTP {resp.status_code}: {rule['filename']}")
                continue
            
            path = os.path.join(SOURCE_DIR, rule["filename"])
            with open(path, "wb") as f:
                f.write(resp.content)
            
            # --- 关键调试：打印文件头，检查是否下载到了 HTML ---
            print(f"🔎 检查文件内容 [{rule['filename']}]:")
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                head = f.read(200) # 只读前200个字符
                print("-" * 30)
                print(head)
                print("-" * 30)
                
                if "<!DOCTYPE html>" in head or "<html" in head:
                    print("🚨 严重错误: 下载到的是网页HTML，不是规则文件！请检查 URL。")
                    exit(1) # 直接报错停止
                    
        except Exception as e:
            print(f"⚠️ 异常: {e}")

def convert_rules():
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)

    for root, _, files in os.walk(SOURCE_DIR):
        if "rule-set" in root or "scripts" in root: continue
        for file in files:
            if file.lower().endswith(('.yaml', '.yml')):
                src = os.path.join(root, file)
                dst = os.path.join(OUTPUT_DIR, os.path.splitext(file)[0] + ".mrs")
                
                print(f"🔄 编译: {file} ... ", end="")
                
                # 强制使用 classical 模式，不抓取输出，直接打印到控制台
                try:
                    subprocess.run(
                        [BINARY_NAME, "convert-ruleset", "classical", src, dst],
                        check=True,
                        timeout=10 # 正常文件1秒都用不了，10秒足够了
                    )
                    print("✅")
                except subprocess.TimeoutExpired:
                    print("❌ 依然超时！(内核死锁)")
                except subprocess.CalledProcessError:
                    print("❌ 失败")

if __name__ == "__main__":
    download_mihomo()
    fetch_upstream_rules()
    convert_rules()
