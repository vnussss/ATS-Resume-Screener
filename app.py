"""
ATS Resume Screener - Ultra Clean Gen Z Design
Fast, beautiful, and functional
"""

import streamlit as st
from pathlib import Path
import sys

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from src.resume_parser import ResumeParser
from src.jd_parser import JDParser
from src.text_preprocessing import TextPreprocessor
from src.scorer import ResumeScorer
from src.ranker import ResumeRanker

# Page config - MUST BE FIRST
st.set_page_config(
    page_title="ATS Screener",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Clean, modern CSS that WORKS
st.markdown("""
<style>
    /* Import fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Global */
    * {
        font-family: 'Poppins', sans-serif !important;
    }
    
    /* Main app background - Fresh gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    }
    
    /* Content container - Clean white card */
    .main .block-container {
        max-width: 1200px;
        padding: 2rem !important;
        background: white;
        border-radius: 24px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        margin: 2rem auto;
    }
    
    /* Headers - Purple gradient */
    h1 {
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        font-size: 3rem !important;
        margin-bottom: 0.5rem !important;
        letter-spacing: -0.5px;
    }
    
    h2 {
        color: #2d3748 !important;
        font-weight: 700 !important;
        font-size: 1.8rem !important;
        margin-top: 2rem !important;
    }
    
    h3 {
        color: #4a5568 !important;
        font-weight: 600 !important;
        font-size: 1.3rem !important;
    }
    
    /* Tabs - Modern pill style */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: #f7fafc;
        padding: 8px;
        border-radius: 16px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 12px;
        padding: 12px 24px;
        color: #718096;
        font-weight: 600;
        border: none;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
    }
    
    /* Buttons - Vibrant and clickable */
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6) !important;
    }
    
    /* Metrics - Clean cards */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #667eea, #764ba2);
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    [data-testid="stMetricValue"] {
        color: white !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: rgba(255,255,255,0.9) !important;
        font-weight: 500 !important;
    }
    
    /* Text inputs */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 12px !important;
        border: 2px solid #e2e8f0 !important;
        font-size: 1rem !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        border: 2px dashed #667eea !important;
        border-radius: 16px !important;
        padding: 2rem !important;
        background: #f7fafc !important;
    }
    
    /* Radio buttons */
    .stRadio > div {
        background: #f7fafc;
        padding: 1rem;
        border-radius: 12px;
    }
    
    /* Expander - Card style */
    .streamlit-expanderHeader {
        background: #f7fafc !important;
        border-radius: 12px !important;
        border: 2px solid #e2e8f0 !important;
        font-weight: 600 !important;
        padding: 1rem !important;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: #667eea !important;
        background: #edf2f7 !important;
    }
    
    /* Info/Success/Warning boxes */
    .stAlert {
        border-radius: 12px !important;
        border: none !important;
        padding: 1rem !important;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2) !important;
    }
    
    /* Status badges */
    .badge {
        display: inline-block;
        padding: 0.5rem 1.2rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        margin: 0.5rem 0;
    }
    
    .badge-success {
        background: linear-gradient(135deg, #48bb78, #38a169);
        color: white;
        box-shadow: 0 4px 12px rgba(72, 187, 120, 0.3);
    }
    
    .badge-warning {
        background: linear-gradient(135deg, #ed8936, #dd6b20);
        color: white;
        box-shadow: 0 4px 12px rgba(237, 137, 54, 0.3);
    }
    
    .badge-danger {
        background: linear-gradient(135deg, #f56565, #e53e3e);
        color: white;
        box-shadow: 0 4px 12px rgba(245, 101, 101, 0.3);
    }
    
    /* Hero section */
    .hero-text {
        font-size: 1.2rem;
        color: #718096;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #e2e8f0, transparent);
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'resumes_processed' not in st.session_state:
    st.session_state.resumes_processed = []
if 'jd_processed' not in st.session_state:
    st.session_state.jd_processed = None

# Initialize components with spinner
@st.cache_resource(show_spinner=False)
def load_components():
    """Load all ATS components"""
    return {
        'resume_parser': ResumeParser(),
        'jd_parser': JDParser(),
        'preprocessor': TextPreprocessor(),
        'scorer': ResumeScorer(),
        'ranker': ResumeRanker()
    }

with st.spinner("🚀 Loading AI models... (first time takes 10-15 seconds)"):
    components = load_components()

# Hero Section
st.markdown('<h1>✨ ATS Resume Screener</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-text">Stop losing great candidates in the pile. Let AI help you find them. 🚀</p>', unsafe_allow_html=True)

st.markdown("---")

# Tabs
tab1, tab2, tab3 = st.tabs(["📝 Job Description", "📄 Upload Resumes", "📊 Results"])

# TAB 1: Job Description
with tab1:
    st.markdown("## 📝 Step 1: Define Your Job")
    st.write("")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        jd_option = st.radio(
            "Input method:",
            ["✍️ Paste Text", "📁 Upload File"],
            horizontal=True
        )
        
        st.write("")
        
        if jd_option == "✍️ Paste Text":
            jd_text = st.text_area(
                "Job Description:",
                height=300,
                placeholder="Example:\n\nSoftware Engineer - Python\n\nRequired:\n• 3+ years Python\n• Django/Flask\n• AWS experience\n• REST APIs\n\nNice to have:\n• Docker\n• Kubernetes"
            )
            
            if st.button("🔍 Analyze JD"):
                if jd_text.strip():
                    with st.spinner("Analyzing..."):
                        jd_data = components['jd_parser'].parse(jd_text)
                        processed = components['preprocessor'].preprocess(jd_data['text'])
                        jd_data['processed_text'] = processed['lemmatized']
                        jd_data['processed_skills'] = processed['skills']
                        st.session_state.jd_processed = jd_data
                        st.success("✅ Done!")
                        st.balloons()
                else:
                    st.warning("⚠️ Please paste a job description")
        else:
            jd_file = st.file_uploader("Upload TXT file:", type=['txt'])
            
            if jd_file:
                if st.button("🔍 Analyze JD"):
                    with st.spinner("Analyzing..."):
                        jd_text = jd_file.read().decode('utf-8')
                        jd_data = components['jd_parser'].parse(jd_text)
                        processed = components['preprocessor'].preprocess(jd_data['text'])
                        jd_data['processed_text'] = processed['lemmatized']
                        jd_data['processed_skills'] = processed['skills']
                        st.session_state.jd_processed = jd_data
                        st.success("✅ Done!")
                        st.balloons()
    
    with col2:
        st.info("""
        **💡 Tips:**
        
        ✅ List requirements  
        ✅ Include skills  
        ✅ Specify experience  
        ✅ Mention education
        """)
    
    # Show results
    if st.session_state.jd_processed:
        st.write("")
        st.markdown("### 📊 Analysis")
        
        jd_data = st.session_state.jd_processed
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Words", f"{jd_data['word_count']:,}")
        with col2:
            st.metric("Skills", jd_data['total_skills_count'])
        with col3:
            st.metric("Level", jd_data['experience_level'].title())
        with col4:
            st.metric("Education", len(jd_data.get('qualifications', [])))
        
        with st.expander("🔧 Extracted Skills"):
            for category, skills in jd_data['skills'].items():
                if skills:
                    st.write(f"**{category.title()}:** {', '.join(skills)}")

# TAB 2: Upload Resumes
with tab2:
    st.markdown("## 📄 Step 2: Upload Resumes")
    st.write("")
    
    if not st.session_state.jd_processed:
        st.warning("⚠️ Please analyze a Job Description first")
    else:
        st.info("📤 Upload multiple files (PDF, DOCX)")
        
        uploaded_files = st.file_uploader(
            "Choose files:",
            type=['pdf', 'docx', 'doc'],
            accept_multiple_files=True
        )
        
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} file(s) ready")
            
            if st.button("🚀 Process All"):
                progress = st.progress(0)
                status = st.empty()
                
                processed_resumes = []
                total = len(uploaded_files)
                
                for idx, file in enumerate(uploaded_files):
                    status.text(f"Processing {file.name}... ({idx+1}/{total})")
                    progress.progress((idx + 1) / total)
                    
                    # Save temp
                    temp_path = Path("data/resumes") / file.name
                    temp_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(temp_path, 'wb') as f:
                        f.write(file.read())
                    
                    # Parse
                    resume_data = components['resume_parser'].parse(str(temp_path))
                    
                    if resume_data['success']:
                        processed = components['preprocessor'].preprocess(resume_data['text'])
                        resume_data['processed_text'] = processed['lemmatized']
                        resume_data['skills'] = processed['skills']
                        
                        score_data = components['scorer'].calculate_overall_score(
                            resume_data,
                            st.session_state.jd_processed
                        )
                        
                        processed_resumes.append({**resume_data, **score_data})
                
                # Rank
                ranked = components['ranker'].rank_resumes(processed_resumes)
                st.session_state.resumes_processed = ranked
                
                status.empty()
                progress.empty()
                
                st.success(f"✅ Processed {len(ranked)} resumes!")
                st.balloons()

# TAB 3: Results
with tab3:
    st.markdown("## 📊 Step 3: Results")
    st.write("")
    
    if not st.session_state.resumes_processed:
        st.info("📊 Process resumes to see results")
    else:
        resumes = st.session_state.resumes_processed
        
        # Stats
        col1, col2, col3, col4 = st.columns(4)
        
        total = len(resumes)
        selected = sum(1 for r in resumes if r['status'] == 'selected')
        review = sum(1 for r in resumes if r['status'] == 'review')
        rejected = sum(1 for r in resumes if r['status'] == 'rejected')
        
        with col1:
            st.metric("Total", total)
        with col2:
            st.metric("✅ Strong", selected)
        with col3:
            st.metric("⚠️ Review", review)
        with col4:
            st.metric("❌ Weak", rejected)
        
        st.markdown("---")
        
        # Rankings
        st.markdown("### 🏆 Rankings")
        
        for resume in resumes:
            rank = resume['rank']
            name = resume['file_name']
            score = resume['overall_score']
            status = resume['status']
            
            if status == 'selected':
                badge = '<span class="badge badge-success">✅ STRONG MATCH</span>'
                emoji = "🌟"
            elif status == 'review':
                badge = '<span class="badge badge-warning">⚠️ REVIEW</span>'
                emoji = "🤔"
            else:
                badge = '<span class="badge badge-danger">❌ WEAK</span>'
                emoji = "📉"
            
            with st.expander(f"#{rank} {emoji} {name} - {score:.1f}/100", expanded=(rank <= 2)):
                st.markdown(badge, unsafe_allow_html=True)
                st.write("")
                
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    breakdown = resume['breakdown']
                    st.metric("Overall", f"{score:.1f}/100")
                    st.metric("Content", f"{breakdown['cosine_similarity']:.1f}%")
                    st.metric("Skills", f"{breakdown['keyword_match']['match_score']:.1f}%")
                    st.metric("Experience", f"{breakdown['experience_match']['experience_match_score']:.0f}%")
                
                with col2:
                    explanation = components['ranker'].generate_explanation(resume, resume)
                    st.markdown(explanation)
        
        st.markdown("---")
        
        # Export
        st.markdown("### 💾 Export")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Download CSV"):
                csv_path = "data/results.csv"
                components['ranker'].export_to_csv(resumes, csv_path)
                with open(csv_path, 'rb') as f:
                    st.download_button("⬇️ Download", f, "results.csv", "text/csv")
        
        with col2:
            if st.button("📄 Report"):
                report = components['ranker'].generate_summary_report(resumes)
                st.markdown(report)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #718096;'>
    <p><strong>ATS Resume Screener</strong> - Built by a recent grad 💜</p>
    <p style='font-size: 0.9rem;'>Python • spaCy • Streamlit</p>
</div>
""", unsafe_allow_html=True)
