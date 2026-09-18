import json
import sys
from pathlib import Path
from safety_guard import validate_safe_path

def generate_sdk(spec_path: Path):
    with spec_path.open("r", encoding="utf-8") as f:
        spec = json.load(f)

    program_name = spec["program"]
    program_id = spec.get("program_id", "11111111111111111111111111111111")
    
    # Corrige path relativo correto dentro da sandbox
    sdk_dir = validate_safe_path(f"sdk/{program_name}")
    sdk_dir.mkdir(parents=True, exist_ok=True)
    
    methods_code = ""
    for inst in spec.get("instructions", []):
        name = inst["name"]
        methods_code += f"""
    async {name}(params: any): Promise<string> {{
        return await this.program.methods
            .{name}(params)
            .rpc();
    }}
"""

    class_name = "".join(word.capitalize() for word in program_name.split("_"))
    sdk_content = f"""import {{ Program }} from '@coral-xyz/anchor';
import {{ PublicKey }} from '@solana/web3.js';

export const PROGRAM_ID = new PublicKey('{program_id}');

export class {class_name}Client {{
    program: Program<any>;

    constructor(program: Program<any>) {{
        this.program = program;
    }}
{methods_code}}}
"""

    out_file = sdk_dir / "client.ts"
    out_file.write_text(sdk_content, encoding="utf-8")
    print(f"[SDK GEN] Client stub generated at: {out_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 sdk_gen.py <path-to-spec.json>")
    generate_sdk(Path(sys.argv))

