import * as anchor from '@project-serum/anchor';
import { Program } from '@project-serum/anchor';
import { assert } from 'chai';
import { NexusStaking } from '../target/types/nexus_staking';

describe('nexus_staking', () => {
  const provider = anchor.AnchorProvider.env();
  anchor.setProvider(provider);
  const program = anchor.workspace.NexusStaking as Program<NexusStaking>;

  it('Initializes PDA and executes state invariant lifecycle', async () => {
    const [pda] = await anchor.web3.PublicKey.findProgramAddressSync(
      [Buffer.from("pool"), provider.wallet.publicKey.toBuffer()],
      program.programId
    );
    
    const poolAccount = await program.account.stakePool.fetch(pda);
    assert.ok(poolAccount.authority.equals(provider.wallet.publicKey));
    assert.strictEqual(poolAccount.totalStaked.toNumber(), 0);

    // Test stake invariant
    await program.methods.stake(new anchor.BN(1000)).accounts({ pool: pda }).rpc();
    const p = await program.account.stakePool.fetch(pda);
    assert.strictEqual(p.totalStaked.toNumber(), 1000);
  });
});
