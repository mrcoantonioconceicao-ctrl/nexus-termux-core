import * as anchor from '@project-serum/anchor';
import { Program } from '@project-serum/anchor';
import { assert } from 'chai';
import { NexusTokenVault } from '../target/types/nexus_token_vault';

describe('nexus_token_vault', () => {
  const provider = anchor.AnchorProvider.env();
  anchor.setProvider(provider);
  const program = anchor.workspace.NexusTokenVault as Program<NexusTokenVault>;

  it('Initializes PDA and executes state invariant lifecycle', async () => {
    const [pda] = await anchor.web3.PublicKey.findProgramAddressSync(
      [Buffer.from("vault"), provider.wallet.publicKey.toBuffer()],
      program.programId
    );
    
    
  });
});
