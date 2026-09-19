use anchor_lang::prelude::*;

pub mod state;
pub mod context;
use state::*;
use context::*;

declare_id!("NexaStaking111111111111111111111111111111111");

#[program]
pub mod nexus_staking {
    use super::*;

    pub fn initialize_pool(ctx: Context<InitializePool>) -> Result<()> {
        msg!("Staking pool initialized");
    ctx.accounts.pool.bump = ctx.bumps.pool;
        Ok(())
    }
}
