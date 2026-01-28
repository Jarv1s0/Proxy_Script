import os
import sys
import platform
import shutil
import subprocess
import gzip
import zipfile
import time
import requests

# Configuration
MIHOMO_VERSION = "v1.18.1"
GITHUB_REPO = "MetaCubeX/mihomo"
RULES_DIR = "../rules"
OUTPUT_DIR = "../rules"

def get_system_info():
    system = platform.system().lower()
    machine = platform.machine().lower()

    if system == "windows":
        os_name = "windows"
        ext = ".zip"
        exe_ext = ".exe"
    elif system == "linux":
        os_name = "linux"
        ext = ".gz"
        exe_ext = ""
    elif system == "darwin":
        os_name = "darwin"
        ext = ".gz"
        exe_ext = ""
    else:
        print(f"Unsupported OS: {system}")
        sys.exit(1)

    if machine in ["x86_64", "amd64"]:
        arch = "amd64"
    elif machine in ["aarch64", "arm64"]:
        arch = "arm64"
    else:
        print(f"Unsupported Arch: {machine}")
        sys.exit(1)

    return os_name, arch, ext, exe_ext

def download_file(url, dest, timeout=30, retries=3):
    """Downloads a file with timeout and retries."""
    for attempt in range(retries):
        try:
            print(f"Downloading {url} (Attempt {attempt+1}/{retries})...")
            with requests.get(url, stream=True, timeout=timeout) as r:
                r.raise_for_status()
                with open(dest, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            return True
        except Exception as e:
            print(f"Download failed: {e}")
            if attempt < retries - 1:
                time.sleep(2) # Wait a bit before retry
            else:
                print("Max retries reached.")
                return False
    return False

def download_mihomo(os_name, arch, ext, exe_ext):
    binary_name = f"mihomo-{os_name}-{arch}"
    if os_name == "windows":
        asset_name = f"mihomo-{os_name}-{arch}-{MIHOMO_VERSION}{ext}"
    else:
        asset_name = f"mihomo-{os_name}-{arch}-{MIHOMO_VERSION}{ext}"

    download_url = f"https://github.com/{GITHUB_REPO}/releases/download/{MIHOMO_VERSION}/{asset_name}"
    local_binary = f"mihomo{exe_ext}"

    if os.path.exists(local_binary):
        print("Mihomo binary already exists.")
        return local_binary

    if not download_file(download_url, asset_name):
        sys.exit(1)

    print("Extracting...")
    try:
        if asset_name.endswith(".zip"):
            with zipfile.ZipFile(asset_name, 'r') as zip_ref:
                file_list = zip_ref.namelist()
                target_file = None
                for f in file_list:
                    if f.endswith(".exe"):
                        target_file = f
                        break
                if target_file:
                    zip_ref.extract(target_file, ".")
                    if target_file != local_binary:
                        if os.path.exists(local_binary):
                            os.remove(local_binary)
                        shutil.move(target_file, local_binary)
        elif asset_name.endswith(".gz"):
            with gzip.open(asset_name, 'rb') as f_in:
                with open(local_binary, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            # Make executable on Linux/Mac
            if os_name != "windows":
                st = os.stat(local_binary)
                os.chmod(local_binary, st.st_mode | 0o111)
    except Exception as e:
        print(f"Extraction failed: {e}")
        sys.exit(1)

    # Cleanup
    if os.path.exists(asset_name):
        os.remove(asset_name)

    return local_binary

def convert_rules_to_mrs(binary_path, rules_dir, output_dir):
    if not os.path.exists(rules_dir):
        print(f"Rules directory not found: {rules_dir}")
        return

    # Ensure absolute paths
    binary_path = os.path.abspath(binary_path)
    rules_dir = os.path.abspath(rules_dir)
    output_dir = os.path.abspath(output_dir)

    for filename in os.listdir(rules_dir):
        if filename.endswith(".yaml") or filename.endswith(".yml"):
            file_path = os.path.join(rules_dir, filename)
            base_name = os.path.splitext(filename)[0]
            output_path = os.path.join(output_dir, f"{base_name}.mrs")

            print(f"Converting {filename} to {base_name}.mrs ...")

            rule_type = "domain"
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if "IP-CIDR" in content or "IP-CIDR6" in content:
                        rule_type = "ipcidr"
            except Exception as e:
                print(f"Failed to read {filename}: {e}")
                continue

            cmd = [binary_path, "convert-ruleset", rule_type, "yaml", file_path, output_path]
            
            # On Windows, subprocess might need shell=True or full path handled carefully if simple invocation fails, 
            # but usually list args are safer.
            
            try:
                result = subprocess.run(cmd, check=True, capture_output=True, text=True)
                print(f"Success: {output_path}")
            except subprocess.CalledProcessError as e:
                print(f"Failed to convert {filename}:")
                print(f"Stderr: {e.stderr}")
                print(f"Stdout: {e.stdout}")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_dir)

    os_name, arch, ext, exe_ext = get_system_info()
    binary_path = download_mihomo(os_name, arch, ext, exe_ext)

    rules_path = os.path.abspath(RULES_DIR)
    convert_rules_to_mrs(binary_path, rules_path, rules_path)
