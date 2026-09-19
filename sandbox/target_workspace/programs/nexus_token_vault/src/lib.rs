use anchor_lang::prelude::*;
mod state;
mod context;
use state::*;
use context::*;

declare_id!("NexaTokenV11111111111111111111111111111111");

#[program]
pub mod nexus_token_vault {
    use super::*;

    pub fn initialize_token_vault(ctx: Context<InitializeTokenVault>) -> Result<()> {
        let vault = &mut ctx.accounts.vault;
vault.authority = ctx.accounts.signer.key();
vault.bump = ctx.bumps.vault;
vault.mint = ctx.accounts.mint.key();
msg!("Token vault initialized");
        Ok(())
    }
    pub fn deposit_token(ctx: Context<DepositToken>, amount: u64) -> Result<()> {
        msg!("Depositing token amount: {}", amount);
        Ok(())
    }
}
