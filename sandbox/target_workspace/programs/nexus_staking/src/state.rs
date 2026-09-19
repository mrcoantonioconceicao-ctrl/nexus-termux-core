use anchor_lang::prelude::*;

#[account]
#[derive(Default)]
pub struct StakePool {
    pub authority: Pubkey,
    pub bump: u8,
    pub total_staked: u64,
}

