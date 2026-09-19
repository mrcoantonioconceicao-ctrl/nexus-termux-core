use anchor_lang::prelude::*;


#[account]
pub struct StakePool {
    pub authority: Pubkey,
    pub bump: u8,
    pub total_staked: u64,
}
