#!/usr/bin/env python3
"""
Script to add Twitter accounts to twscrape pool
"""

import asyncio
import sys
import os

def show_instructions():
    print("TWITTER ACCOUNT SETUP")
    print("=" * 30)
    print("This script will help you add Twitter accounts to twscrape.")
    print("\nInstructions:")
    print("1. Create a file called 'accounts.txt' with your Twitter accounts")
    print("2. Each line should contain: username password")
    print("3. Example:")
    print("   user1 pass1")
    print("   user2 pass2")
    print("\nNote: Use throwaway/secondary accounts, not your main account.")
    print("These accounts will be used for scraping news only.\n")

async def add_accounts():
    # Check if accounts.txt exists
    if not os.path.exists("accounts.txt"):
        print("Error: accounts.txt file not found!")
        show_instructions()
        return False
    
    # Read accounts from file
    accounts = []
    try:
        with open("accounts.txt", "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    parts = line.split()
                    if len(parts) >= 2:
                        username = parts[0]
                        password = parts[1]
                        accounts.append((username, password))
    except Exception as e:
        print(f"Error reading accounts.txt: {e}")
        return False
    
    if not accounts:
        print("No accounts found in accounts.txt")
        show_instructions()
        return False
    
    print(f"Found {len(accounts)} accounts in accounts.txt")
    
    # Add accounts to twscrape pool
    try:
        from twscrape import AccountsPool
        pool = AccountsPool()
        
        for username, password in accounts:
            try:
                # Add account to pool
                await pool.add_account(username, password, "", "")
                print(f"Added account: {username}")
            except Exception as e:
                print(f"Failed to add account {username}: {e}")
        
        print("\nAccounts added successfully!")
        print("Now run: twscrape pool login-all")
        return True
        
    except Exception as e:
        print(f"Error adding accounts: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(add_accounts())