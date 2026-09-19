import json
import sys
from pathlib import Path

def generate_cpi_helpers(spec_path: Path):
    with open(spec_path, "r") as f:
        spec = json.load(f)
    
    prog_name = spec["program"]
    cpi_targets = spec.get("cpi", [])
    out_dir = Path("sandbox/target_workspace/programs") / prog_name / "src"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    if not cpi_targets:
        cpi_file = out_dir / "cpi.rs"
        if cpi_file.exists():
            cpi_file.unlink()
        return

    cpi_code = "use anchor_lang::prelude::*;\n\n"
    for target in cpi_targets:
        target_prog = target["program"]
        fn_name = target["instruction"]
        mod_fn = f"cpi_{target_prog}_{fn_name}".lower()
        cpi_code += f"// Auto-generated cross-program invocation stub targeting {target_prog}::{fn_name}\n"
        cpi_code += f"pub fn {mod_fn}<'info>(target_program: &AccountInfo<'info>, accounts: &[AccountInfo<'info>], data: &[u8]) -> Result<()> " + "{\n"
        cpi_code += "    let ix = anchor_lang::solana_program::instruction::Instruction {\n"
        cpi_code += "        program_id: *target_program.key,\n"
        cpi_code += "        accounts: vec![],\n"
        cpi_code += "        data: data.to_vec(),\n"
        cpi_code += "    };\n"
        cpi_code += "    anchor_lang::solana_program::program::invoke(&ix, accounts)\n"
        cpi_code += "}\n\n"
    
    (out_dir / "cpi.rs").write_text(cpi_code)
    print(f"[CPI GEN] Generated cpi.rs helper for '{prog_name}' targeting {len(cpi_targets)} programs.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        generate_cpi_helpers(Path(sys.argv[1]))
