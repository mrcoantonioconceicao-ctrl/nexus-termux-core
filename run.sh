#!/usr/bin/env bash
set -euo pipefail

export SANDBOX_DIR="$(realpath ./sandbox/target_workspace)"
export CORE_DIR="$(realpath ./core)"
export PYTHONPATH="$CORE_DIR"

echo "[*] Nexus Termux Core - Full Pipeline (Forge + Audit + SDK + Tests)"
echo "[*] Sandbox: $SANDBOX_DIR"

SPEC_FILE="./specs/nexus_vault_init.json"

if [ ! -f "$SPEC_FILE" ]; then
    echo "[!] Spec file not found: $SPEC_FILE"
    exit 1
fi

# 1. Forge
python3 "$CORE_DIR/forge.py" "$SPEC_FILE"

# 2. Audit Gate
PROGRAM_NAME=$(python3 -c "import json; data = json.load(open('$SPEC_FILE')); print(data['program'])")
python3 "$CORE_DIR/audit_gate.py" "$PROGRAM_NAME"

# 3. SDK Gen
python3 "$CORE_DIR/sdk_gen.py" "$SPEC_FILE"

# 4. Test Gen
python3 "$CORE_DIR/tests_gen.py" "$SPEC_FILE"

echo "[+] Full CI/CD local pipeline execution clean and verified."

