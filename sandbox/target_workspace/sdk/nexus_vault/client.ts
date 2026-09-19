// Strict Typed SDK for nexus_vault
import { Program, BN } from '@project-serum/anchor';
import { PublicKey } from '@solana/web3.js';


export interface Vault {
  authority: PublicKey;
  bump: number;
  total_deposits: number | BN;
}


export class NexusVaultClient {
  constructor(readonly program: Program) {}

  async initialize() {
    return await this.program.methods.initialize().rpc();
  }

  async deposit() {
    return await this.program.methods.deposit().rpc();
  }

}
