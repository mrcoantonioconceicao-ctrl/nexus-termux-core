use anchor_lang::prelude::*;
use super::state::*;


#[derive(Accounts)]
pub struct InitializePool<'info> {
    #[account(mut)]
    pub signer: Signer<'info>,
    pub system_program: Program<'info, System>,
    #[account(
        init,
        payer = signer,
        space = 49,
        seeds = [b"pool", signer.key().as_ref()],
        bump
    )]
    pub pool: Account<'info, StakePool>,
}
