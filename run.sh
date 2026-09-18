#!/usr/bin/env bash
set -euo pipefail

export SANDBOX_DIR="$(realpath ./sandbox/target_workspace)"
export CORE_DIR="$(realpath ./core)"
export PYTHONPATH="$CORE_DIR"

echo "[*] Nexus Termux Core Boot"
echo "[*] Sandbox: $SANDBOX_DIR"

IR_TEMP="/tmp/nexus_ir_test.json"
cat <<EOF > "$IR_TEMP"
{
  "version": "1.0",
  "target_file": "programs/nexus_vault/src/lib.rs",
  "mutations": [
    {
      "op": "insert_instruction",
      "symbol": "initialize_vault",
      "payload": "basic_init"
    }
  ]
}
EOF

python3 "$CORE_DIR/ast_mutator.py" "$IR_TEMP"
rm -f "$IR_TEMP"
echo "[+] Pipeline execution clean."

