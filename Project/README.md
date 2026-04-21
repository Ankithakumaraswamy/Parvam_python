# 🔐 PassVault — Password Manager
### Complete Beginner Guide (VS Code)

---

## 📁 Project Structure

```
password-manager/
├── app.py                  ← Flask backend (all your Python logic)
├── vault.json              ← Where passwords are stored
├── requirements.txt        ← Python packages needed
├── test_selenium.py        ← Automated browser test
└── templates/
    └── index.html          ← Your entire frontend UI
```

---

## 🛠️ Step-by-Step Setup in VS Code

### Step 1 — Install Python
1. Go to https://python.org/downloads and download Python 3.10+
2. During install, **tick "Add Python to PATH"** ✅
3. Open a terminal in VS Code: `View → Terminal` (or Ctrl + `)
4. Verify: `python --version` → should print `Python 3.x.x`

---

### Step 2 — Open the project folder in VS Code
1. In VS Code: `File → Open Folder`
2. Select your `password-manager` folder
3. You should see all files in the Explorer panel on the left

---

### Step 3 — Create a virtual environment
In the VS Code terminal, run these commands one by one:

```bash
# Create a virtual environment called "venv"
python -m venv venv

# Activate it  (Windows)
venv\Scripts\activate

# Activate it  (Mac / Linux)
source venv/bin/activate
```

✅ You'll see `(venv)` appear at the start of your terminal line.

---

### Step 4 — Install Flask
```bash
pip install -r requirements.txt
```

This installs Flask (the web framework) from `requirements.txt`.

---

### Step 5 — Run the app
```bash
python app.py
```

You should see:
```
✅ Created empty vault.json
 * Running on http://127.0.0.1:5000
```

---

### Step 6 — Open in browser
Go to: **http://localhost:5000**

You'll see the PassVault UI! 🎉

---

## 🧪 How to Run the Selenium Test

### Step A — Install Selenium
```bash
pip install selenium
```

### Step B — Install ChromeDriver
- Go to: https://chromedriver.chromium.org/downloads
- Download the version that **matches your Chrome browser**
  - Check Chrome version: Chrome → `⋮` → Help → About Google Chrome
- Extract the `chromedriver` file
- Move it to a folder in your PATH (e.g. `C:\Windows\` on Windows)

### Step C — Run the test (keep Flask running in one terminal!)
Open a **second terminal** in VS Code (`+` button in terminal panel):

```bash
# Make sure venv is activated
venv\Scripts\activate   # Windows

# Run the test
python test_selenium.py
```

Expected output:
```
✅ Test 1 PASSED — Password generated with 12 characters
✅ Test 2 PASSED — Strength bar is displayed
✅ Test 3 PASSED — Password field revealed after generation
✅ Test 4 PASSED — Credential saved and appears in vault
✅ Test 5 PASSED — Per-entry show/hide toggle works

🎉 ALL TESTS PASSED!
```

---

## 📖 Understanding the Code

### `app.py` — Flask Backend
| Function | What it does |
|---|---|
| `load_vault()` | Reads `vault.json` into Python dict |
| `save_vault()` | Writes Python dict back to `vault.json` |
| `check_strength()` | Returns "Weak"/"Medium"/"Strong" |
| `generate_password()` | Makes a 12-char random password |
| `GET /api/credentials` | Returns all saved credentials |
| `POST /api/credentials` | Saves a new credential |
| `DELETE /api/credentials/<id>` | Deletes an entry by ID |
| `GET /api/generate-password` | Generates & returns a password |
| `POST /api/check-strength` | Returns strength of a given password |

### `vault.json` — Data Structure
```json
{
  "vault": [
    {
      "id": 1,
      "site": "Gmail",
      "username": "divya@gmail.com",
      "password": "xK#9mLp2Qr!w",
      "strength": "Strong"
    }
  ]
}
```

### `templates/index.html` — Frontend
- Pure HTML + CSS + Vanilla JavaScript
- Calls the Flask API using `fetch()`
- No external JS frameworks needed

---

## 🐛 Common Errors & Fixes

| Error | Fix |
|---|---|
| `ModuleNotFoundError: flask` | Run `pip install flask` |
| `Address already in use` | Another app uses port 5000. Change `app.run(port=5001)` in app.py |
| `chromedriver not found` | Make sure chromedriver is in PATH (see Step B above) |
| `vault.json` shows corrupt data | Delete `vault.json` and restart `app.py` — it recreates it empty |

---

## ✨ Features Summary

- ✅ **Add credentials** — Website, Username, Password
- ✅ **Generate password** — 12-char random, always Strong
- ✅ **Strength meter** — Live colour-coded bar (Weak/Medium/Strong)
- ✅ **Show/hide toggle** — Both in form and per vault entry
- ✅ **Persistent storage** — All data saved to `vault.json`
- ✅ **Delete entries** — Remove any saved credential
- ✅ **Selenium tests** — 5 automated browser checks