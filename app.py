from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file
import pandas as pd
import os
from user_handler import check_user_credentials, add_new_user, initialize_user_file
from excel_handler import get_excel_data, load_data, save_data, log_edit

app = Flask(__name__)
app.secret_key = "supersecretkey"

# ✅ Ensure Users File Exists
initialize_user_file()


# ✅ Home Route (Redirect to Dashboard or Login)
@app.route("/")
def home():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


# ✅ User Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = check_user_credentials(username, password)

        if role:
            session["user"] = username
            session["role"] = role
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="❌ Invalid Credentials")

    return render_template("login.html")


# ✅ User Registration
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        if add_new_user(username, password, role):
            return redirect(url_for("login"))
        else:
            return render_template("register.html", error="❌ User already exists!")

    return render_template("register.html")


# ✅ Dashboard (Shows Excel Preview)
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    table_data = get_excel_data()
    return render_template("dashboard.html", user=session["user"], role=session["role"], table=table_data)


# ✅ View & Edit Excel File (For Teachers/Admins)
@app.route("/excel")
def view_excel():
    if "user" not in session:
        return redirect(url_for("login"))

    table_data = get_excel_data()
    return render_template("edit_excel.html", table=table_data)


# ✅ Edit Excel File (Save Changes)
@app.route("/excel/edit", methods=["POST"])
def update_excel():
    if "user" not in session:
        return jsonify({"success": False, "error": "Unauthorized"}), 403

    try:
        updates = request.form.to_dict(flat=False)
        df = load_data()
        if df is None:
            return jsonify({"success": False, "error": "Excel file not found"})

        for i in range(len(updates["row"])):
            row = int(updates["row"][i])
            col = int(updates["col"][i])
            new_value = updates["value"][i]
            username = session["user"]

            old_value = df.iloc[row, col]
            df.iloc[row, col] = new_value
            log_edit(username, row, col, old_value, new_value)

        save_data(df)

        return jsonify({"success": True, "message": "✅ Excel updated successfully!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ✅ View Edit Log (For Admins)
@app.route("/log")
def view_log():
    if "user" not in session or session["role"] != "Admin":
        return redirect(url_for("login"))

    log_file = "edit_log.xlsx"
    if os.path.exists(log_file):
        log_df = pd.read_excel(log_file, engine="openpyxl")
        logs = log_df.to_dict(orient="records")
        edit_map = {(row["Row"], row["Column"]): row["Username"] for row in logs}
    else:
        logs = []
        edit_map = {}

    table_data = get_excel_data()
    return render_template("view_log.html", logs=logs, table=table_data, edit_map=edit_map)


# ✅ Route to Download Updated Excel File
@app.route("/download")
def download_excel():
    updated_file = "Updated_Patrak.xlsx"
    df = load_data()

    if df is not None:
        df.to_excel(updated_file, index=False, engine="openpyxl")
        return send_file(updated_file, as_attachment=True)

    return "❌ Error: No updated file found.", 404


# ✅ User Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ✅ Run Flask
if __name__ == "__main__":
    app.run(debug=True)
