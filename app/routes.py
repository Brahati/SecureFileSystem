from flask import render_template, request, redirect, session, send_from_directory
from app.zk_auth import generate_challenge, compute_response, USER_SECRETS
from crypto.pipeline import encrypt_and_embed, extract_and_decrypt
import sqlite3
import os

def setup_routes(app):

    # ---------------- LOGIN ----------------
    @app.route("/", methods=["GET", "POST"])
    def login():

        if request.method == "GET":
            challenge = generate_challenge()
            session["challenge"] = challenge
            return render_template("login.html", challenge=challenge)

        username = request.form["username"]
        response = request.form["response"]

        secret = USER_SECRETS.get(username)
        expected = compute_response(secret, session["challenge"])

        if response == expected:
            session["user"] = username
            return redirect("/dashboard")

        return "❌ Login Failed"


    # ---------------- DASHBOARD ----------------
    @app.route("/dashboard")
    def dashboard():

        conn = sqlite3.connect("instance/users.db")
        c = conn.cursor()

        c.execute("SELECT id, filepath FROM files WHERE receiver=?", (session["user"],))
        files = c.fetchall()

        conn.close()

        return render_template("dashboard.html", user=session["user"], files=files)


    # ---------------- SEND ----------------
    @app.route("/send", methods=["GET", "POST"])
    def send():

        if request.method == "GET":
            return render_template("send.html")

        receiver = request.form["receiver"]
        file = request.files["file"]

        path = f"storage/{session['user']}/sent/{file.filename}"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        file.save(path)

        result = encrypt_and_embed(path, session["user"], receiver)

        conn = sqlite3.connect("instance/users.db")
        c = conn.cursor()

        c.execute("""
        INSERT INTO files (sender, receiver, filepath, payload_length, seed, private_key)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            session["user"],
            receiver,
            result["output_path"],
            result["payload_length"],
            result["seed"],
            result["private_key"]
        ))

        conn.commit()
        conn.close()

        return render_template("result.html", logs=result["logs"], output="File Sent Successfully!")


    # ---------------- RECEIVE ----------------
    @app.route("/receive")
    def receive():

        conn = sqlite3.connect("instance/users.db")
        c = conn.cursor()

        c.execute("SELECT id, filepath FROM files WHERE receiver=?", (session["user"],))
        files = c.fetchall()

        conn.close()

        return render_template("receive.html", files=files)


    # ---------------- DECRYPT ----------------
    @app.route("/decrypt/<int:file_id>")
    def decrypt(file_id):

        conn = sqlite3.connect("instance/users.db")
        c = conn.cursor()

        c.execute("SELECT filepath, payload_length, seed, private_key FROM files WHERE id=?", (file_id,))
        row = c.fetchone()

        conn.close()

        # 🔥 NEW: get structured result
        result, logs = extract_and_decrypt(row[0], row[1], row[2], row[3])

        if not result:
            return render_template("result.html", logs=logs, output="Decryption Failed")

        file_data = result["file_data"]
        filename = result["filename"]

        # 🔥 ensure folder exists
        output_dir = "storage/decrypted"
        os.makedirs(output_dir, exist_ok=True)

        output_path = f"{output_dir}/{filename}"

        # 🔥 save decrypted file
        with open(output_path, "wb") as f:
            f.write(file_data)

        # 🔥 detect file type (for preview)
        is_html = filename.endswith(".html")

        return render_template(
            "result.html",
            logs=logs,
            output="Decryption Successful!",
            file_path=output_path,
            is_html=is_html
        )


    # ---------------- SERVE FILES ----------------
    @app.route('/storage/<path:filename>')
    def serve_file(filename):
        return send_from_directory('storage', filename)


    # ---------------- DELETE ----------------
    @app.route("/delete/<int:file_id>")
    def delete(file_id):

        conn = sqlite3.connect("instance/users.db")
        c = conn.cursor()

        c.execute("SELECT filepath FROM files WHERE id=?", (file_id,))
        row = c.fetchone()

        if row:
            if os.path.exists(row[0]):
                os.remove(row[0])

        c.execute("DELETE FROM files WHERE id=?", (file_id,))
        conn.commit()
        conn.close()

        return redirect("/receive")


    # ---------------- LOGOUT ----------------
    @app.route("/logout")
    def logout():
        session.clear()
        return redirect("/")