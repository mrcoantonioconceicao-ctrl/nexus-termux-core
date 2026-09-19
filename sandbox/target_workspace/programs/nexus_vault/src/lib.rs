use anchor_lang::prelude::*;
mod state;
mod context;
use state::*;
use context::*;

declare_id!("NexaVault111111111111111111111111111111111");

#[program]
pub mod nexus_vault {
    use super::*;

    pub fn initialize_vault(ctx: Context<InitializeVault>) -> Result<()> {
        let vault = &mut ctx.accounts.vault;
vault.authority = ctx.accounts.signer.key();
vault.bump = ctx.bumps.vault;
vault.balance = 0;
msg!("Vault initialized");
        Ok(())
    }
    pub fn deposit(ctx: Context<Deposit>, amount: u64) -> Result<()> {
        let vault = &mut ctx.accounts.vault;
vault.balance = vault.balance.checked_add(amount).ok_or(anchor_lang::error::ErrorCode::AccountDidNotSerialize)?;
msg!("Vault deposited: {}", amount);
        Ok(())
    }
    pub fn withdraw(ctx: Context<Withdraw>, amount: u64) -> Result<()> {
        let vault = &mut ctx.accounts.vault;
vault.balance = vault.balance.checked_sub(amount).ok_or(anchor_lang::error::ErrorCode::AccountDidNotSerialize)?;
msg!("Vault withdrawn: {}", amount);
        Ok(())
    }
}
