// -- initial nexus state --

// [nexus-inserted: initialize_vault]
pub fn initialize_vault() -> Result<()> { Ok(()) 
    pub fn initialize(ctx: Context<InitializeVault>) -> Result<()> {
        // [nexus-forged-logic]: set vault authority and bump PDA
        msg!("Executing initialize");
        Ok(())
    }


    pub fn deposit(ctx: Context<DepositVault>) -> Result<()> {
        // [nexus-forged-logic]: transfer lamports into PDA vault
        msg!("Executing deposit");
        Ok(())
    }

}
