# 🚀 First Time Setup (Simple Guide)

## What You Need
- Python 3.8+ installed on your computer
- Internet connection
- 5 minutes of your time

## Setup Steps (Copy & Paste These Commands)

### 1. Clone Repository
```bash
git clone https://github.com/futureKrishna/Darwix-AI.git
cd Darwix-AI
```

### 2. Create Virtual Environment
```bash
# Windows Users:
python -m venv venv
venv\Scripts\activate

# Mac/Linux Users:
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Everything
```bash
pip install -r requirements.txt
```
*(This takes 2-3 minutes - downloads all the AI libraries)*

### 4. Start the Server
```bash
python fast_run.py
```

## ✅ Success!
If you see this message:
```
🚀 Fast Development Server - Sales Analytics Microservice
Server will start at http://localhost:8000
```

**You're done!** Open http://localhost:8000/docs in your browser.

## Every Time After First Setup

```bash
# 1. Go to project folder
cd Darwix-AI

# 2. Activate environment
venv\Scripts\activate    # Windows
# source venv/bin/activate  # Mac/Linux

# 3. Start server
python fast_run.py

# 4. Open browser: http://localhost:8000/docs
```

## Test Everything Works
```bash
python production_test.py
```
Should show: "🎉 ALL PRODUCTION TESTS PASSED!"

---
**That's it! The setup is complete and tested.**
