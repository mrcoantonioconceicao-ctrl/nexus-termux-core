import sys
from pathlib import Path

def generate_ci(root_dir: str = "."):
    root = Path(root_dir)
    wf_dir = root / ".github" / "workflows"
    wf_dir.mkdir(parents=True, exist_ok=True)
    
    ci_content = """name: Nexus Termux Core CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Run Workspace Pipeline
        run: ./run.sh
      - name: Verify Git Integrity
        run: git status --porcelain
"""
    wf_file = wf_dir / "pipeline.yml"
    wf_file.write_text(ci_content)
    print(f"[CI GEN] GitHub Actions workflow generated at: {wf_file}")

if __name__ == "__main__":
    generate_ci(sys.argv[1] if len(sys.argv) > 1 else ".")
