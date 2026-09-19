use anchor_lang::prelude::*;

#[account]
#[derive(Default)]
pub struct Vault {
    pub authority: Pubkey,
    pub bump: u8,
    pub total_deposits: u64,
}

