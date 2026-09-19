use anchor_lang::prelude::*;

#[account]
#[derive(Default)]
pub struct StakePool {
    pub authority: Pubkey,
    pub bump: u8,
    pub total_staked: u64,
}

impl StakePool {
    pub const LEN: usize = 8 + 32 + 1 + 8; // Discriminator (8 bytes) + Pubkey (32 bytes) + u8 (1 byte) + u64 (8 bytes)
}

