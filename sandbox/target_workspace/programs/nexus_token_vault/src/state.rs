use anchor_lang::prelude::*;

#[account]
#[derive(Default)]
pub struct TokenVaultState {
    pub authority: Pubkey,
    pub bump: u8,
    pub mint: Pubkey,
}

