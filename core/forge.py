import json
import sys
from pathlib import Path
from safety_guard import validate_safe_path

def forge_instruction(spec_path: Path):
    with spec_path.open("r", encoding="utf-8") as f:
        spec = json.load(f)

    program_name = spec["program"]
    program_id = spec.get("program_id", "11111111111111111111111111111111")
    target_rel = f"programs/{program_name}/src/lib.rs"
    target_file = validate_safe_path(target_rel)
    
    target_file.parent.mkdir(parents=True, exist_ok=True)

    instructions_code = ""
    for inst in spec.get("instructions", []):
        name = inst["name"]
        accounts_struct = inst["accounts_struct"]
        logic_comment = inst.get("logic", "Ok(())")
        
        instructions_code += f"""
    pub fn {name}(ctx: Context<{accounts_struct}>) -> Result<()> {{
        // [nexus-forged-logic]: {logic_comment}
        msg!("Executing {name}");
        Ok(())
    }}
"""

    full_source = f"""use anchor_lang::prelude::*;

declare_id!("{program_id}");

#[program]
pub mod {program_name} {{
    use super::*;
{instructions_code}}}
"""

    target_file.write_text(full_source, encoding="utf-8")
    print(f"[+] Clean forge render completed for program '{program_name}' on file: {target_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 forge.py <path-to-spec.json>")
    forge_instruction(Path(sys.argv[1]))

