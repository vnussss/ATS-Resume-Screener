# 🪟 Windows Setup Guide for ATS Resume Screener

## Problem: Python 3.13.7 Compatibility Issues

The issue you're facing is that **Python 3.13 is too new** and many ML libraries (spaCy, numpy) don't have pre-built wheels yet. Plus, Windows needs a C++ compiler to build them from source.

## ✅ **Solution 1: Use Python 3.11 (RECOMMENDED)**

This is the easiest and most reliable solution.

### Step 1: Install Python 3.11

1. Download Python 3.11.8 from: https://www.python.org/downloads/release/python-3118/
2. Run the installer
3. ✅ **CHECK** "Add Python to PATH"
4. Click "Install Now"

### Step 2: Create Virtual Environment

```powershell
# Navigate to your project folder
cd C:\Users\drust\OneDrive\Documents\ATS-Resume-Screener

# Create virtual environment with Python 3.11
py -3.11 -m venv venv

# If py -3.11 doesn't work, try:
python -m venv venv

# Activate the virtual environment
.\venv\Scripts\activate

# You should see (venv) in your terminal
```

### Step 3: Install Dependencies

```powershell
# Upgrade pip first
python -m pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt

# This might take 3-5 minutes
```

### Step 4: Download spaCy Language Model

```powershell
python -m spacy download en_core_web_sm
```

### Step 5: Run the Application

```powershell
streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`

---

## ✅ **Solution 2: Fix Python 3.13 (Advanced)**

If you must use Python 3.13, follow these steps:

### Step 1: Install Visual Studio Build Tools

1. Download: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Run the installer
3. Select "Desktop development with C++"
4. Click Install (this takes ~6GB and 30+ minutes)

### Step 2: Use Updated Requirements File

```powershell
# Create virtual environment
python -m venv venv

# Activate
.\venv\Scripts\activate

# Upgrade pip
python -m pip install --upgrade pip

# Use the Python 3.13 compatible requirements
pip install -r requirements-py313.txt

# If that fails, install one by one:
pip install streamlit
pip install pandas numpy
pip install scikit-learn
pip install nltk
pip install PyPDF2 pdfplumber python-docx
pip install plotly matplotlib tqdm

# Install spaCy (might need to build from source)
pip install spacy --no-cache-dir

# Download language model
python -m spacy download en_core_web_sm
```

---

## 🐛 **Troubleshooting**

### Issue: "streamlit: command not found"

**Solution:**
```powershell
# Make sure virtual environment is activated
.\venv\Scripts\activate

# Try running with python -m
python -m streamlit run app.py
```

### Issue: "Import 'streamlit' could not be resolved"

**Solution:**
- Your VS Code is using the wrong Python interpreter
- Press `Ctrl+Shift+P`
- Type "Python: Select Interpreter"
- Choose the one in `venv\Scripts\python.exe`

### Issue: Still getting build errors

**Solution:**
```powershell
# Install pre-built wheels manually
pip install --only-binary :all: numpy pandas scikit-learn

# Then try requirements again
pip install -r requirements.txt
```

---

## 🎯 **Recommended: Quick Start with Python 3.11**

Here's the complete command sequence (copy-paste):

```powershell
# 1. Make sure you're in the project directory
cd C:\Users\drust\OneDrive\Documents\ATS-Resume-Screener

# 2. Create virtual environment (use Python 3.11)
py -3.11 -m venv venv

# 3. Activate
.\venv\Scripts\activate

# 4. Upgrade pip
python -m pip install --upgrade pip

# 5. Install dependencies
pip install -r requirements.txt

# 6. Download spaCy model
python -m spacy download en_core_web_sm

# 7. Run the app
streamlit run app.py
```

---

## 📱 **VS Code Setup**

If using VS Code:

1. Open Command Palette (`Ctrl+Shift+P`)
2. Type "Python: Select Interpreter"
3. Choose `.\venv\Scripts\python.exe`
4. Reload VS Code window
5. The import errors should disappear

---

## ✅ **Verification**

After setup, test if everything works:

```powershell
# Test Python
python --version
# Should show: Python 3.11.x

# Test imports
python -c "import streamlit; print('✅ Streamlit OK')"
python -c "import spacy; print('✅ spaCy OK')"
python -c "import sklearn; print('✅ sklearn OK')"

# If all three print "OK", you're good to go!
```

---

## 🆘 **Still Having Issues?**

### Option A: Use Python 3.10

Download Python 3.10.11 from: https://www.python.org/downloads/release/python-31011/

Then repeat the steps above with `py -3.10 -m venv venv`

### Option B: Use Docker (if you have it)

```powershell
# Build container
docker build -t ats-screener .

# Run
docker run -p 8501:8501 ats-screener
```

---

## 💡 **Why Python 3.13 Doesn't Work**

- **Too New**: Python 3.13 was released in October 2024
- **No Pre-built Wheels**: Libraries like spaCy, numpy need time to build wheels for new Python versions
- **Compiler Required**: Without pre-built wheels, you need Visual Studio C++ compiler (6GB+ install)
- **Best Practice**: Stick with Python 3.10 or 3.11 for ML projects until ecosystem catches up

---

## 🎉 **Expected Result**

After successful setup, you should see:

```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

Then the ATS app will open in your browser! 🚀

---

Need more help? Let me know which error you're getting and I'll help troubleshoot! 💪
