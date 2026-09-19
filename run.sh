#!/bin/bash
set -e

SPECS=("./specs/nexus_vault_init.json" "./specs/nexus_staking_init.json")
WORKSPACE="sandbox/target_workspace"

echo "[*] Nexus Termux Core - Multi-Program Workspace Pipeline"
mkdir -p "$WORKSPACE/programs" "$WORKSPACE/sdk" "$WORKSPACE/tests"

for spec in "${SPECS[@]}"; do
    if [ -f "$spec" ]; then
        echo "[*] Processing spec: $spec"
        python3 core/forge.py "$spec"
        python3 core/sdk_gen.py "$spec"
        python3 core/tests_gen.py "$spec"
    fi
done

# Audit Gate on whole workspace
python3 core/audit_gate.py "$WORKSPACE"

# Multi-program workspace sync
python3 core/workspace_sync.py "$WORKSPACE"

echo "[+] Multi-program workspace pipeline execution clean and verified."
