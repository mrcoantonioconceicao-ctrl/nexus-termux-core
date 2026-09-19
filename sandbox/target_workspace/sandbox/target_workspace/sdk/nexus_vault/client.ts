import { Program } from '@coral-xyz/anchor';
import { PublicKey } from '@solana/web3.js';

export const PROGRAM_ID = new PublicKey('NexaVault1111111111111111111111111111111111');

export class NexusVaultClient {
    program: Program<any>;

    constructor(program: Program<any>) {
        this.program = program;
    }

    async initialize(params: any): Promise<string> {
        return await this.program.methods
            .initialize(params)
            .rpc();
    }

    async deposit(params: any): Promise<string> {
        return await this.program.methods
            .deposit(params)
            .rpc();
    }
}
