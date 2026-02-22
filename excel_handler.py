import pandas as pd
import os
from datetime import datetime
from crypto_handler import encrypt_file, decrypt_file

FILE_PATH = "पत्रक 2025-26.xlsx"
ENC_FILE_PATH = "पत्रक 2025-26.enc"
EDIT_LOG_FILE = "edit_log.xlsx"
ENC_EDIT_LOG_FILE = "edit_log.enc"

def init_encryption():
    """Encrypts the original files if encrypted versions don't exist yet."""
    if not os.path.exists(ENC_FILE_PATH) and os.path.exists(FILE_PATH):
        print(f"🔒 Encrypting original {FILE_PATH}...")
        encrypt_file(FILE_PATH, ENC_FILE_PATH)
        os.remove(FILE_PATH)
        print(f"✅ Replaced with {ENC_FILE_PATH}")

    if not os.path.exists(ENC_EDIT_LOG_FILE) and os.path.exists(EDIT_LOG_FILE):
        print(f"🔒 Encrypting original {EDIT_LOG_FILE}...")
        encrypt_file(EDIT_LOG_FILE, ENC_EDIT_LOG_FILE)
        os.remove(EDIT_LOG_FILE)
        print(f"✅ Replaced with {ENC_EDIT_LOG_FILE}")

def load_data():
    """Loads the Excel file by decrypting it first."""
    init_encryption()

    if not os.path.exists(ENC_FILE_PATH):
        print("❌ Error: Encrypted Excel file not found.")
        return None

    try:
        # Decrypt to a temporary file
        temp_file = "temp_patrak.xlsx"
        if not decrypt_file(ENC_FILE_PATH, temp_file):
            return None

        # Load data - Using header=0 to avoid skipping rows unless necessary
        with pd.ExcelFile(temp_file, engine="openpyxl") as xl:
            sheet_name = "Sheet1" if "Sheet1" in xl.sheet_names else xl.sheet_names[0]
            df = pd.read_excel(xl, sheet_name=sheet_name, header=0)
        
        # Clean up unencrypted temp file immediately
        os.remove(temp_file)

        if df.empty:
            print("❌ Error: Excel file is empty.")
            return None
            
        df.fillna("", inplace=True)
        return df
    except Exception as e:
        print("❌ Error loading Encrypted Excel:", e)
        # Attempt cleanup just in case
        if os.path.exists("temp_patrak.xlsx"):
            os.remove("temp_patrak.xlsx")
        return None

def get_excel_data():
    """Returns Excel data as a list of dictionaries for rendering in HTML."""
    df = load_data()
    if df is None or df.empty:
        return []
    return df.to_dict(orient="records")

def save_data(df):
    """Saves the updated DataFrame to an encrypted Excel file."""
    temp_file = "temp_save.xlsx"
    
    # Save unencrypted version temporarily
    df.to_excel(temp_file, index=False, engine="openpyxl")
    
    # Encrypt to real file and delete unencrypted footprint
    encrypt_file(temp_file, ENC_FILE_PATH)
    os.remove(temp_file)

def load_log():
    """Loads the edit log by decrypting it first."""
    if not os.path.exists(ENC_EDIT_LOG_FILE):
        return pd.DataFrame() # Return empty DataFrame if no log config found
        
    try:
        with pd.ExcelFile(temp_file, engine="openpyxl") as xl:
            df = pd.read_excel(xl)
        
        os.remove(temp_file)
        return df
    except Exception as e:
        if os.path.exists("temp_log.xlsx"):
            os.remove("temp_log.xlsx")
        print("❌ Error loading encrypted log:", e)
        return pd.DataFrame()

def save_log(log_df):
    """Saves the log DataFrame to an encrypted Excel file."""
    temp_file = "temp_log_save.xlsx"
    log_df.to_excel(temp_file, index=False, engine="openpyxl")
    encrypt_file(temp_file, ENC_EDIT_LOG_FILE)
    os.remove(temp_file)

def log_edit(username, row, col, old_value, new_value):
    """Logs changes to the encrypted edit_log.enc."""
    log_entry = {
        "Username": username,
        "Row": row,
        "Column": col,
        "Old Value": old_value,
        "New Value": new_value,
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    log_df = load_log()
    
    if log_df.empty:
        log_df = pd.DataFrame([log_entry])
    else:
        log_df = pd.concat([log_df, pd.DataFrame([log_entry])], ignore_index=True)

    save_log(log_df)
    print(f"✅ Change Logged securely: {log_entry}")
