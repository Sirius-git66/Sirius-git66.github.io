import asyncio
from twscrape import AccountsPool

async def add_account():
    try:
        pool = AccountsPool()
        # Add your account to the pool
        await pool.add_account("TheArcCloud", "Loveholic!66", "", "")
        print("Account 'TheArcCloud' added successfully to twscrape pool!")
        print("\nNow you need to log in to the account.")
        print("Run this command in your terminal:")
        print("twscrape pool login-all")
    except Exception as e:
        print(f"Error adding account: {e}")

if __name__ == "__main__":
    asyncio.run(add_account())