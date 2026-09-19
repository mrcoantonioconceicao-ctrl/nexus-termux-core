import { Program } from '@coral-xyz/anchor';
import { PublicKey } from '@solana/web3.js';

export const PROGRAM_ID = new PublicKey('NexaStaking111111111111111111111111111111111');

export class NexusStakingClient {
    program: Program<any>;

    constructor(program: Program<any>) {
        this.program = program;
    }

    async initialize_pool(params: any): Promise<string> {
        return await this.program.methods
            .initialize_pool(params)
            .rpc();
    }

    async stake(params: any): Promise<string> {
        return await this.program.methods
            .stake(params)
            .rpc();
    }
}
