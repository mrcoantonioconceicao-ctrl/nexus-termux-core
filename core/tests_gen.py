import json
import sys
from pathlib import Path

def generate_tests(spec_path: Path):
    with open(spec_path, "r") as f:
        spec = json.load(f)
    
    prog_name = spec["program"]
    out_dir = Path("sandbox/target_workspace/tests")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    pascal_name = "".join(word.capitalize() for word in prog_name.split("_"))
    seed_prefix = "vault" if "vault" in prog_name else "pool"
    
    state_asserts = ""
    if "nexus_vault" in prog_name:
        state_asserts = """
    const vaultAccount = await program.account.vault.fetch(pda);
    assert.ok(vaultAccount.authority.equals(provider.wallet.publicKey));
    assert.strictEqual(vaultAccount.balance.toNumber(), 0);

    // Test deposit invariant
    await program.methods.deposit(new anchor.BN(150)).accounts({ vault: pda }).rpc();
    let v = await program.account.vault.fetch(pda);
    assert.strictEqual(v.balance.toNumber(), 150);

    // Test withdraw invariant
    await program.methods.withdraw(new anchor.BN(50)).accounts({ vault: pda }).rpc();
    v = await program.account.vault.fetch(pda);
    assert.strictEqual(v.balance.toNumber(), 100);
    """
    elif "nexus_staking" in prog_name:
        state_asserts = """
    const poolAccount = await program.account.stakePool.fetch(pda);
    assert.ok(poolAccount.authority.equals(provider.wallet.publicKey));
    assert.strictEqual(poolAccount.totalStaked.toNumber(), 0);

    // Test stake invariant
    await program.methods.stake(new anchor.BN(1000)).accounts({ pool: pda }).rpc();
    const p = await program.account.stakePool.fetch(pda);
    assert.strictEqual(p.totalStaked.toNumber(), 1000);
    """

    test_code = f"""import * as anchor from '@project-serum/anchor';
import {{ Program }} from '@project-serum/anchor';
import {{ assert }} from 'chai';
import {{ {pascal_name} }} from '../target/types/{prog_name}';

describe('{prog_name}', () => {{
  const provider = anchor.AnchorProvider.env();
  anchor.setProvider(provider);
  const program = anchor.workspace.{pascal_name} as Program<{pascal_name}>;

  it('Initializes PDA and executes state invariant lifecycle', async () => {{
    const [pda] = await anchor.web3.PublicKey.findProgramAddressSync(
      [Buffer.from("{seed_prefix}"), provider.wallet.publicKey.toBuffer()],
      program.programId
    );
    
    {state_asserts.strip()}
  }});
}});
"""
    out_file = out_dir / f"{prog_name}.ts"
    out_file.write_text(test_code)
    print(f"[TEST GEN] Rich assertions harness generated at: {out_file}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        generate_tests(Path(sys.argv[1]))
