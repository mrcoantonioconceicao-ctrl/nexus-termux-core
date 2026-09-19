import * as anchor from '@coral-xyz/anchor';
import { NexusVaultClient } from '../sdk/nexus_vault/client';

describe('nexus_vault', () => {
    const provider = anchor.AnchorProvider.env();
    anchor.setProvider(provider);
    
    const mockProgram = { methods: {} } as any;
    const client = new NexusVaultClient(mockProgram);

    it("initialize_vault instruction", async () => {
        const tx = await client.initialize_vault({});
        console.log("initialize_vault tx:", tx);
    });
    it("deposit instruction", async () => {
        const tx = await client.deposit({});
        console.log("deposit tx:", tx);
    });
    it("withdraw instruction", async () => {
        const tx = await client.withdraw({});
        console.log("withdraw tx:", tx);
    });
});
