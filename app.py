import pandas as pd
import streamlit as st
from utils import extract_text, summarize_resume, score_resume

st.set_page_config(page_title="HR AI", layout="wide")

st.title("HR resume screening assistance tool")

job_description = st.text_area("Enter the job description")
resume_files = st.file_uploader("Upload the resumes", type=['pdf'],
                             help="Make sure that all files are in PDF format",
                             accept_multiple_files=True)

if job_description and resume_files:
    automate_button = st.button("Automate Screening", disabled=False,
                                type="primary", use_container_width=True)
else:
    automate_button = st.button("Automate Screening", disabled=True,
                                type="primary", use_container_width=True)

if automate_button:
    name_list = []
    summary_list = []
    score_list = []
    description_list = []

    # LOOP THROUGH ALL THE RESUME
    for resume in resume_files:
        
        # EXTRACT APPLICANT NAME
        applicant_name = resume.name.replace(".pdf", "")
        name_list.append(applicant_name)

        # EXTRACT TEXT AND SUMMARIZE RESUME CONTENT
        content = extract_text(resume)
        content_summary = summarize_resume(content, "AIzaSyCjvmsPbDJKqMINnFuCmpJOcCvYrve2xfQ")
        summary_list.append(content_summary)

        # GENERATE RESUME SCORE AND DESCRIPTION
        resume_score, resume_description = score_resume(content_summary, job_description, "AIzaSyCjvmsPbDJKqMINnFuCmpJOcCvYrve2xfQ")
        score_list.append(resume_score)
        description_list.append(resume_description)
    
    # CREATE AND SHOW DATAFRAME FROM THE SUMMARIES, SCORES, AND DESCRIPTIONS
    results_table = pd.DataFrame({"Name": name_list,
                       "Resume Summary:": summary_list,
                       "Description": description_list,
                       "Score": score_list,})
    results_table = results_table.sort_values(by='Score', ascending=False)
    results_table = results_table.set_index('Name')
    st.table(results_table)