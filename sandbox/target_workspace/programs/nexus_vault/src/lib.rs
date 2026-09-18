use anchor_lang::prelude::*;

pub mod state;
pub mod context;
use state::*;
use context::*;

declare_id!("NexaVault1111111111111111111111111111111111");

#[program]
pub mod nexus_vault {
    use super::*;

    pub fn initialize(ctx: Context<InitializeVault>) -> Result<()> {
        msg!("Initializing Vault PDA with seeds");
        Ok(())
    }

    pub fn deposit(ctx: Context<DepositVault>) -> Result<()> {
        msg!("Processing deposit lamports to PDA");
        Ok(())
    }
}
