// Strict Typed SDK for nexus_vault
import { Program, BN } from '@project-serum/anchor';
import { PublicKey } from '@solana/web3.js';

export interface DepositParams {
  amount: number | BN;
}

export interface WithdrawParams {
  amount: number | BN;
}


export interface Vault {
  authority: PublicKey;
  bump: number;
  balance: number | BN;
}


export class NexusVaultClient {
  constructor(readonly program: Program) {}

  async initialize_vault() {
    return await this.program.methods.initialize_vault().rpc();
  }

  async deposit(params: DepositParams) {
    return await this.program.methods.deposit({ ...params }).rpc();
  }

  async withdraw(params: WithdrawParams) {
    return await this.program.methods.withdraw({ ...params }).rpc();
  }

}
