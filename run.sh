#!/bin/bash
set -e

SPECS=("./specs/nexus_vault_init.json" "./specs/nexus_staking_init.json" "./specs/nexus_token_vault_init.json")
WORKSPACE="sandbox/target_workspace"

echo "[*] Nexus Termux Core - 3-Node Multi-Program Pipeline + CPI + SDK Agg"
mkdir -p "$WORKSPACE/programs" "$WORKSPACE/sdk" "$WORKSPACE/tests"

for spec in "${SPECS[@]}"; do
    if [ -f "$spec" ]; then
        echo "[*] Processing spec: $spec"
        python3 core/cpi_gen.py "$spec"
        python3 core/forge.py "$spec"
        python3 core/sdk_gen.py "$spec"
        python3 core/tests_gen.py "$spec"
    fi
done

# Audit Gate on whole workspace
python3 core/audit_gate.py "$WORKSPACE"

# Multi-program workspace sync
python3 core/workspace_sync.py "$WORKSPACE"

# SDK Index Aggregator
python3 core/sdk_aggregator.py "$WORKSPACE"

# CI/CD Pipeline Gen
python3 core/ci_gen.py .

echo "[+] Multi-program full pipeline + CPI + Index + CI/CD execution clean and verified."
