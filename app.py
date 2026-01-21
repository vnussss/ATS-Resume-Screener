"""
ATS Resume Screener - ULTRA MODERN Gen Z/Gen Alpha Design
Beautiful, clean, and professional
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
    page_title="ATS Screener 💜",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'About': "Built by a recent grad who gets the struggle 💪"
    }
)

# Ultra-modern CSS with better compatibility
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Root variables */
    :root {
        --primary: #8b5cf6;
        --secondary: #ec4899;
        --dark: #1e1b4b;
        --light: #f8fafc;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main app background - Dark mode vibes */
    .stApp {
        background: linear-gradient(to bottom right, #1e1b4b, #312e81, #1e1b4b);
        background-attachment: fixed;
    }
    
    /* Main content container */
    .main .block-container {
        padding: 3rem 2rem !important;
        max-width: 1400px;
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    }
    
    /* Typography */
    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif !important;
        color: white !important;
        letter-spacing: -0.02em;
    }
    
    h1 {
        font-size: 3.5rem !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem !important;
    }
    
    h2 {
        font-size: 2rem !important;
        font-weight: 600 !important;
        margin-top: 2rem !important;
    }
    
    h3 {
        font-size: 1.5rem !important;
        font-weight: 500 !important;
    }
    
    p, div, span, label {
        font-family: 'Inter', sans-serif !important;
        color: rgba(255, 255, 255, 0.9) !important;
    }
    
    /* Tabs - Modern design */
    .stTabs {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 12px 24px;
        color: rgba(255, 255, 255, 0.6);
        font-weight: 500;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%);
        color: white !important;
        box-shadow: 0 10px 25px -5px rgba(139, 92, 246, 0.4);
    }
    
    /* Buttons - Glassmorphism style */
    .stButton > button {
        background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%);
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 10px 25px -5px rgba(139, 92, 246, 0.4);
        font-family: 'Inter', sans-serif !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 20px 40px -10px rgba(139, 92, 246, 0.6);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Metrics - Card style */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        color: white !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: rgba(255, 255, 255, 0.7) !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
    }
    
    [data-testid="stMetricDelta"] {
        color: #10b981 !important;
    }
    
    /* Metric containers */
    [data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.05);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Text input & textarea */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 2px solid rgba(139, 92, 246, 0.3) !important;
        border-radius: 12px !important;
        color: white !important;
        font-family: 'Inter', sans-serif !important;
        padding: 12px !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #8b5cf6 !important;
        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.2) !important;
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.05);
        border: 2px dashed rgba(139, 92, 246, 0.5);
        border-radius: 16px;
        padding: 2rem;
    }
    
    [data-testid="stFileUploader"] section {
        border: none;
        background: transparent;
    }
    
    [data-testid="stFileUploader"] section > button {
        background: rgba(139, 92, 246, 0.2);
        color: white;
        border-radius: 8px;
    }
    
    /* Radio buttons */
    .stRadio > div {
        background: rgba(255, 255, 255, 0.05);
        padding: 1rem;
        border-radius: 12px;
    }
    
    .stRadio label {
        color: rgba(255, 255, 255, 0.9) !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: white !important;
        font-weight: 600;
        padding: 1rem !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(139, 92, 246, 0.5);
    }
    
    .streamlit-expanderContent {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 0 0 12px 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-top: none;
    }
    
    /* Info/Warning/Success boxes */
    .stAlert {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        border-left: 4px solid #8b5cf6;
        backdrop-filter: blur(10px);
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #8b5cf6 0%, #ec4899 100%);
        border-radius: 8px;
    }
    
    /* Columns */
    [data-testid="column"] {
        padding: 0.5rem;
    }
    
    /* Custom badge styles */
    .status-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        margin: 0.5rem 0;
        letter-spacing: 0.02em;
    }
    
    .badge-selected {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
    }
    
    .badge-review {
        background: linear-gradient(135deg, #f59e0b, #d97706);
        color: white;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
    }
    
    .badge-rejected {
        background: linear-gradient(135deg, #ef4444, #dc2626);
        color: white;
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
    }
    
    /* Hero section */
    .hero-subtitle {
        font-size: 1.25rem;
        color: rgba(255, 255, 255, 0.7);
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Dividers */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(139, 92, 246, 0.5), transparent);
        margin: 2rem 0;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #8b5cf6, #ec4899);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #7c3aed, #db2777);
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
    with st.spinner("🚀 Loading AI models..."):
        return {
            'resume_parser': ResumeParser(),
            'jd_parser': JDParser(),
            'preprocessor': TextPreprocessor(),
            'scorer': ResumeScorer(),
            'ranker': ResumeRanker()
        }

components = load_components()

# Hero Section
st.markdown('<h1>✨ ATS Resume Screener</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-subtitle">Stop losing great candidates in the pile. Let AI help you find them. 🚀</p>',
    unsafe_allow_html=True
)

st.markdown("---")

# Tab navigation with emojis
tab1, tab2, tab3 = st.tabs([
    "📝 Job Description",
    "📄 Upload Resumes", 
    "📊 Results & Rankings"
])

# Tab 1: Job Description
with tab1:
    st.markdown("## Step 1: Define Your Job Requirements")
    st.markdown("")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        jd_option = st.radio(
            "How do you want to provide the JD?",
            ["✍️ Paste Text", "📁 Upload File"],
            horizontal=True,
            label_visibility="collapsed"
        )
        
        st.markdown("")
        
        if jd_option == "✍️ Paste Text":
            jd_text = st.text_area(
                "Paste Job Description",
                height=350,
                placeholder="📋 Paste your complete job description here...\n\nExample:\n\n🎯 Software Engineer - Python\n\nRequired:\n• 3+ years Python experience\n• Django/Flask framework\n• AWS cloud services\n• REST API development\n\nNice to have:\n• Docker & Kubernetes\n• CI/CD experience",
                label_visibility="collapsed"
            )
            
            st.markdown("")
            
            if st.button("🔍 Analyze Job Description", use_container_width=True):
                if jd_text.strip():
                    with st.spinner("🤖 Analyzing requirements with AI..."):
                        # Parse JD
                        jd_data = components['jd_parser'].parse(jd_text)
                        
                        # Preprocess
                        processed = components['preprocessor'].preprocess(jd_data['text'])
                        jd_data['processed_text'] = processed['lemmatized']
                        jd_data['processed_skills'] = processed['skills']
                        
                        st.session_state.jd_processed = jd_data
                        st.success("✅ Job description analyzed successfully!")
                        st.balloons()
                else:
                    st.warning("⚠️ Please paste a job description first")
        
        else:
            jd_file = st.file_uploader(
                "Upload Job Description",
                type=['txt'],
                help="Upload a text file containing the job description",
                label_visibility="collapsed"
            )
            
            st.markdown("")
            
            if jd_file:
                if st.button("🔍 Analyze Job Description", use_container_width=True):
                    with st.spinner("🤖 Analyzing requirements with AI..."):
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
                        st.balloons()
    
    with col2:
        st.info("""
        ### 💡 Pro Tips
        
        **For best results:**
        
        ✅ Include clear requirements  
        ✅ List must-have skills  
        ✅ Specify experience level  
        ✅ Mention education needs
        """)
    
    # Show JD analysis if available
    if st.session_state.jd_processed:
        st.markdown("---")
        st.markdown("### 📊 Analysis Results")
        st.markdown("")
        
        jd_data = st.session_state.jd_processed
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📝 Word Count", f"{jd_data['word_count']:,}")
        with col2:
            st.metric("🔧 Skills Found", jd_data['total_skills_count'])
        with col3:
            st.metric("👔 Experience", jd_data['experience_level'].title())
        with col4:
            qualifications = len(jd_data.get('qualifications', []))
            st.metric("🎓 Education", f"{qualifications} items")
        
        st.markdown("")
        
        # Show extracted skills
        with st.expander("🔧 View Extracted Skills & Requirements"):
            skills_data = jd_data['skills']
            
            for category, skills in skills_data.items():
                if skills:
                    st.markdown(f"**{category.title()}:**")
                    st.write("• " + "\n• ".join(skills))
                    st.markdown("")

# Tab 2: Upload Resumes
with tab2:
    st.markdown("## Step 2: Upload Candidate Resumes")
    st.markdown("")
    
    if not st.session_state.jd_processed:
        st.warning("⚠️ Please analyze a Job Description first (Step 1)")
    else:
        st.info("📤 Upload multiple resumes at once. Supported: PDF, DOCX")
        st.markdown("")
        
        uploaded_files = st.file_uploader(
            "Drop resume files here",
            type=['pdf', 'docx', 'doc'],
            accept_multiple_files=True,
            label_visibility="collapsed"
        )
        
        st.markdown("")
        
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} file(s) ready to process")
            st.markdown("")
            
            if st.button("🚀 Start Processing", use_container_width=True):
                progress_bar = st.progress(0, text="Initializing...")
                
                processed_resumes = []
                total_files = len(uploaded_files)
                
                for idx, uploaded_file in enumerate(uploaded_files):
                    progress_bar.progress(
                        (idx + 1) / total_files,
                        text=f"Processing {uploaded_file.name}... ({idx + 1}/{total_files})"
                    )
                    
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
                
                # Rank resumes
                ranked_resumes = components['ranker'].rank_resumes(processed_resumes)
                st.session_state.resumes_processed = ranked_resumes
                
                progress_bar.progress(1.0, text="Complete! 🎉")
                
                st.success(f"✅ Successfully processed {len(ranked_resumes)} resumes!")
                st.balloons()
                
                st.info("👉 Check the **Results & Rankings** tab to see the results!")

# Tab 3: Results
with tab3:
    st.markdown("## Step 3: Review Results & Rankings")
    st.markdown("")
    
    if not st.session_state.resumes_processed:
        st.info("📊 Process some resumes first to see results here")
    else:
        ranked_resumes = st.session_state.resumes_processed
        
        # Summary metrics
        st.markdown("### 📈 Quick Stats")
        st.markdown("")
        
        col1, col2, col3, col4 = st.columns(4)
        
        total = len(ranked_resumes)
        selected = sum(1 for r in ranked_resumes if r['status'] == 'selected')
        review = sum(1 for r in ranked_resumes if r['status'] == 'review')
        rejected = sum(1 for r in ranked_resumes if r['status'] == 'rejected')
        
        with col1:
            st.metric("📄 Total", total)
        with col2:
            st.metric("✅ Strong Match", selected)
        with col3:
            st.metric("⚠️ Review", review)
        with col4:
            st.metric("❌ Weak Match", rejected)
        
        st.markdown("---")
        
        # Rankings
        st.markdown("### 🏆 Candidate Rankings")
        st.markdown("")
        
        for resume in ranked_resumes:
            rank = resume['rank']
            name = resume['file_name']
            score = resume['overall_score']
            status = resume['status']
            
            # Status badge
            if status == 'selected':
                badge_html = '<span class="status-badge badge-selected">✅ STRONG MATCH</span>'
                emoji = "🌟"
            elif status == 'review':
                badge_html = '<span class="status-badge badge-review">⚠️ REVIEW NEEDED</span>'
                emoji = "🤔"
            else:
                badge_html = '<span class="status-badge badge-rejected">❌ WEAK MATCH</span>'
                emoji = "📉"
            
            with st.expander(f"#{rank} {emoji} {name} - **{score:.1f}/100**", expanded=(rank <= 2)):
                st.markdown(badge_html, unsafe_allow_html=True)
                st.markdown("")
                
                # Score breakdown
                col1, col2 = st.columns([1, 2])
                
                with col1:
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
        st.markdown("### 💾 Export Results")
        st.markdown("")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Download CSV", use_container_width=True):
                csv_path = "data/screening_results.csv"
                success = components['ranker'].export_to_csv(ranked_resumes, csv_path)
                
                if success:
                    with open(csv_path, 'rb') as f:
                        st.download_button(
                            "⬇️ Click to Download",
                            f,
                            file_name="ats_screening_results.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
        
        with col2:
            if st.button("📄 Generate Report", use_container_width=True):
                report = components['ranker'].generate_summary_report(ranked_resumes)
                st.markdown(report)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem;'>
    <p style='color: rgba(255, 255, 255, 0.6); font-size: 1rem;'>
        <strong>ATS Resume Screener</strong> - Built with 💜 by a recent grad who gets the struggle
    </p>
    <p style='color: rgba(255, 255, 255, 0.4); font-size: 0.9rem;'>
        Powered by Python, spaCy, and determination
    </p>
</div>
""", unsafe_allow_html=True)
