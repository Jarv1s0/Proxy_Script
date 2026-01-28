import os
import subprocess
import requests
import gzip
import shutil
import stat

# --- 路径配置 (基于仓库根目录) ---
# GitHub Actions 默认在仓库根目录运行，所以直接用相对路径最稳
BASE_DIR = "Clash"
OUTPUT_DIR = os.path.join(BASE_DIR, "rule-set")
SCRIPT_DIR = os.path.join(BASE_DIR, "scripts")
BINARY_PATH = os.path.join(SCRIPT_DIR, "mihomo")

UPSTREAM_RULES = [
    {
        "url": "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/SteamCN/SteamCN.yaml",
        "filename": "SteamCN.yaml"
    }
]

# 依然强制使用 v1.17.0，因为它在无头环境(CI)中最稳定
MIHOMO_URL = "https://github.com/MetaCubeX/mihomo/releases/download/v1.17.0/mihomo-linux-amd64-v1.17.0.gz"

def setup_mihomo():
    print(f"⬇️  准备内核: {BINARY_PATH}")
    if os.path.exists(BINARY_PATH):
        try: os.remove(BINARY_PATH) # 清理旧文件
        except: pass

    try:
        with requests.get(MIHOMO_URL, stream=True, timeout=30) as r:
            r.raise_for_status()
            with open(f"{BINARY_PATH}.gz", "wb") as f:
                for chunk in r.iter_content(chunk_size=8192): f.write(chunk)
        
        with gzip.open(f"{BINARY_PATH}.gz", "rb") as f_in:
            with open(BINARY_PATH, "wb") as f_out: shutil.copyfileobj(f_in, f_out)
        
        st = os.stat(BINARY_PATH)
        os.chmod(BINARY_PATH, st.st_mode | stat.S_IEXEC)
        print("✅ 内核就绪")
    except Exception as e:
        print(f"❌ 内核安装失败: {e}")
        exit(1)

def download_rules():
    print("🌍 下载规则...")
    for rule in UPSTREAM_RULES:
        save_path = os.path.join(BASE_DIR, rule["filename"])
        try:
            r = requests.get(rule["url"], timeout=15)
            r.raise_for_status()
            with open(save_path, "wb") as f: f.write(r.content)
            print(f"   -> 已保存: {save_path}")
        except Exception as e:
            print(f"❌ 规则下载失败: {e}")
            exit(1) # 下载失败直接停止

def compile_rules():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    print("🔄 开始编译...")
    success_count = 0
    
    # 只扫描 Clash 目录下的 yaml 文件
    for file in os.listdir(BASE_DIR):
        if file.lower().endswith(('.yaml', '.yml')):
            src = os.path.join(BASE_DIR, file)
            dst = os.path.join(OUTPUT_DIR, os.path.splitext(file)[0] + ".mrs")
            
            rule_type = "ipcidr" if "ip" in file.lower() else "classical"
            
            print(f"   🔨 正在编译: {file} -> .mrs ... ", end="")
            
            # 使用列表传参，避免 shell=True 的路径转义问题
            cmd = [os.path.abspath(BINARY_PATH), "convert-ruleset", rule_type, os.path.abspath(src), os.path.abspath(dst)]
            
            try:
                subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=20)
                if os.path.exists(dst):
                    print("✅")
                    success_count += 1
                else:
                    print("❌ (文件未生成)")
                    exit(1)
            except subprocess.CalledProcessError as e:
                print(f"\n❌ 编译错误: {e.stderr.decode().strip()}")
                exit(1) # 只要有一个失败，任务就失败
            except Exception as e:
                print(f"\n❌ 异常: {e}")
                exit(1)

    if success_count == 0:
        print("❌ 未找到任何 YAML 文件进行编译！")
        exit(1)

if __name__ == "__main__":
    setup_mihomo()
    download_rules()
    compile_rules()
    print("🎉 脚本执行完毕，文件已生成。")
