import json
import sys
from pathlib import Path
from safety_guard import validate_safe_path

def generate_tests(spec_path: Path):
    with spec_path.open("r", encoding="utf-8") as f:
        spec = json.load(f)

    program_name = spec["program"]
    class_name = "".join(word.capitalize() for word in program_name.split("_"))
    
    test_dir = validate_safe_path("tests")
    test_dir.mkdir(parents=True, exist_ok=True)
    
    calls = ""
    for inst in spec.get("instructions", []):
        name = inst["name"]
        calls += f"""    it("{name} instruction", async () => {{
        const tx = await client.{name}({{}});
        console.log("{name} tx:", tx);
    }});
"""

    test_content = f"""import * as anchor from '@coral-xyz/anchor';
import {{ {class_name}Client }} from '../sdk/{program_name}/client';

describe('{program_name}', () => {{
    const provider = anchor.AnchorProvider.env();
    anchor.setProvider(provider);
    
    const mockProgram = {{ methods: {{}} }} as any;
    const client = new {class_name}Client(mockProgram);

{calls}}});
"""

    out_file = test_dir / f"{program_name}.ts"
    out_file.write_text(test_content, encoding="utf-8")
    print(f"[TEST GEN] Anchor test harness generated at: {out_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 tests_gen.py <path-to-spec.json>")
    generate_tests(Path(sys.argv[1]))

