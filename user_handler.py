import pandas as pd
import os

USER_FILE = "users.xlsx"  # File storing user credentials

def initialize_user_file():
    """Creates users.xlsx if it doesn't exist with default users and correct columns."""
    if not os.path.exists(USER_FILE):
        print("📌 users.xlsx not found. Creating a new one...")

        data = {
            "username": ["admin", "teacher1"],
            "password": ["admin123", "pass1"],
            "role": ["Admin", "Teacher"]
        }
        
        df = pd.DataFrame(data)
        df.to_excel(USER_FILE, index=False, engine="openpyxl")
        print("✅ users.xlsx created successfully!")
    else:
        # ✅ Check if file exists but missing required columns
        df = pd.read_excel(USER_FILE, engine="openpyxl")
        required_columns = {"username", "password", "role"}

        if not required_columns.issubset(df.columns):
            print("❌ Error: Missing required columns in users.xlsx. Recreating file...")
            os.remove(USER_FILE)  # Remove incorrect file
            initialize_user_file()  # Create correct file

def check_user_credentials(username, password):
    """Checks if username, password, and role match in users.xlsx."""
    try:
        if not os.path.exists(USER_FILE):
            initialize_user_file()  # ✅ Ensure file exists

        df = pd.read_excel(USER_FILE, engine="openpyxl")

        # ✅ Ensure required columns exist
        required_columns = {"username", "password", "role"}
        if not required_columns.issubset(df.columns):
            print("❌ Error: Missing required columns in users.xlsx")
            return None

        # ✅ Convert username and password to strings (avoiding NaN errors)
        df["username"] = df["username"].astype(str)
        df["password"] = df["password"].astype(str)

        # ✅ Check if username and password exist
        user_data = df[(df["username"].str.lower() == username.lower()) & (df["password"] == password)]

        if not user_data.empty:
            return user_data["role"].values[0]  # ✅ Return role if valid
        else:
            print("❌ Invalid username or password")
            return None
    except Exception as e:
        print("❌ Error loading users.xlsx:", e)
        return None

def add_new_user(username, password, role):
    """Adds a new user to users.xlsx if not already present."""
    try:
        # ✅ Ensure `users.xlsx` exists
        if not os.path.exists(USER_FILE):
            initialize_user_file()

        df = pd.read_excel(USER_FILE, engine="openpyxl")

        # ✅ Convert username to lowercase for case-insensitive check
        if username.lower() in df["username"].str.lower().values:
            print(f"⚠️ User '{username}' already exists.")
            return False

        # ✅ Append new user
        new_user = pd.DataFrame({"username": [username], "password": [password], "role": [role]})
        df = pd.concat([df, new_user], ignore_index=True)

        df.to_excel(USER_FILE, index=False, engine="openpyxl")
        print(f"✅ User '{username}' added successfully!")
        return True
    except Exception as e:
        print("❌ Error updating users.xlsx:", e)
        return False

# ✅ Ensure users.xlsx exists when Flask starts
initialize_user_file()
