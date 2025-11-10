import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def add_account():
    try:
        # Import twscrape
        from twscrape import AccountsPool
        
        # Create accounts pool
        pool = AccountsPool()
        
        # Add your account directly
        username = "TheArcCloud"
        password = "Loveholic!66"
        email = "thearccloud@example.com"
        email_password = "password123"
        
        print(f"Adding account: {username}")
        await pool.add_account(username, password, email, email_password)
        print("Account added successfully!")
        
        # Try to login
        print("Attempting to login...")
        await pool.login_all()
        print("Login completed!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(add_account())