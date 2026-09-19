use anchor_lang::prelude::*;
use crate::state::*;
use anchor_spl::token::{Token, TokenAccount, Mint};

#[derive(Accounts)]
pub struct InitializeVault<'info> {
    #[account(init, payer = signer, space = 8 + 49, seeds = [b"vault", signer.key().as_ref()], bump)]
    pub vault: Account<'info, Vault>,
    #[account(mut)]
    pub signer: Signer<'info>
    , pub system_program: Program<'info, System>
}

#[derive(Accounts)]
pub struct Deposit<'info> {
    #[account(mut)]
    pub vault: Account<'info, Vault>,
    #[account(mut)]
    pub signer: Signer<'info>
    , pub system_program: Program<'info, System>
}

#[derive(Accounts)]
pub struct Withdraw<'info> {
    #[account(mut)]
    pub vault: Account<'info, Vault>,
    #[account(mut)]
    pub signer: Signer<'info>
    , pub system_program: Program<'info, System>
}

