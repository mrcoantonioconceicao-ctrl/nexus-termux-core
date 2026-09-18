use anchor_lang::prelude::*;

declare_id!("NexaVault1111111111111111111111111111111111");

#[program]
pub mod nexus_vault {
    use super::*;

    pub fn initialize(ctx: Context<InitializeVault>) -> Result<()> {
        // [nexus-forged-logic]: set vault authority and bump PDA
        msg!("Executing initialize");
        Ok(())
    }

    pub fn deposit(ctx: Context<DepositVault>) -> Result<()> {
        // [nexus-forged-logic]: transfer lamports into PDA vault
        msg!("Executing deposit");
        Ok(())
    }
}
