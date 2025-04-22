# 🔐 Secure Login with MFA using Flask

This project demonstrates a secure login system that uses:
- **Username + Password**
- **Google Authenticator 2FA (MFA)**
- Built with **Python Flask**, **SQLite**, **pyotp**, and **qrcode**

---

## 🚀 Features

✅ User registration  
✅ QR code generation for MFA (compatible with Google Authenticator)  
✅ Secure login flow  
✅ 2FA verification with one-time tokens  
✅ SQLite database backend  
✅ Flask session handling  

---

## 🧪 How It Works

1. Register a user with username & password
2. A QR code appears — scan it using your Google Authenticator app
3. Login using username & password
4. Enter the 6-digit code from your app to complete login (MFA)

---

## 💻 Project Setup

```bash
git clone https://github.com/FarahMae/secure-login-mfa.git
cd secure-login-mfa
pip3 install flask pyotp qrcode
python3 app.py
