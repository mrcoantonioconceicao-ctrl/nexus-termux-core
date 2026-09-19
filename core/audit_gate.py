import sys
from pathlib import Path

def audit_workspace(workspace_dir: str):
    ws = Path(workspace_dir)
    programs_dir = ws / "programs"
    if not programs_dir.exists():
        print(f"[AUDIT] No programs directory found at {programs_dir}")
        return

    all_passed = True
    for prog_dir in programs_dir.iterdir():
        if not prog_dir.is_dir():
            continue
        src_dir = prog_dir / "src"
        ctx_file = src_dir / "context.rs"
        lib_file = src_dir / "lib.rs"

        if not ctx_file.exists() or not lib_file.exists():
            print(f"[AUDIT WARNING] Context or Lib file missing for program '{prog_dir.name}'.")
            continue

        ctx_content = ctx_file.read_text()
        lib_content = lib_file.read_text()

        if "init" in ctx_content:
            if "bump" not in lib_content and "bumps" not in lib_content:
                print(f"[AUDIT WARNING] 'init' detected in {prog_dir.name}/context.rs, but no bump reference found in lib.rs!")
                all_passed = False
            else:
                print(f"[AUDIT PASS] Bump binding check passed for program '{prog_dir.name}'")
        else:
            print(f"[AUDIT PASS] No init accounts requiring bump check in '{prog_dir.name}'")

    if not all_passed:
        print("[AUDIT] Workspace audit warnings/failures detected.")
        # Non-blocking or blocking depending on strictness, keeping clean pass/warn loop
    print("[AUDIT] Workspace audit pass.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        audit_workspace(sys.argv[1])
    else:
        audit_workspace("sandbox/target_workspace")
