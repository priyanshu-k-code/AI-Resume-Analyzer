# ================================
# AI Resume Analyzer
# Main Application
# ================================

# Import required libraries
import streamlit as st

from utils.pdf_reader import extract_pdf_text
from utils.ats import calculate_similarity_bert
from utils.llm import get_report
from utils.helper import extract_scores, calculate_average_score


# ================================
# Configure Streamlit Page
# ================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📝",
    layout="wide",
)


# ================================
# Load Custom Styling
# ================================

def load_custom_css():
    """Load the application's custom CSS file."""

    try:
        with open("assets/style.css", "r", encoding="utf-8") as css_file:
            st.markdown(
                f"<style>{css_file.read()}</style>",
                unsafe_allow_html=True,
            )
    except FileNotFoundError:
        pass


load_custom_css()


# ================================
# Session State
# ================================

if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False

if "resume" not in st.session_state:
    st.session_state.resume = ""

if "job_desc" not in st.session_state:
    st.session_state.job_desc = ""

if "report" not in st.session_state:
    st.session_state.report = ""

if "ats_score" not in st.session_state:
    st.session_state.ats_score = 0.0

if "ai_score" not in st.session_state:
    st.session_state.ai_score = 0.0


# ================================
# Application Header
# ================================

st.title("AI Resume Analyzer 📝")
st.caption(
    "Analyze your resume against a job description using ATS similarity "
    "and Generative AI."
)

st.divider()


# ================================
# Helper Functions
# ================================

def reset_analysis():
    """Reset the current analysis and return to the upload form."""

    st.session_state.form_submitted = False
    st.session_state.resume = ""
    st.session_state.job_desc = ""
    st.session_state.report = ""
    st.session_state.ats_score = 0.0
    st.session_state.ai_score = 0.0


def display_score_card(title, score, description):
    """Display a clean score card with a progress bar."""

    percentage = score * 100

    st.markdown(
        f"""
        <div class="score-card">
            <div class="score-title">{title}</div>
            <div class="score-value">{percentage:.1f}%</div>
            <div class="score-description">{description}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.progress(min(max(score, 0.0), 1.0))


def display_match_status(score):
    """Display a simple interpretation of the ATS similarity score."""

    if score >= 0.80:
        st.success("Excellent Resume Match ✅")
    elif score >= 0.60:
        st.info("Good Resume Match 👍")
    elif score >= 0.40:
        st.warning("Moderate Resume Match ⚠️")
    else:
        st.error("Resume Needs Improvement ❌")


# ================================
# Resume Analysis Form
# ================================

if not st.session_state.form_submitted:

    st.subheader("Resume & Job Details")
    st.caption("Upload your resume and provide the job description to begin.")

    with st.form("resume_analysis_form"):

        # Upload resume in PDF format
        resume_file = st.file_uploader(
            "Upload your Resume/CV",
            type=["pdf"],
            help="Upload a text-based PDF resume for best results.",
        )

        # Enter the job description
        job_description = st.text_area(
            "Enter the Job Description",
            placeholder="Paste the job description here...",
            height=220,
        )

        submitted = st.form_submit_button(
            "Analyze Resume",
            use_container_width=True,
        )

        if submitted:

            # Validate both required inputs
            if not resume_file:
                st.warning("Please upload your resume in PDF format.")

            elif not job_description.strip():
                st.warning("Please enter the job description.")

            else:
                with st.spinner("Extracting information from your resume..."):
                    resume_text = extract_pdf_text(resume_file)

                if not resume_text.strip():
                    st.error(
                        "No readable text could be extracted from the PDF. "
                        "Please try another PDF."
                    )
                else:
                    st.session_state.resume = resume_text
                    st.session_state.job_desc = job_description.strip()
                    st.session_state.form_submitted = True
                    st.rerun()


# ================================
# Resume Analysis
# ================================

if st.session_state.form_submitted:

    st.subheader("Analysis Results")

    # Calculate ATS similarity score
    with st.spinner("Calculating ATS similarity score..."):
        ats_score = calculate_similarity_bert(
            st.session_state.resume,
            st.session_state.job_desc,
        )

    st.session_state.ats_score = ats_score

    # Generate AI analysis report
    with st.spinner("Generating AI resume analysis..."):
        report = get_report(
            st.session_state.resume,
            st.session_state.job_desc,
        )

    st.session_state.report = report

    # Extract scores from the AI report
    report_scores = extract_scores(report)
    avg_score = calculate_average_score(report_scores)
    st.session_state.ai_score = avg_score

    # Display score cards
    col1, col2 = st.columns(2)

    with col1:
        display_score_card(
            "ATS Similarity Score",
            ats_score,
            "Similarity between your resume and the job description.",
        )
        display_match_status(ats_score)

    with col2:
        display_score_card(
            "AI Resume Score",
            avg_score,
            "Average score generated from the AI evaluation.",
        )

    st.divider()

    # Display generated analysis
    st.subheader("AI Generated Analysis Report")

    st.markdown(
        f'<div class="report-container">{report}</div>',
        unsafe_allow_html=True,
    )

    st.divider()

    # Download and reset actions
    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            label="Download Analysis Report",
            data=report,
            file_name="AI_Resume_Analysis_Report.txt",
            mime="text/plain",
            use_container_width=True,
        )

    with col2:
        if st.button(
            "Analyze Another Resume",
            use_container_width=True,
        ):
            reset_analysis()
            st.rerun()


# ================================
# Application Footer
# ================================

st.divider()

st.caption(
    "Built with Python, Streamlit, Sentence Transformers, Scikit-learn and Groq."
)
