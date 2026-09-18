import json
import sys
from pathlib import Path
from safety_guard import validate_safe_path

def forge_instruction(spec_path: Path):
    with spec_path.open("r", encoding="utf-8") as f:
        spec = json.load(f)

    program_name = spec["program"]
    program_id = spec.get("program_id", "11111111111111111111111111111111")
    base_prog_dir = validate_safe_path(f"programs/{program_name}/src")
    base_prog_dir.mkdir(parents=True, exist_ok=True)

    # 1. Gera state.rs
    state_structs = spec.get("state_structs", [])
    state_code = "use anchor_lang::prelude::*;\n\n"
    for st in state_structs:
        s_name = st["name"]
        fields = st.get("fields", [])
        fields_str = "\n    ".join([f"pub {f}," for f in fields])
        state_code += f"""
#[account]
pub struct {s_name} {{
    {fields_str}
}}
"""
    (base_prog_dir / "state.rs").write_text(state_code, encoding="utf-8")

    # 2. Gera context.rs com suporte a PDAs e space dinâmico/estático
    contexts_def = spec.get("contexts", {})
    accounts_code = "use anchor_lang::prelude::*;\nuse super::state::*;\n\n"
    
    seen_accs = set()
    init_accounts_map = {} # acc_name -> field_name
    for inst in spec.get("instructions", []):
        acc_name = inst["accounts_struct"]
        if acc_name not in seen_accs:
            seen_accs.add(acc_name)
            ctx_config = contexts_def.get(acc_name, {})
            acc_fields_code = """    #[account(mut)]
    pub signer: Signer<'info>,
    pub system_program: Program<'info, System>,"""
            
            custom_accs = ctx_config.get("accounts", [])
            for ca in custom_accs:
                c_name = ca["name"]
                c_type = ca["type"]
                c_init = ca.get("init", False)
                if c_init:
                    init_accounts_map[acc_name] = c_name
                    payer = ca.get("payer", "signer")
                    space = ca.get("space", 64)
                    seeds = ca.get("seeds", [])
                    seeds_str = ", ".join(seeds)
                    acc_fields_code += f"""
    #[account(
        init,
        payer = {payer},
        space = {space},
        seeds = [{seeds_str}],
        bump
    )]
    pub {c_name}: Account<'info, {c_type}>,"""
                else:
                    acc_fields_code += f"""
    #[account(mut)]
    pub {c_name}: Account<'info, {c_type}>,"""

            accounts_code += f"""
#[derive(Accounts)]
pub struct {acc_name}<'info> {{
{acc_fields_code}
}}
"""
    (base_prog_dir / "context.rs").write_text(accounts_code, encoding="utf-8")

    # 3. Gera lib.rs com injeção automática de bump binding se init presente
    instructions_code = ""
    for inst in spec.get("instructions", []):
        name = inst["name"]
        accounts_struct = inst["accounts_struct"]
        custom_logic = inst.get("logic", "Ok(())")
        
        bump_inject = ""
        if accounts_struct in init_accounts_map:
            acc_field = init_accounts_map[accounts_struct]
            bump_inject = f"\n    ctx.accounts.{acc_field}.bump = ctx.bumps.{acc_field};"

        instructions_code += f"""
    pub fn {name}(ctx: Context<{accounts_struct}>) -> Result<()> {{
        {custom_logic}{bump_inject}
        Ok(())
    }}
"""

    full_source = f"""use anchor_lang::prelude::*;

pub mod state;
pub mod context;
use state::*;
use context::*;

declare_id!("{program_id}");

#[program]
pub mod {program_name} {{
    use super::*;
{instructions_code}}}
"""

    (base_prog_dir / "lib.rs").write_text(full_source, encoding="utf-8")
    print(f"[+] Full PDA-aware nexus module forged for '{program_name}' in {base_prog_dir}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 forge.py <path-to-spec.json>")
    forge_instruction(Path(sys.argv[1]))

