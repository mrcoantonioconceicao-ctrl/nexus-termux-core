use anchor_lang::prelude::*;

// Auto-generated cross-program invocation stub targeting nexus_token_vault::deposit_token
pub fn cpi_nexus_token_vault_deposit_token<'info>(target_program: &AccountInfo<'info>, accounts: &[AccountInfo<'info>], data: &[u8]) -> Result<()> {
    let ix = anchor_lang::solana_program::instruction::Instruction {
        program_id: *target_program.key,
        accounts: vec![],
        data: data.to_vec(),
    };
    anchor_lang::solana_program::program::invoke(&ix, accounts)
}

