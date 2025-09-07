# API Project

This is a cryptocurrency-related API project with functionality for airdrops, mining, deposits, and withdrawals.

## Setup Instructions

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory based on the `.env.example` template:
   ```
   cp .env.example .env
   ```
4. Edit the `.env` file and add your credentials:
   - Database credentials
   - API keys for BaseScan and BscScan
   - Wallet private key

5. Run the application:
   ```
   python app.py
   ```

## Security Notes

- Never commit your `.env` file to version control
- Keep your private keys and API credentials secure
- Use strong passwords for database access
- Regularly rotate your credentials for enhanced security

## Features

- Airdrop Distribution
- Mining System
- Deposit Management
- Withdrawal Processing
