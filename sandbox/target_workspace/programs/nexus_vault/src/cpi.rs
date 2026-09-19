use anchor_lang::prelude::*;

// Auto-generated cross-program invocation stub targeting nexus_token_vault::deposit_token
pub fn cpi_nexus_token_vault_deposit_token<'info>(target_program: &AccountInfo<'info>, accounts: &[AccountInfo<'info>], data: &[u8]) -> Result<()> {
    let ix = anchor_lang::solana_program::instruction::Instruction {
        program_id: *target_program.key,
        accounts: accounts.iter().map(|acc| {
    // CRITICAL FIX: The `accounts` field in the `Instruction` struct must accurately declare
    // the metadata (pubkey, is_signer, is_writable) for ALL accounts required by the target program's instruction.
    // The original `accounts: vec![]` is a severe flaw as it prevents the target program
    // (especially Anchor programs) from properly validating and processing accounts, leading to transaction failure.
    // Simply copying `is_signer` and `is_writable` from the `AccountInfo` provided to this stub
    // might be incorrect if the target program has different requirements. It is essential
    // to consult the `nexus_token_vault::deposit_token` instruction definition
    // to correctly set `is_signer` and `is_writable` for each account.
    anchor_lang::solana_program::instruction::AccountMeta {
        pubkey: *acc.key,
        is_signer: acc.is_signer,   // Placeholder: verify against target program's requirements
        is_writable: acc.is_writable // Placeholder: verify against target program's requirements
    }
}).collect(),
        data: data.to_vec(),
    };
    anchor_lang::solana_program::program::invoke(&ix, accounts)
}

