use anchor_lang::prelude::*;
mod state;
mod context;
use state::*;
use context::*;

declare_id!("NexaStaking111111111111111111111111111111111");

#[program]
pub mod nexus_staking {
    use super::*;

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
pool.total_staked = pool.total_staked.checked_add(amount).ok_or(anchor_lang::error::ErrorCode::AccountDidNotSerialize)?;
msg!("Staked amount: {}", amount);
        Ok(())
    }
}
