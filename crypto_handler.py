import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get or create encryption key
KEY_FILE = ".env"
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

def generate_key():
    """Generates a new encryption key and saves it to .env."""
    key = Fernet.generate_key().decode()
    with open(KEY_FILE, "a") as f:
        f.write(f"\nENCRYPTION_KEY={key}\n")
    return key

if not ENCRYPTION_KEY:
    print("🔑 No encryption key found. Generating a new one...")
    ENCRYPTION_KEY = generate_key()

fernet = Fernet(ENCRYPTION_KEY.encode())

def encrypt_file(file_path, encrypted_path):
    """Encrypts a file and saves it to a new path."""
    if not os.path.exists(file_path):
        return False
        
    with open(file_path, "rb") as f:
        data = f.read()
        
    encrypted_data = fernet.encrypt(data)
    
    with open(encrypted_path, "wb") as f:
        f.write(encrypted_data)
        
    return True

def decrypt_file(encrypted_path, file_path):
    """Decrypts a file and saves it to a new path."""
    if not os.path.exists(encrypted_path):
        return False
        
    with open(encrypted_path, "rb") as f:
        encrypted_data = f.read()
        
    try:
        decrypted_data = fernet.decrypt(encrypted_data)
        with open(file_path, "wb") as f:
            f.write(decrypted_data)
        return True
    except Exception as e:
        print(f"❌ Error decrypting file: {e}")
        return False
