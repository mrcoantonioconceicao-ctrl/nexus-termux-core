// Strict Typed SDK for nexus_staking
import { Program, BN } from '@project-serum/anchor';
import { PublicKey } from '@solana/web3.js';

export interface StakeParams {
  amount: BN;
}


export interface StakePool {
  authority: PublicKey;
  bump: number;
  total_staked: number | BN;
}


export class NexusStakingClient {
  constructor(readonly program: Program) {}

  async initialize_pool() {
    return await this.program.methods.initialize_pool().rpc();
  }

  async stake(params: StakeParams) {
    return await this.program.methods.stake({ ...params }).rpc();
  }

}
