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
    #[account(
        mut,
        // Ensure the vault token account is owned by the vault PDA.
        // This prevents an attacker from redirecting funds to an arbitrary account, leading to loss of funds.
        owner = vault.key(),
        // Ensure the vault token account holds tokens of the correct mint type as defined by the vault state.
        // This prevents depositing wrong token types or interacting with an unrelated token account.
        mint = vault.mint
    )]
    pub vault_token_account: Account<'info, TokenAccount>,
    #[account(mut)]
    pub user_token_account: Account<'info, TokenAccount>,
    pub token_program: Program<'info, Token>,
    #[account(mut)]
    pub signer: Signer<'info>
;
}

