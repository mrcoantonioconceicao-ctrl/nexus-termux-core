import * as anchor from '@coral-xyz/anchor';
import { NexusVaultClient } from '../sdk/nexus_vault/client';

describe('nexus_vault', () => {
    const provider = anchor.AnchorProvider.env();
    anchor.setProvider(provider);
    
    const mockProgram = { methods: {} } as any;
    const client = new NexusVaultClient(mockProgram);

    it("initialize instruction", async () => {
        const tx = await client.initialize({});
        console.log("initialize tx:", tx);
    });
    it("deposit instruction", async () => {
        const tx = await client.deposit({});
        console.log("deposit tx:", tx);
    });
});
