use anchor_lang::prelude::*;
mod state;
mod context;
use state::*;
use context::*;

declare_id!("NexaTokenV11111111111111111111111111111111");

#[program]
pub mod nexus_token_vault {
    use super::*;

    pub fn initialize_token_vault(ctx: Context<InitializeTokenVault>) -> Result<()> {
        let vault = &mut ctx.accounts.vault;
vault.authority = ctx.accounts.signer.key();
vault.bump = ctx.bumps.vault;
vault.mint = ctx.accounts.mint.key();
msg!("Token vault initialized");
        // VULNERABILITY: Missing token transfer logic.
        // The deposit_token function currently logs a message but does not
        // perform any actual token transfer or update any vault state.
        // This means tokens sent by users would not be accounted for or moved
        // to the vault, leading to loss of funds or misleading behavior.

        // --- FIX: Implement actual token transfer using Anchor's SPL token CPI ---
        // This requires 'sender_token_account', 'vault_token_account', 'sender'
        // (the signer initiating the transfer), and 'token_program' to be
        // correctly defined and marked as `mut` where appropriate in the
        // `DepositToken` context struct.

        // Example of required accounts in context (assuming `DepositToken` includes them):
        // #[derive(Accounts)]
        // pub struct DepositToken<'info> {
        //     #[account(mut)]
        //     pub sender: Signer<'info>, // The user initiating the deposit
        //     #[account(mut, token::mint = mint, token::authority = sender)]
        //     pub sender_token_account: Account<'info, TokenAccount>, // User's token account
        //     #[account(mut, seeds = [b"token_vault", mint.key().as_ref()], bump = vault.bump)]
        //     pub vault: Account<'info, Vault>, // The vault state account (must be mutable)
        //     #[account(mut, token::mint = mint, token::authority = vault_authority)]
        //     pub vault_token_account: Account<'info, TokenAccount>, // The vault's token account
        //     /// CHECK: This is the PDA that owns the vault_token_account, not a signer.
        //     pub vault_authority: UncheckedAccount<'info>, // PDA as authority for vault's token account
        //     pub mint: Account<'info, Mint>, // The token mint being deposited
        //     pub token_program: Program<'info, Token>,
        // }

        let cpi_accounts = anchor_spl::token::Transfer {
            from: ctx.accounts.sender_token_account.to_account_info(),
            to: ctx.accounts.vault_token_account.to_account_info(),
            authority: ctx.accounts.sender.to_account_info(), // The signer account authorizing the transfer
        };
        let cpi_program = ctx.accounts.token_program.to_account_info();
        anchor_spl::token::transfer(
            CpiContext::new(cpi_program, cpi_accounts),
            amount,
        )?;

        // --- IMPORTANT: Update the vault's internal state to track the deposit ---
        // The provided `state.rs` and `context.rs` are not available, but typically
        // you would want to update a field in the `vault` account (e.g., total_deposited)
        // or create a separate account to track individual user deposits for future withdrawals.

        // Example: If `ctx.accounts.vault` has a `total_deposited_amount` field:
        // ctx.accounts.vault.total_deposited_amount = ctx.accounts.vault.total_deposited_amount
        //     .checked_add(amount)
        //     .ok_or_else(|| error!(ErrorCode::MathOverflow))?; // Define MathOverflow in your Error enum

        msg!("Tokens successfully deposited: {}", amount);
        Ok(())
    }
    pub fn deposit_token(ctx: Context<DepositToken>, amount: u64) -> Result<()> {
        msg!("Depositing token amount: {}", amount);
        Ok(())
    }
}
