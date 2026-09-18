import os
from pathlib import Path

def get_sandbox_dir() -> Path:
    env_sandbox = os.getenv("SANDBOX_DIR")
    if env_sandbox:
        return Path(env_sandbox).resolve()
    return (Path(__file__).resolve().parent.parent / "sandbox" / "target_workspace").resolve()

def validate_safe_path(target_file: str) -> Path:
    sandbox = get_sandbox_dir()
    abs_path = (sandbox / target_file).resolve()
    
    if not str(abs_path).startswith(str(sandbox)):
        raise PermissionError(f"Security Violation: Path traversal detected -> {target_file}")
    return abs_path

