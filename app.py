from flask import Flask, render_template, request, redirect, url_for, session, flash
import pyotp
import sqlite3
import os
import qrcode

app = Flask(__name__)
app.secret_key = os.urandom(24)

# ✅ Initialize the database
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        totp_secret TEXT NOT NULL)''')
    conn.commit()
    conn.close()

init_db()

# ✅ Homepage
@app.route('/')
def index():
    return render_template('index.html')

# ✅ Register page with QR code generation
@app.route('/register', methods=['GET', 'POST'])
def register():
    qr_image_path = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        totp_secret = pyotp.random_base32()
        try:
            conn = sqlite3.connect('database.db')
            conn.execute("INSERT INTO users (username, password, totp_secret) VALUES (?, ?, ?)",
                         (username, password, totp_secret))
            conn.commit()

            # ✅ Generate QR code
            uri = pyotp.TOTP(totp_secret).provisioning_uri(name=username, issuer_name="SecureLogin")
            img = qrcode.make(uri)
            qr_image_path = f'static/qrcode_{username}.png'
            img.save(qr_image_path)

            flash("Scan the QR code below using Google Authenticator.", "info")
        except sqlite3.IntegrityError:
            flash("Username already exists", "danger")
        conn.close()
    return render_template('register.html', qr_image=qr_image_path)

# ✅ Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        user = conn.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password)).fetchone()
        conn.close()
        if user:
            session['username'] = username
            session['totp_secret'] = user[3]
            return redirect(url_for('mfa'))
        else:
            flash("Invalid credentials", "danger")
    return render_template('login.html')

# ✅ MFA verification page
@app.route('/mfa', methods=['GET', 'POST'])
def mfa():
    if request.method == 'POST':
        token = request.form['token']
        totp = pyotp.TOTP(session['totp_secret'])
        if totp.verify(token):
            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid 2FA token", "danger")
    return render_template('mfa.html')

# ✅ Protected dashboard
@app.route('/dashboard')
def dashboard():
    return f"✅ Welcome, {session.get('username')}! You are now logged in with MFA."

if __name__ == '__main__':
    app.run(debug=True)
