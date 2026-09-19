use anchor_lang::prelude::*;
use crate::state::*;
use anchor_spl::token::{Token, TokenAccount, Mint};

#[derive(Accounts)]
pub struct InitializePool<'info> {
    #[account(init, payer = signer, space = 8 + 49, seeds = [b"pool", signer.key().as_ref()], bump)]
    pub pool: Account<'info, StakePool>,
    #[account(mut)]
    pub signer: Signer<'info>
    , pub system_program: Program<'info, System>
}

#[derive(Accounts)]
pub struct Stake<'info> {
    #[account(mut, seeds = [b"pool", signer.key().as_ref()], bump)]
    pub pool: Account<'info, StakePool>,
    #[account(mut)]
    pub signer: Signer<'info>
    , pub system_program: Program<'info, System>
}

