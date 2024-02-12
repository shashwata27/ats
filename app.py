from dotenv import load_dotenv
import base64
import streamlit as st
import os
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(prompt)
    return response.text


## Streamlit App

st.set_page_config(page_title="ATS Resume EXpert")
st.header("Resume Scoring")

st.subheader("Enter 5 different JDs for the same position")
jds=[]
jds.append(st.text_area("Job Description 1: ",key="jd1"))
jds.append(st.text_area("Job Description 2: ",key="jd2"))
jds.append(st.text_area("Job Description 3: ",key="jd3"))
jds.append(st.text_area("Job Description 4: ",key="jd4"))
jds.append(st.text_area("Job Description 5: ",key="jd5"))
jd_scan = st.button("JD Keyword Scan")

st.subheader("Enter The Resume")
resume_text=st.text_area("Resume Description: ",key="resume")
resume_scan = st.button("Resume Keyword Scan")

match = st.button("Show Match percentage")

jd_scan_prompt="""
As a enterprise level Application Tracking System (ATS) whose expertise is in tech/software engineering field. 
Scan through the job descriptions listed below, and find the most import keywords in them and assign weightage to them.
The most important keywords occur most often in the job description. 
Note: 
    1. plural and single words are same keywords, eg: pipelines and pipeline are same
    2. sub part of word or words are also same, eg: aws s3 and s3 are same
    
the Job Description:
{jd}
    
Provide Output as a set of unique keywords with their weightages like word1:weightage1|word2:weightage2|word3:weightage3.
(Only add keywords that are provided in the prompt)
"""

jd_compiler_prompt="""
As a enterprise level Application Tracking System,
keywords scanned form jds are given as word1:weightage1|word2:weightage2|word3:weightage3

Compile all the keywords and normalize the weightage and find all the unique keywords.
the keywords are:
{keywords}

Output should be a set of unique keywords with their weightages like word1:weightage1|word2:weightage2|word3:weightage3
(Only add keywords that are provided in the prompt)
"""

resume_scan_prompt="""
As a enterprise level Application Tracking System (ATS) whose expertise is in tech/software engineering field. 
Scan through the resume of a software engineer or tech person and note the keywords.
Note: 
    1. plural and single words are same keywords, eg: pipelines and pipeline are same
    2. sub part of word or words are also same, eg: aws s3 and s3 are same

the resume is:
{resume}

Provide Output as a set of unique keywords like word1|word2|word3
(Only add keywords that are provided in the prompt)
"""

match_prompt="""
As a enterprise level Application Tracking System (ATS) whose expertise is in tech/software engineering field. 
Compare the keywords and generate a match score against the keywords from resume and Job descriptions.

{jd_keywords} vs {resume_keywords}

The output should be:
Output Percentage: %
Words: Missing_word1|Missing_word2
"""



if jd_scan:
    res=[]
    for jd in jds:
        response=get_gemini_response(jd_scan_prompt.format(jd=jd))
        res.append(response)
    jd_keywords=get_gemini_response(jd_compiler_prompt.format(keywords="|".join(res)))
    st.session_state['jd_keywords']=jd_keywords
st.subheader("The JD keywords are")
if 'jd_keywords' in st.session_state.keys():
    st.write(st.session_state.jd_keywords)


if resume_scan:
    resume_keywords=get_gemini_response(resume_scan_prompt.format(resume=resume_text))
    st.session_state['resume_keywords'] = resume_keywords
st.subheader("The Resume keywords are")
if 'resume_keywords' in st.session_state.keys():
    st.write(st.session_state.resume_keywords)

if match:
    match_verdict = get_gemini_response(match_prompt.format(jd_keywords=st.session_state.jd_keywords, resume_keywords=st.session_state.resume_keywords))
    st.session_state['match_verdict'] = match_verdict
st.subheader("The Verdict is")
if 'match_verdict' in st.session_state.keys():
    st.write(st.session_state.match_verdict)






