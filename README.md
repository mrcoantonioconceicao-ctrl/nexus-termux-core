# Nexus Termux Core (`nexus-termux-core`)

Deterministic local CI/CD, multi-program Anchor scaffolding, strict TypeScript client generation, and security audit pipeline engineered specifically for **Termux / mobile-first Solana developer workflows** without relying on heavy native Anchor CLI toolchains.

---

## 🏛️ Architecture & Pipeline Flow

```
specs/*.json  --> [core/cpi_gen.py]      --> cpi.rs stubs
              --> [core/forge.py]        --> multi-file Rust modules (state, context, lib, cpi)
              --> [core/sdk_gen.py]      --> strict TS clients (no "any", BN/Pubkey typed)
              --> [core/tests_gen.py]    --> Chai/BN invariant assertions harnesses
                                              |
                      ------------------------+
                      v
              [core/audit_gate.py]       --> static bump-binding security verification
              [core/workspace_sync.py]   --> unified multi-program Anchor.toml
              [core/sdk_aggregator.py]   --> unified sdk/index.ts exports
              [core/ci_gen.py]           --> GitHub Actions workflow (.github/workflows/pipeline.yml)
              [core/sim_runner.py]       --> local E2E simulation verification
```

---

## 📁 Core Components (`core/`)

| File | Purpose |
| :--- | :--- |
| `core/forge.py` | Generates modular multi-file Rust programs (`state.rs`, `context.rs`, `lib.rs`) supporting PDAs, custom space/seeds, and SPL Token/Mint structures. |
| `core/cpi_gen.py` | Injects cross-program invocation helpers (`cpi.rs`) targeting multi-program compositions. |
| `core/sdk_gen.py` | Generates strict typed TypeScript SDK clients with exact mapping (`u64`/`i64` -> `number | BN`, `Pubkey` -> `PublicKey`). |
| `core/tests_gen.py` | Generates Chai test harnesses with real state invariant assertions (`balance`, `totalStaked`). |
| `core/audit_gate.py` | Static analysis audit checking `init` accounts for required `bump`/`bumps` safety bindings across the workspace. |
| `core/workspace_sync.py` | Discovers programs in `sandbox/target_workspace/programs/` and synchronizes a unified `Anchor.toml`. |
| `core/sdk_aggregator.py` | Aggregates client modules into a single entrypoint at `sandbox/target_workspace/sdk/index.ts`. |
| `core/ci_gen.py` | Generates GitHub Actions CI workflow for pull requests and main pushes. |
| `core/sim_runner.py` | Local E2E verification runner validating CPI stubs and unified SDK integrity. |

---

## 🚀 Quickstart / Execution

Run the deterministic pipeline locally:
```bash
chmod +x run.sh
./run.sh
```

## 🛡️ Verification Status
* **Audit Gate**: Pass (`3/3` programs verified with bump binding)
* **SDK**: Strict typing enforced
* **Workspace**: Multi-program monorepo synced (`nexus_vault`, `nexus_staking`, `nexus_token_vault`)
