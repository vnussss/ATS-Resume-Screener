#!/bin/bash

echo "🚀 Setting up ATS Resume Screener..."
echo ""

# Check Python version
echo "📌 Checking Python version..."
python3 --version

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo ""
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo ""
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Download spaCy model
echo ""
echo "🔽 Downloading spaCy English model..."
python -m spacy download en_core_web_sm

# Download NLTK data
echo ""
echo "📚 Downloading NLTK data..."
python -c "import nltk; nltk.download('stopwords', quiet=True)"

# Create necessary directories
echo ""
echo "📁 Creating project directories..."
mkdir -p data/resumes
mkdir -p static/assets

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎉 You're ready to go! Run the app with:"
echo "   streamlit run app.py"
echo ""
