use anchor_lang::prelude::*;
use crate::state::*;
use anchor_spl::token::{Token, TokenAccount, Mint};

#[derive(Accounts)]
pub struct InitializeTokenVault<'info> {
    #[account(init, payer = signer, space = 8 + 65, seeds = [b"vault", signer.key().as_ref()], bump)]
    pub vault: Account<'info, TokenVaultState>,
    pub mint: Account<'info, Mint>,
    #[account(mut)]
    pub signer: Signer<'info>
    , pub system_program: Program<'info, System>
}

#[derive(Accounts)]
pub struct DepositToken<'info> {
    #[account(mut)]
    pub vault: Account<'info, TokenVaultState>,
    #[account(mut)]
    pub vault_token_account: Account<'info, TokenAccount>,
    #[account(mut)]
    pub user_token_account: Account<'info, TokenAccount>,
    pub token_program: Program<'info, Token>,
    #[account(mut)]
    pub signer: Signer<'info>
;
}

