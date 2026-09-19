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
    #[account(
        mut,
        // O token_account do vault deve ser para o mint especificado.
        token::mint = mint_account,
        // A autoridade do token_account do vault deve ser a própria conta PDA do vault.
        // Isso garante que o vault PDA é quem "possui" os tokens e pode autorizar a retirada.
        token::authority = vault // A conta do vault (PDA) atua como autoridade para este token account
    )]
    pub vault_token_account: Account<'info, TokenAccount>,
    #[account(
        mut,
        // O token_account de destino do signer deve ser para o mint especificado.
        token::mint = mint_account,
        // O token_account de destino deve ser de propriedade do signer.
        token::authority = signer
    )]
    pub signer_token_account: Account<'info, TokenAccount>,
    // A conta Mint real para o token que está sendo sacado.
    pub mint_account: Account<'info, Mint>,
    #[account(mut)]
    pub signer: Signer<'info>,
    pub system_program: Program<'info, System>,
    pub token_program: Program<'info, Token> // O programa SPL Token
}

