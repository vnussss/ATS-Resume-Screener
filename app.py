"""
ATS Resume Screener - Main Application
A modern, Gen Z/Gen Alpha aesthetic ATS system
"""

import streamlit as st
from pathlib import Path
import sys
import os

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from src.resume_parser import ResumeParser
from src.jd_parser import JDParser
from src.text_preprocessing import TextPreprocessor
from src.scorer import ResumeScorer
from src.ranker import ResumeRanker

# Page config
st.set_page_config(
    page_title="ATS Resume Screener",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Gen Z/Gen Alpha Professional Aesthetic
st.markdown("""
<style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    .block-container {
        padding: 2rem 3rem;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        margin: 2rem auto;
        max-width: 1400px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
    }
    
    /* Headers */
    h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    
    h2 {
        color: #1a202c;
        font-weight: 700;
        font-size: 1.8rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    h3 {
        color: #2d3748;
        font-weight: 600;
        font-size: 1.4rem;
    }
    
    /* Cards */
    .stMetric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .stMetric label {
        color: white !important;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: white !important;
        font-size: 2rem;
        font-weight: 700;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* File uploader */
    .stFileUploader {
        background: #f7fafc;
        border: 2px dashed #667eea;
        border-radius: 15px;
        padding: 2rem;
    }
    
    /* Text area */
    .stTextArea textarea {
        border: 2px solid #e2e8f0;
        border-radius: 10px;
        font-size: 1rem;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: white;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Info boxes */
    .stAlert {
        border-radius: 10px;
        border-left: 5px solid #667eea;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #f7fafc;
        border-radius: 10px;
        font-weight: 600;
    }
    
    /* Dataframe */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Custom badge styles */
    .badge {
        display: inline-block;
        padding: 0.35rem 0.8rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        margin: 0.2rem;
    }
    
    .badge-selected {
        background: #48bb78;
        color: white;
    }
    
    .badge-review {
        background: #ed8936;
        color: white;
    }
    
    .badge-rejected {
        background: #f56565;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'resumes_processed' not in st.session_state:
    st.session_state.resumes_processed = []
if 'jd_processed' not in st.session_state:
    st.session_state.jd_processed = None

# Initialize components
@st.cache_resource
def load_components():
    """Load all ATS components (cached)"""
    return {
        'resume_parser': ResumeParser(),
        'jd_parser': JDParser(),
        'preprocessor': TextPreprocessor(),
        'scorer': ResumeScorer(),
        'ranker': ResumeRanker()
    }

components = load_components()

# Sidebar
with st.sidebar:
    st.markdown("## 📄 ATS Resume Screener")
    st.markdown("*by a recent grad, for recent grads* 💪")
    
    st.markdown("---")
    
    st.markdown("### 🎯 How it works:")
    st.markdown("""
    1. **Upload** your Job Description
    2. **Drop** candidate resumes
    3. **Get** instant AI rankings
    4. **Understand** why each resume was selected/rejected
    """)
    
    st.markdown("---")
    
    st.markdown("### 💡 Features:")
    st.markdown("""
    - 🤖 NLP-powered matching
    - 📊 Smart skill extraction
    - 🎯 Cosine similarity scoring
    - 📈 Detailed explanations
    - 💾 Export results (CSV)
    """)
    
    st.markdown("---")
    st.markdown("### 📱 Built with:")
    st.markdown("Python • spaCy • Streamlit")
    st.markdown("TF-IDF • Scikit-learn")

# Main content
st.title("📄 ATS Resume Screener")
st.markdown("### Stop losing great candidates in the pile. Let AI help you find them. 🚀")

st.markdown("---")

# Tab navigation
tab1, tab2, tab3 = st.tabs(["📝 Job Description", "📄 Upload Resumes", "📊 Results & Rankings"])

# Tab 1: Job Description
with tab1:
    st.header("Step 1: Define Your Job Requirements")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        jd_option = st.radio(
            "How do you want to provide the JD?",
            ["✍️ Paste Text", "📁 Upload File"],
            horizontal=True
        )
        
        if jd_option == "✍️ Paste Text":
            jd_text = st.text_area(
                "Paste Job Description here:",
                height=300,
                placeholder="Paste your complete job description here...\n\nExample:\nSoftware Engineer - Python\n\nRequired:\n- 3+ years Python experience\n- Django/Flask\n- AWS\n..."
            )
            
            if st.button("🔍 Analyze JD", key="analyze_jd_text"):
                if jd_text.strip():
                    with st.spinner("Analyzing job description..."):
                        # Parse JD
                        jd_data = components['jd_parser'].parse(jd_text)
                        
                        # Preprocess
                        processed = components['preprocessor'].preprocess(jd_data['text'])
                        jd_data['processed_text'] = processed['lemmatized']
                        jd_data['processed_skills'] = processed['skills']
                        
                        st.session_state.jd_processed = jd_data
                        st.success("✅ Job description analyzed successfully!")
                else:
                    st.warning("⚠️ Please paste a job description first")
        
        else:
            jd_file = st.file_uploader(
                "Upload Job Description (TXT file):",
                type=['txt'],
                help="Upload a text file containing the job description"
            )
            
            if jd_file and st.button("🔍 Analyze JD", key="analyze_jd_file"):
                with st.spinner("Analyzing job description..."):
                    # Read file
                    jd_text = jd_file.read().decode('utf-8')
                    
                    # Parse JD
                    jd_data = components['jd_parser'].parse(jd_text)
                    
                    # Preprocess
                    processed = components['preprocessor'].preprocess(jd_data['text'])
                    jd_data['processed_text'] = processed['lemmatized']
                    jd_data['processed_skills'] = processed['skills']
                    
                    st.session_state.jd_processed = jd_data
                    st.success("✅ Job description analyzed successfully!")
    
    with col2:
        st.markdown("### 💡 Pro Tips")
        st.info("""
        **For best results:**
        
        ✅ Include clear requirements
        
        ✅ List must-have skills
        
        ✅ Specify experience level
        
        ✅ Mention education needs
        """)
    
    # Show JD analysis if available
    if st.session_state.jd_processed:
        st.markdown("---")
        st.subheader("📊 JD Analysis Results")
        
        jd_data = st.session_state.jd_processed
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📝 Word Count", jd_data['word_count'])
        with col2:
            st.metric("🔧 Skills Found", jd_data['total_skills_count'])
        with col3:
            st.metric("👔 Experience Level", jd_data['experience_level'].title())
        with col4:
            qualifications = len(jd_data.get('qualifications', []))
            st.metric("🎓 Qualifications", qualifications)
        
        # Show extracted skills
        with st.expander("🔧 View Extracted Skills"):
            skills_data = jd_data['skills']
            
            for category, skills in skills_data.items():
                if skills:
                    st.markdown(f"**{category.title()}:**")
                    st.write(", ".join(skills))

# Tab 2: Upload Resumes
with tab2:
    st.header("Step 2: Upload Candidate Resumes")
    
    if not st.session_state.jd_processed:
        st.warning("⚠️ Please analyze a Job Description first (Step 1)")
    else:
        st.info("📤 Upload multiple resumes at once. Supported formats: PDF, DOCX")
        
        uploaded_files = st.file_uploader(
            "Choose resume files:",
            type=['pdf', 'docx', 'doc'],
            accept_multiple_files=True,
            help="Upload one or more resumes in PDF or DOCX format"
        )
        
        if uploaded_files and st.button("🚀 Process Resumes", key="process_resumes"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            processed_resumes = []
            total_files = len(uploaded_files)
            
            for idx, uploaded_file in enumerate(uploaded_files):
                status_text.text(f"Processing {uploaded_file.name}... ({idx + 1}/{total_files})")
                
                # Save temporarily
                temp_path = Path("data/resumes") / uploaded_file.name
                temp_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(temp_path, 'wb') as f:
                    f.write(uploaded_file.read())
                
                # Parse resume
                resume_data = components['resume_parser'].parse(str(temp_path))
                
                if resume_data['success']:
                    # Preprocess
                    processed = components['preprocessor'].preprocess(resume_data['text'])
                    resume_data['processed_text'] = processed['lemmatized']
                    resume_data['skills'] = processed['skills']
                    
                    # Score against JD
                    score_data = components['scorer'].calculate_overall_score(
                        resume_data,
                        st.session_state.jd_processed
                    )
                    
                    # Merge data
                    resume_result = {**resume_data, **score_data}
                    processed_resumes.append(resume_result)
                
                progress_bar.progress((idx + 1) / total_files)
            
            # Rank resumes
            ranked_resumes = components['ranker'].rank_resumes(processed_resumes)
            st.session_state.resumes_processed = ranked_resumes
            
            status_text.empty()
            progress_bar.empty()
            
            st.success(f"✅ Processed {len(ranked_resumes)} resumes successfully!")
            st.balloons()

# Tab 3: Results
with tab3:
    st.header("Step 3: Review Results & Rankings")
    
    if not st.session_state.resumes_processed:
        st.info("📊 Process some resumes first to see results here")
    else:
        ranked_resumes = st.session_state.resumes_processed
        
        # Summary metrics
        st.subheader("📈 Quick Stats")
        col1, col2, col3, col4 = st.columns(4)
        
        total = len(ranked_resumes)
        selected = sum(1 for r in ranked_resumes if r['status'] == 'selected')
        review = sum(1 for r in ranked_resumes if r['status'] == 'review')
        rejected = sum(1 for r in ranked_resumes if r['status'] == 'rejected')
        
        with col1:
            st.metric("📄 Total Resumes", total)
        with col2:
            st.metric("✅ Strong Matches", selected)
        with col3:
            st.metric("⚠️ Need Review", review)
        with col4:
            st.metric("❌ Not Strong Match", rejected)
        
        st.markdown("---")
        
        # Rankings
        st.subheader("🏆 Candidate Rankings")
        
        for resume in ranked_resumes:
            rank = resume['rank']
            name = resume['file_name']
            score = resume['overall_score']
            status = resume['status']
            
            # Status badge styling
            if status == 'selected':
                badge_class = "badge-selected"
                status_emoji = "✅"
                status_text = "STRONG MATCH"
            elif status == 'review':
                badge_class = "badge-review"
                status_emoji = "⚠️"
                status_text = "REVIEW NEEDED"
            else:
                badge_class = "badge-rejected"
                status_emoji = "❌"
                status_text = "NOT STRONG MATCH"
            
            with st.expander(f"#{rank} - {status_emoji} {name} - {score:.1f}/100", expanded=(rank <= 3)):
                # Score breakdown
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.markdown(f'<span class="badge {badge_class}">{status_text}</span>', 
                              unsafe_allow_html=True)
                    st.metric("Overall Score", f"{score:.1f}/100")
                    
                    breakdown = resume['breakdown']
                    st.metric("Content Match", f"{breakdown['cosine_similarity']:.1f}%")
                    st.metric("Skills Match", f"{breakdown['keyword_match']['match_score']:.1f}%")
                    st.metric("Experience", f"{breakdown['experience_match']['experience_match_score']:.0f}%")
                
                with col2:
                    # Generate explanation
                    explanation = components['ranker'].generate_explanation(resume, resume)
                    st.markdown(explanation)
        
        st.markdown("---")
        
        # Export options
        st.subheader("💾 Export Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Download as CSV"):
                csv_path = "data/screening_results.csv"
                success = components['ranker'].export_to_csv(ranked_resumes, csv_path)
                
                if success:
                    with open(csv_path, 'rb') as f:
                        st.download_button(
                            "⬇️ Click to Download CSV",
                            f,
                            file_name="ats_screening_results.csv",
                            mime="text/csv"
                        )
        
        with col2:
            if st.button("📄 Generate Summary Report"):
                report = components['ranker'].generate_summary_report(ranked_resumes)
                st.markdown(report)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #718096; padding: 2rem;'>
    <p><strong>ATS Resume Screener</strong> - Built with 💜 by a recent grad who gets the struggle</p>
    <p style='font-size: 0.9rem;'>Powered by Python, spaCy, and determination</p>
</div>
""", unsafe_allow_html=True)
