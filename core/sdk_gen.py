import json
import sys
from pathlib import Path

def generate_strict_sdk(spec_path: Path):
    with open(spec_path, "r") as f:
        spec = json.load(f)
    
    prog_name = spec["program"]
    out_dir = Path("sandbox/target_workspace/sdk") / prog_name
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # Map rust/anchor types to TS types
    type_map = {
        "u64": "number | BN",
        "u32": "number",
        "u16": "number",
        "u8": "number",
        "i64": "number | BN",
        "i32": "number",
        "bool": "boolean",
        "Pubkey": "PublicKey",
        "string": "string"
    }
    
    ts_interfaces = ""
    methods_code = ""
    
    for ix in spec.get("instructions", []):
        method_name = ix["name"]
        args = ix.get("args", [])
        interface_name = "".join(word.capitalize() for word in method_name.split("_")) + "Params"
        
        if args:
            ts_interfaces += f"export interface {interface_name} {{\n"
            for arg in args:
                parts = [p.strip() for p in arg.split(":")]
                if len(parts) == 2:
                    field_name, rust_type = parts[0], parts[1]
                    ts_type = type_map.get(rust_type, "any")
                    ts_interfaces += f"  {field_name}: {ts_type};\n"
            ts_interfaces += "}\n\n"
            param_sig = f"params: {interface_name}"
            pass_args = ", { ...params }"
        else:
            param_sig = ""
            pass_args = ""
            
        args_payload = pass_args.lstrip(", ")
        methods_code += f"  async {method_name}({param_sig}) {{\n"
        methods_code += f"    return await this.program.methods.{method_name}({args_payload}).rpc();\n  }}\n\n"

    state_types = ""
    for st in spec.get("state_structs", []):
        st_name = st["name"]
        state_types += f"export interface {st_name} {{\n"
        for field in st["fields"]:
            parts = [p.strip() for p in field.split(":")]
            if len(parts) == 2:
                f_name, r_type = parts[0], parts[1]
                ts_type = type_map.get(r_type, "any")
                state_types += f"  {f_name}: {ts_type};\n"
        state_types += "}\n\n"

    class_name = "".join(word.capitalize() for word in prog_name.split("_")) + "Client"
    sdk_content = f"""// Strict Typed SDK for {prog_name}
import {{ Program, BN }} from '@project-serum/anchor';
import {{ PublicKey }} from '@solana/web3.js';

{ts_interfaces}
{state_types}
export class {class_name} {{
  constructor(readonly program: Program) {{}}

{methods_code}}}
"""
    
    out_file = out_dir / "client.ts"
    out_file.write_text(sdk_content)
    print(f"[STRICT SDK GEN] Strict TS client stub generated at: {out_file}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        generate_strict_sdk(Path(sys.argv[1]))
