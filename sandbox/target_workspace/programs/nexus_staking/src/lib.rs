use anchor_lang::prelude::*;
mod state;
mod context;
use state::*;
use context::*;

declare_id!("NexaStaking111111111111111111111111111111111");

#[program]
pub mod nexus_staking {
    use super::*;

    // [SecOps Guard] Checked Signer & Authority Validation
    pub fn initialize_pool(ctx: Context<InitializePool>) -> Result<()> {
        let pool = &mut ctx.accounts.pool;
pool.authority = ctx.accounts.signer.key();
pool.bump = ctx.bumps.pool;
pool.total_staked = 0;
msg!("Staking pool initialized");
        Ok(())
    }
    pub fn stake(ctx: Context<Stake>, amount: u64) -> Result<()> {
        let pool = &mut ctx.accounts.pool;

        // Transfer tokens from the staker's token account to the pool's vault
        let cpi_accounts = anchor_spl::token::Transfer {
            from: ctx.accounts.user_token_account.to_account_info(),
            to: ctx.accounts.pool_vault.to_account_info(),
            authority: ctx.accounts.signer.to_account_info(),
        };
        let cpi_program = ctx.accounts.token_program.to_account_info();
        let cpi_context = CpiContext::new(cpi_program, cpi_accounts);
        anchor_spl::token::transfer(cpi_context, amount)?;

        // Update the pool's total_staked counter AFTER successful transfer
        pool.total_staked = pool.total_staked.checked_add(amount)
            .ok_or(anchor_lang::error::ErrorCode::ArithmeticError)?;

        msg!("Successfully staked amount: {}", amount);
        Ok(())
    }
}
