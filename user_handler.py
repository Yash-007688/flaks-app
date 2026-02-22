import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

DB_FILE = "users.db"

def get_db_connection():
    """Returns a connection to the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_user_file():
    """Creates the users.db database and the users table if it doesn't exist."""
    print("📌 Checking database initialization...")
    conn = get_db_connection()
    c = conn.cursor()
    
    # Create table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    
    # Check if admin user exists, if not create default admin and teacher
    c.execute('SELECT * FROM users WHERE username = ?', ('admin',))
    if c.fetchone() is None:
        print("📌 No admin found, creating default users...")
        admin_hashed = generate_password_hash("admin123")
        teacher_hashed = generate_password_hash("pass1")
        
        c.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', 
                  ('admin', admin_hashed, 'Admin'))
        c.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', 
                  ('teacher1', teacher_hashed, 'Teacher'))
        print("✅ users.db created successfully with default users.")
    
    conn.commit()
    conn.close()

def check_user_credentials(username, password):
    """Verifies username and password against the database."""
    try:
        if not os.path.exists(DB_FILE):
            initialize_user_file()
            
        conn = get_db_connection()
        c = conn.cursor()
        
        c.execute('SELECT * FROM users WHERE LOWER(username) = LOWER(?)', (username,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            return user["role"]
        else:
            print("❌ Invalid username or password")
            return None
    except Exception as e:
        print("❌ Error loading database:", e)
        return None

def add_new_user(username, password, role):
    """Adds a new user to the database with a hashed password."""
    try:
        if not os.path.exists(DB_FILE):
            initialize_user_file()

        conn = get_db_connection()
        c = conn.cursor()
        
        # Check if user already exists
        c.execute('SELECT * FROM users WHERE LOWER(username) = LOWER(?)', (username,))
        if c.fetchone():
            print(f"⚠️ User '{username}' already exists.")
            conn.close()
            return False
            
        hashed_password = generate_password_hash(password)
        c.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', 
                  (username, hashed_password, role))
        
        conn.commit()
        conn.close()
        
        print(f"✅ User '{username}' added successfully!")
        return True
    except Exception as e:
        print("❌ Error updating database:", e)
        return False

# ✅ Ensure database is ready when the app starts
initialize_user_file()
