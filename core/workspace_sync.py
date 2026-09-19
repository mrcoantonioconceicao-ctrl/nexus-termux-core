import sys
from pathlib import Path

def sync_workspace(workspace_dir: str):
    ws = Path(workspace_dir)
    programs_dir = ws / "programs"
    toml_path = ws / "Anchor.toml"
    
    prog_names = [p.name for p in programs_dir.iterdir() if p.is_dir()]
    print(f"[WORKSPACE] Discovered programs: {prog_names}")
    
    # Generate unified Anchor.toml workspace config
    toml_content = f"""[toolchain]
anchor_version = "0.29.0"

[features]
resolution = "2"
skip-lint = false

[workspace]
members = [
"""
    for name in prog_names:
        toml_content += f'    "programs/{name}",\n'
    toml_content += "]\n\n[registry]\nurl = \"https://api.apr.dev\"\n\n[provider]\ncluster = \"localnet\"\nwallet = \"~/.config/solana/id.json\"\n"
    
    if programs_dir.exists():
        toml_path.write_text(toml_content)
        print(f"[WORKSPACE] Synced unified Anchor.toml with {len(prog_names)} programs.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        sync_workspace(sys.argv[1])
