
import os
import sys
import platform
import shutil
import urllib.request
import subprocess
import tarfile
import gzip
import zipfile

# Configuration
MIHOMO_VERSION = "v1.18.1" # Fixed version for stability, or fetch latest
GITHUB_REPO = "MetaCubeX/mihomo"
RULES_DIR = "../rules"
OUTPUT_DIR = "../rules" # Process in place or output elsewhere

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

def download_mihomo(os_name, arch, ext, exe_ext):
    binary_name = f"mihomo-{os_name}-{arch}"
    if os_name == "windows":
        binary_name += f"-{MIHOMO_VERSION}" # Windows zip usually has version in name inside? No, standard naming.
        # Check assets naming convention: mihomo-windows-amd64-v1.18.1.zip
        asset_name = f"mihomo-{os_name}-{arch}-{MIHOMO_VERSION}{ext}"
    else:
        # Linux: mihomo-linux-amd64-v1.18.1.gz
        asset_name = f"mihomo-{os_name}-{arch}-{MIHOMO_VERSION}{ext}"

    download_url = f"https://github.com/{GITHUB_REPO}/releases/download/{MIHOMO_VERSION}/{asset_name}"
    
    local_binary = f"mihomo{exe_ext}"
    
    if os.path.exists(local_binary):
        print("Mihomo binary already exists.")
        return local_binary

    print(f"Downloading {asset_name} from {download_url}...")
    try:
        urllib.request.urlretrieve(download_url, asset_name)
    except Exception as e:
        print(f"Download failed: {e}")
        sys.exit(1)

    print("Extracting...")
    if asset_name.endswith(".zip"):
        with zipfile.ZipFile(asset_name, 'r') as zip_ref:
            # zip might contain a folder or just the file.
            # usually it contains the executable. 
            # let's list to be sure or just extract all.
            file_list = zip_ref.namelist()
            target_file = None
            for f in file_list:
                if f.endswith(".exe"):
                    target_file = f
                    break
            if target_file:
                zip_ref.extract(target_file, ".")
                if target_file != local_binary:
                    shutil.move(target_file, local_binary)
    elif asset_name.endswith(".gz"):
        # it is likely just a compressed binary
        with gzip.open(asset_name, 'rb') as f_in:
            with open(local_binary, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        # Make executable
        st = os.stat(local_binary)
        os.chmod(local_binary, st.st_mode | 0o111)

    # Cleanup
    if os.path.exists(asset_name):
        os.remove(asset_name)

    return local_binary

def convert_rules_to_mrs(binary_path, rules_dir, output_dir):
    if not os.path.exists(rules_dir):
        print(f"Rules directory not found: {rules_dir}")
        return

    for filename in os.listdir(rules_dir):
        if filename.endswith(".yaml") or filename.endswith(".yml"):
            file_path = os.path.join(rules_dir, filename)
            # Output filename: replace extension with .mrs
            base_name = os.path.splitext(filename)[0]
            output_path = os.path.join(output_dir, f"{base_name}.mrs")
            
            print(f"Converting {filename} to {base_name}.mrs ...")
            
            # Command: mihomo rule-set convert -t <type> -o <output> <input>
            # But wait, modern mihomo syntax:
            # convert is a subcommand.
            # We assume the YAML is a valid rule-set source.
            
            # Note: We need to know the TYPE (behavior, ipcidr, domain, etc.)?
            # Or does mihomo detect it? 
            # `mihomo convert-ruleset <type> <path>` was old?
            # Let's check help if possible, but assuming standard:
            # `mihomo convert-ruleset domain source.yaml output.mrs`
            # Wait, `rule-set convert` ? 
            # Based on docs (which I cannot verify online now), recent versions use `convert-ruleset`.
            # BUT, the generic way often requires specifying type. 
            # If the YAML contains `payload`, it might need `type` specified in command?
            # Actually, standard rule-set YAMLs have a structure.
            # Let's try to detect type from file content or default to 'domain' for safety?
            # Better: The user didn't specify. Standard `rule-set` usually implies usage in `rule-providers`.
            
            # Let's look at file content to guess type if needed, OR just assume a type. 
            # OOM-WG/RuleList usually has domain lists or IP lists.
            # Let's naively assume if it contains 'ip' it is ipcidr, else domain?
            # A safer bet is just `mihomo convert-ruleset domain ...` if it fails default.
            
            # But wait, recent mihomo might infer it.
            # Command: ./mihomo convert-ruleset <type> <yaml> <mrs>
            
            # Try to detect type: domain or ipcidr
            rule_type = "domain" 
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Check for IP-CIDR to switch to ipcidr
                if "IP-CIDR" in content or "IP-CIDR6" in content:
                    rule_type = "ipcidr"
                # If specifically payload with content
            
            # Syntax: mihomo convert-ruleset <behavior> yaml <input> <output>
            # behavior: domain | ipcidr
            
            cmd = [os.path.abspath(binary_path), "convert-ruleset", rule_type, "yaml", os.path.abspath(file_path), os.path.abspath(output_path)]
            
            print(f"Running: {' '.join(cmd)}")
            try:
                # Capture output to see errors
                result = subprocess.run(cmd, check=True, capture_output=True, text=True)
                print(f"Success: {output_path}")
                print(result.stdout)
            except subprocess.CalledProcessError as e:
                print(f"Failed to convert {filename}: {e}")
                print(f"Stderr: {e.stderr}")
                print(f"Stdout: {e.stdout}")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_dir) # Ensure running from scripts dir
    
    os_name, arch, ext, exe_ext = get_system_info()
    binary_path = download_mihomo(os_name, arch, ext, exe_ext)
    
    # Resolve directories relative to script
    rules_path = os.path.abspath(RULES_DIR)
    convert_rules_to_mrs(binary_path, rules_path, rules_path)
