#!/usr/bin/env bash
set -euo pipefail

export SANDBOX_DIR="$(realpath ./sandbox/target_workspace)"
export CORE_DIR="$(realpath ./core)"
export PYTHONPATH="$CORE_DIR"

echo "[*] Nexus Termux Core - First Development Pipeline"
echo "[*] Sandbox: $SANDBOX_DIR"

SPEC_FILE="./specs/nexus_vault_init.json"

if [ ! -f "$SPEC_FILE" ]; then
    echo "[!] Spec file not found: $SPEC_FILE"
    exit 1
fi

python3 "$CORE_DIR/forge.py" "$SPEC_FILE"

echo "[+] First development build applied cleanly into sandbox."

