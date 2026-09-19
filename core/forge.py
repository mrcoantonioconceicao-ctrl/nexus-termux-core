import json
import sys
from pathlib import Path

def forge_module(spec_path: Path):
    with open(spec_path, "r") as f:
        spec = json.load(f)
    
    prog_name = spec["program"]
    out_dir = Path("sandbox/target_workspace/programs") / prog_name / "src"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. State structs
    state_code = "use anchor_lang::prelude::*;\n\n"
    for st in spec.get("state_structs", []):
        state_code += f"#[account]\n#[derive(Default)]\npub struct {st['name']} {{\n"
        for field in st["fields"]:
            state_code += f"    pub {field},\n"
        state_code += "}\n\n"
    (out_dir / "state.rs").write_text(state_code)
    
    # 2. Context structs (PDA-aware simplified)
    ctx_code = "use anchor_lang::prelude::*;\nuse crate::state::*;\n\n"
    for ctx_name, ctx_data in spec.get("contexts", {}).items():
        ctx_code += f"#[derive(Accounts)]\npub struct {ctx_name}<'info> {{\n"
        for acc in ctx_data.get("accounts", []):
            if acc.get("init"):
                ctx_code += f"    #[account(init, payer = signer, space = 8 + {acc.get('space', 64)}, seeds = [b\"pool\", signer.key().as_ref()], bump)]\n"
            else:
                ctx_code += f"    #[account(mut)]\n"
            ctx_code += f"    pub {acc['name']}: Account<'info, {acc['type']}>,\n"
        ctx_code += "    #[account(mut)]\n    pub signer: Signer<'info>,\n    pub system_program: Program<'info, System>,\n}\n\n"
    (out_dir / "context.rs").write_text(ctx_code)
    
    # 3. Lib.rs with args support
    lib_code = f"use anchor_lang::prelude::*;\nmod state;\nmod context;\nuse state::*;\nuse context::*;\n\ndeclare_id!(\"{spec['program_id']}\");\n\n#[program]\npub mod {prog_name} {{\n    use super::*;\n\n"
    
    for ix in spec.get("instructions", []):
        name = ix["name"]
        acc_struct = ix["accounts_struct"]
        args_str = ", ".join(ix.get("args", []))
        sig_args = f", {args_str}" if args_str else ""
        lib_code += f"    pub fn {name}(ctx: Context<{acc_struct}>{sig_args}) -> Result<()> {{\n"
        lib_code += f"        {ix['logic']}\n"
        lib_code += f"        Ok(())\n    }\n"
    
    lib_code += "}\n"
    (out_dir / "lib.rs").write_text(lib_code)
    print(f"[+] Forged multi-file module with args support for '{prog_name}' in {out_dir}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        forge_module(Path(sys.argv[1]))

