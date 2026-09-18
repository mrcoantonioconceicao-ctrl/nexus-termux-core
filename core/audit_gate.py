import sys
from pathlib import Path
from safety_guard import validate_safe_path

def audit_bump_bindings(program_name: str):
    prog_dir = validate_safe_path(f"programs/{program_name}/src")
    context_file = prog_dir / "context.rs"
    lib_file = prog_dir / "lib.rs"
    
    if not context_file.exists() or not lib_file.exists():
        raise FileNotFoundError("Context or Lib file missing for audit.")
        
    ctx_content = context_file.read_text(encoding="utf-8")
    lib_content = lib_file.read_text(encoding="utf-8")
    
    if "init" in ctx_content and "bump" not in lib_content:
        print("[AUDIT WARNING] 'init' detected in context.rs, but no bump reference found in lib.rs!")
        sys.exit(1)
            
    print(f"[AUDIT PASS] Bump binding check passed for program '{program_name}'.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 audit_gate.py <program_name>")
    audit_bump_bindings(sys.argv[1])

