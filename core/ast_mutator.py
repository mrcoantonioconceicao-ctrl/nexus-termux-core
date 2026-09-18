import json
import sys
from pathlib import Path
from safety_guard import validate_safe_path

def apply_mutation(ir_path: Path):
    with ir_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    target_file = validate_safe_path(data["target_file"])
    target_file.parent.mkdir(parents=True, exist_ok=True)
    if not target_file.exists():
        target_file.touch()

    content = target_file.read_text(encoding="utf-8") if target_file.stat().st_size > 0 else "// -- initial nexus state --\n"

    for mut in data.get("mutations", []):
        op = mut["op"]
        symbol = mut["symbol"]
        payload = mut["payload"]

        if op == "insert_instruction":
            content += f"\n// [nexus-inserted: {symbol}]\npub fn {symbol}() -> Result<()> {{ Ok(()) }}\n"
        elif op == "update_state":
            content += f"\n// [nexus-state: {symbol}] -> {payload}\n"

    target_file.write_text(content, encoding="utf-8")
    print(f"[+] Mutated safely: {target_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 ast_mutator.py <path-to-ir.json>")
    apply_mutation(Path(sys.argv[1]))

