import subprocess
import sys
from pathlib import Path

def run_cmd(cmd: list[str]):
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[ERROR] Command failed: {' '.join(cmd)}\n{res.stderr}")
        sys.exit(1)
    print(res.stdout, end="")

def release_to_github(remote_url: str, branch: str = "main"):
    print(f"[*] Preparing release sync for remote: {remote_url}")
    
    # Remove origin anterior se existir
    subprocess.run(["git", "remote", "remove", "origin"], capture_output=True)
    
    # Adiciona novo origin
    run_cmd(["git", "remote", "add", "origin", remote_url])
    
    # Push com upstream
    print(f"[*] Pushing branch '{branch}' to GitHub...")
    run_cmd(["git", "push", "-u", "origin", branch])
    print("[+] Repository pushed successfully to GitHub!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 release.py <git-remote-url>")
    release_to_github(sys.argv[1])

