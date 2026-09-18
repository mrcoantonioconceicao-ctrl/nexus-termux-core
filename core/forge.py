import json
import sys
from pathlib import Path
from safety_guard import validate_safe_path

def forge_instruction(spec_path: Path):
    with spec_path.open("r", encoding="utf-8") as f:
        spec = json.load(f)

    program_name = spec["program"]
    target_rel = f"programs/{program_name}/src/lib.rs"
    target_file = validate_safe_path(target_rel)
    
    target_file.parent.mkdir(parents=True, exist_ok=True)
    if not target_file.exists():
        initial_boilerplate = f"""use anchor_lang::prelude::*;

declare_id!{{"{spec.get('program_id', '11111111111111111111111111111111')}"}}

#[program]
pub mod {program_name} {{
    use super::*;
}}
"""
        target_file.write_text(initial_boilerplate, encoding="utf-8")

    content = target_file.read_text(encoding="utf-8")

    for inst in spec.get("instructions", []):
        name = inst["name"]
        accounts_struct = inst["accounts_struct"]
        logic_comment = inst.get("logic", "Ok(())")
        
        snippet = f"""
    pub fn {name}(ctx: Context<{accounts_struct}>) -> Result<()> {{
        // [nexus-forged-logic]: {logic_comment}
        msg!("Executing {name}");
        Ok(())
    }}
"""
        if f"fn {name}(" not in content:
            idx = content.rfind("}")
            if idx != -1:
                content = content[:idx] + snippet + "\n}\n"

    target_file.write_text(content, encoding="utf-8")
    print(f"[+] Forge completed for program '{program_name}' on file: {target_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 forge.py <path-to-spec.json>")
    forge_instruction(Path(sys.argv[1]))

