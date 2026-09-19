import * as anchor from '@coral-xyz/anchor';
import { NexusStakingClient } from '../sdk/nexus_staking/client';

describe('nexus_staking', () => {
    const provider = anchor.AnchorProvider.env();
    anchor.setProvider(provider);
    
    const mockProgram = { methods: {} } as any;
    const client = new NexusStakingClient(mockProgram);

    it("initialize_pool instruction", async () => {
        const tx = await client.initialize_pool({});
        console.log("initialize_pool tx:", tx);
    });
    it("stake instruction", async () => {
        const tx = await client.stake({});
        console.log("stake tx:", tx);
    });
});
