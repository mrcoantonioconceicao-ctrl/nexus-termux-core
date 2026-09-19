import * as anchor from '@project-serum/anchor';
import { Program } from '@project-serum/anchor';
import { assert } from 'chai';
import { NexusVault } from '../target/types/nexus_vault';

describe('nexus_vault', () => {
  const provider = anchor.AnchorProvider.env();
  anchor.setProvider(provider);
  const program = anchor.workspace.NexusVault as Program<NexusVault>;

  it('Initializes PDA and executes state invariant lifecycle', async () => {
    const [pda] = await anchor.web3.PublicKey.findProgramAddressSync(
      [Buffer.from("vault"), provider.wallet.publicKey.toBuffer()],
      program.programId
    );
    
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
  });
});
