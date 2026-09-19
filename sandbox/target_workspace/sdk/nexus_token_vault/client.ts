// Strict Typed SDK for nexus_token_vault
import { Program, BN } from '@project-serum/anchor';
import { PublicKey } from '@solana/web3.js';

export interface DepositTokenParams {
  amount: number | BN;
}


export interface TokenVaultState {
  authority: PublicKey;
  bump: number;
  mint: PublicKey;
}


export class NexusTokenVaultClient {
  constructor(readonly program: Program) {}

  async initialize_token_vault() {
    return await this.program.methods.initialize_token_vault().rpc();
  }

  async deposit_token(params: DepositTokenParams) {
    return await this.program.methods.deposit_token({ ...params }).rpc();
  }

}
