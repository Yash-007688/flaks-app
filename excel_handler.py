import pandas as pd
import os
from datetime import datetime

FILE_PATH = "पत्रक 2025-26.xlsx"
EDIT_LOG_FILE = "edit_log.xlsx"

def load_data():
    """Loads the Excel file."""
    if not os.path.exists(FILE_PATH):
        print("❌ Error: Excel file not found.")
        return None

    try:
        df = pd.read_excel(FILE_PATH, engine="openpyxl", sheet_name="Sheet1", header=1)
        if df.empty:
            print("❌ Error: Excel file is empty.")
            return None
        df.fillna("", inplace=True)  # ✅ Replace NaN with empty string
        return df
    except Exception as e:
        print("❌ Error loading Excel:", e)
        return None

def get_excel_data():
    """Returns Excel data as a list of dictionaries for rendering in HTML."""
    df = load_data()
    if df is None or df.empty:
        return []
    return df.to_dict(orient="records")  # ✅ Convert DataFrame to list of dictionaries

def save_data(df):
    """Saves the updated DataFrame to the Excel file."""
    df.to_excel(FILE_PATH, index=False, engine="openpyxl")

def log_edit(username, row, col, old_value, new_value):
    """Logs changes to the Excel file in edit_log.xlsx."""
    log_entry = {
        "Username": username,
        "Row": row,
        "Column": col,
        "Old Value": old_value,
        "New Value": new_value,
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    if os.path.exists(EDIT_LOG_FILE):
        log_df = pd.read_excel(EDIT_LOG_FILE, engine="openpyxl")
        log_df = pd.concat([log_df, pd.DataFrame([log_entry])], ignore_index=True)
    else:
        log_df = pd.DataFrame([log_entry])

    log_df.to_excel(EDIT_LOG_FILE, index=False, engine="openpyxl")
    print(f"✅ Change Logged: {log_entry}")
