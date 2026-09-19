import sys
from pathlib import Path

def generate_sdk_index(workspace_dir: str):
    ws = Path(workspace_dir)
    sdk_dir = ws / "sdk"
    if not sdk_dir.exists():
        print(f"[SDK INDEX] SDK directory not found at {sdk_dir}")
        return
    
    exports = []
    for prog_dir in sorted(sdk_dir.iterdir()):
        if prog_dir.is_dir() and (prog_dir / "client.ts").exists():
            exports.append(f"export * from './{prog_dir.name}/client';")
    
    index_file = sdk_dir / "index.ts"
    index_file.write_text("\n".join(exports) + "\n")
    print(f"[SDK INDEX] Unified index generated at: {index_file} with {len(exports)} modules.")

if __name__ == "__main__":
    generate_sdk_index(sys.argv[1] if len(sys.argv) > 1 else "sandbox/target_workspace")
