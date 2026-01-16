# 📄 ATS Resume Screener

> *Stop losing great candidates in the pile. Let AI help you find them.* 🚀

A modern, AI-powered Applicant Tracking System built by a recent grad who understands the struggle of getting past ATS filters. This tool helps recruiters **quickly identify top candidates** while providing **transparent explanations** for every decision.

## ✨ Features

- 🤖 **Smart NLP Matching** - Uses spaCy and TF-IDF for intelligent resume-JD matching
- 📊 **Multi-Factor Scoring** - Combines content similarity, skill matching, experience, and education
- 🎯 **Transparent Rankings** - Clear explanations for why each resume is selected or rejected
- 💼 **Skill Extraction** - Automatically identifies technical skills and qualifications
- 📈 **Visual Dashboard** - Clean, modern Gen Z aesthetic UI
- 💾 **Export Results** - Download screening results as CSV for further analysis
- 📄 **Multiple Formats** - Supports PDF and DOCX resume uploads

## 🛠️ Tech Stack

**Backend:**
- Python 3.10+
- spaCy (NLP & text processing)
- scikit-learn (TF-IDF, Cosine Similarity)
- NLTK (stopwords, tokenization)

**Resume Parsing:**
- PyPDF2 & pdfplumber (PDF extraction)
- python-docx (DOCX extraction)

**Frontend:**
- Streamlit (modern web UI)
- Plotly (visualizations)

**Data:**
- Pandas (data manipulation)
- CSV export functionality

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd ATS-Resume-Screener
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Download spaCy Model

```bash
python -m spacy download en_core_web_sm
```

### 4. Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📖 How to Use

### Step 1: Upload Job Description
1. Go to the **"📝 Job Description"** tab
2. Either paste your JD text or upload a `.txt` file
3. Click **"🔍 Analyze JD"** to extract requirements

### Step 2: Upload Resumes
1. Navigate to **"📄 Upload Resumes"** tab
2. Upload one or multiple resumes (PDF or DOCX)
3. Click **"🚀 Process Resumes"** to start screening

### Step 3: Review Results
1. Check the **"📊 Results & Rankings"** tab
2. See candidates ranked by match score
3. Read detailed explanations for each candidate
4. Export results as CSV if needed

## 🧮 Scoring Algorithm

The ATS uses a weighted scoring system:

| Component | Weight | Description |
|-----------|--------|-------------|
| **Content Similarity** | 40% | TF-IDF + Cosine similarity between resume and JD |
| **Skill Matching** | 30% | Percentage of required skills found in resume |
| **Experience Level** | 20% | Match between candidate experience and JD requirement |
| **Education** | 10% | Match between candidate qualifications and JD requirement |

### Score Interpretation:

- **75-100**: ✅ **Strong Match** - Recommended for interview
- **60-74**: ⚠️ **Potential Match** - Needs manual review
- **0-59**: ❌ **Not a Strong Match** - May not meet requirements

## 📁 Project Structure

```
ATS-Resume-Screener/
│
├── data/
│   ├── resumes/              # Uploaded resume files
│   └── job_description.txt   # Sample JD
│
├── src/
│   ├── resume_parser.py      # Extract text from PDF/DOCX
│   ├── jd_parser.py          # Parse job descriptions
│   ├── text_preprocessing.py # Clean & normalize text
│   ├── scorer.py             # Calculate similarity scores
│   └── ranker.py             # Rank & explain results
│
├── app.py                     # Main Streamlit application
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🎨 Why This Design?

As a recent graduate navigating the job market, I know how frustrating ATS systems can be. This tool is built with:

- **Transparency**: Every decision is explained
- **Fairness**: Objective, multi-factor scoring
- **Modern UX**: Clean, professional Gen Z aesthetic
- **Speed**: Process dozens of resumes in seconds

## 🔧 Customization

### Modify Scoring Weights

Edit `src/scorer.py`:

```python
overall_score = (
    cosine_score * 0.40 +           # Adjust these weights
    keyword_match['match_score'] * 0.30 +
    experience_match['experience_match_score'] * 0.20 +
    education_match['education_match_score'] * 0.10
)
```

### Add Custom Skills

Edit `src/jd_parser.py`:

```python
self.tech_skills = {
    'languages': ['python', 'java', 'your_skill'],
    # Add your custom categories and skills
}
```

## 📊 Sample Output

```
Candidate Rankings:
#1 - ✅ john_doe_resume.pdf - 87.5/100
   • Strong content alignment (85% similarity)
   • Excellent skill match (12/14 key skills found)
   • Experience requirement met (4 years)
   • Education requirement met

#2 - ⚠️ jane_smith_resume.pdf - 68.3/100
   • Moderate content alignment (72% similarity)
   • Partial skill match (8/14 key skills found)
   • Missing: kubernetes, terraform, graphql
   • Experience gap (2 years, mid-level required)
```

## 🤝 Contributing

Built this as a solo project, but open to contributions! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📝 License

This project is open source and available under the MIT License.

## 💪 Built By a Recent Grad

This tool was created by someone who's been there - sending hundreds of applications, wondering why some got through and others didn't. Now you can make your own ATS that's actually fair and transparent.

**Let's make hiring better, together.** 🚀

---

### 🙏 Acknowledgments

- **spaCy** for amazing NLP capabilities
- **Streamlit** for making beautiful UIs accessible
- **scikit-learn** for powerful ML tools
- **Every recent grad** who's ever struggled with ATS systems

---

<div align="center">
Made with 💜 and a whole lot of job application PTSD
</div>
