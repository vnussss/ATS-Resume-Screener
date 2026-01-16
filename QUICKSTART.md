# 🚀 Quick Start Guide

## Installation (5 minutes)

### Option 1: Automated Setup (Recommended)

```bash
# Run the setup script
./setup.sh
```

This will:
- Create a virtual environment
- Install all dependencies
- Download required NLP models
- Set up project directories

### Option 2: Manual Setup

```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download spaCy model
python -m spacy download en_core_web_sm

# 5. Download NLTK data
python -c "import nltk; nltk.download('stopwords')"
```

## Running the App

```bash
# Make sure virtual environment is activated
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run Streamlit
streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`

## First-Time Usage

### 1. Prepare Your Job Description
Create a text file or prepare to paste your JD. Include:
- Job title and overview
- Required skills (must-haves)
- Nice-to-have skills
- Experience level required
- Education requirements

### 2. Prepare Resume Files
- Supported formats: PDF, DOCX
- Can upload multiple files at once
- Files should be actual resumes (not scanned images)

### 3. Using the App

**Step 1: Upload JD**
- Go to "📝 Job Description" tab
- Paste text or upload TXT file
- Click "🔍 Analyze JD"
- Review extracted skills and requirements

**Step 2: Upload Resumes**
- Go to "📄 Upload Resumes" tab
- Select one or more resume files
- Click "🚀 Process Resumes"
- Wait for processing to complete

**Step 3: Review Results**
- Go to "📊 Results & Rankings" tab
- See candidates ranked by score
- Read detailed explanations
- Export to CSV if needed

## Troubleshooting

### "Module not found" error
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### "spaCy model not found" error
```bash
python -m spacy download en_core_web_sm
```

### PDF parsing issues
- Make sure PDF is text-based (not scanned image)
- Try converting to DOCX and uploading again
- Check if PDF is password-protected

### Low scores for good candidates
- Review JD for clarity and completeness
- Ensure technical skills are explicitly listed
- Check if resume uses similar terminology as JD

## Tips for Best Results

### For Job Descriptions:
✅ Be specific about required skills
✅ Use standard tech terminology (e.g., "Python" not "py")
✅ Include experience level (e.g., "3+ years")
✅ Mention education requirements clearly

### For Resumes:
✅ Use standard section headers (Experience, Education, Skills)
✅ Include years of experience explicitly
✅ List technical skills clearly
✅ Use industry-standard terminology

## Advanced Usage

### Adjusting Score Weights

Edit `src/scorer.py`, line ~290:

```python
overall_score = (
    cosine_score * 0.40 +                          # Content similarity
    keyword_match['match_score'] * 0.30 +          # Skill matching
    experience_match['experience_match_score'] * 0.20 +  # Experience
    education_match['education_match_score'] * 0.10      # Education
)
```

Change the weights (must add up to 1.0) based on your priorities.

### Adding Custom Skills

Edit `src/jd_parser.py`, line ~20:

```python
self.tech_skills = {
    'languages': ['python', 'java', 'javascript', 'your_skill_here'],
    'frameworks': ['react', 'django', 'your_framework_here'],
    # Add more categories as needed
}
```

### Batch Processing

For processing many resumes:
1. Place all resumes in `data/resumes/` folder
2. Upload them all at once in the UI
3. Export results to CSV for further analysis

## Getting Help

- Check `README.md` for detailed documentation
- Review code comments in `src/` directory
- Open an issue on GitHub (if applicable)

## Next Steps

- Customize scoring weights for your needs
- Add your specific industry skills to the parser
- Export and analyze results in your preferred tool
- Integrate with your existing HR workflow

---

Happy screening! 🎉
