import streamlit as st
import os
from dotenv import load_dotenv
from azure.ai.language import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import re

# Load environment variables
load_dotenv()
AZURE_KEY = os.getenv("AZURE_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")

# Initialize Azure Language client
client = TextAnalyticsClient(endpoint=AZURE_ENDPOINT, credential=AzureKeyCredential(AZURE_KEY))

# Streamlit UI
st.title("Resume Key Phrase Extractor & Experience Analyzer")

st.markdown("""
Upload a resume in **TXT format** to extract key phrases, identify skills, and calculate total experience.
""")

# Upload resume file
uploaded_file = st.file_uploader("Upload your resume (.txt)", type=["txt"])

# Predefined skill list for matching
predefined_skills = ["Python", "Azure", "Machine Learning", "SQL", "Power BI", "Streamlit"]

if uploaded_file:
    # Read uploaded resume
    resume_text = uploaded_file.read().decode("utf-8")

    # Key phrase extraction
    response = client.extract_key_phrases(documents=[resume_text])[0]
    key_phrases = response.key_phrases if not response.is_error else []

    st.subheader("Key Phrases Extracted")
    st.write(key_phrases)

    # Skill matching
    matched_skills = [skill for skill in predefined_skills if skill.lower() in resume_text.lower()]
    st.subheader("Matched Skills")
    st.write(matched_skills if matched_skills else "No skills matched from predefined list.")

    # Experience extraction
    experience_matches = re.findall(r"(\d+)\+?\s+years?", resume_text.lower())
    experience_years = max([int(x) for x in experience_matches]) if experience_matches else 0
    st.subheader("Total Experience (Years)")
    st.write(experience_years)
