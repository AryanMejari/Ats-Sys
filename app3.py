from dotenv import load_dotenv
import base64
import streamlit as st
import os
import io
import fitz  # PyMuPDF
import google.generativeai as genai
from PIL import Image

# Load environment variables
load_dotenv()

# Configure Gemini API
# Configure Gemini API (replace YOUR_KEY_HERE with your actual key)
genai.configure(api_key="AIzaSyC2p9DdKiaV_fN__TU1iac1dapmHCpXQ0s")
  # Update your .env key to be named GOOGLE_API_KEY

# Function to send request to Gemini
def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text

# Function to convert PDF to image using PyMuPDF
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        page = doc.load_page(0)  # First page
        pix = page.get_pixmap()

        # Save image as bytes
        img_byte_arr = io.BytesIO(pix.tobytes("jpeg"))

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr.getvalue()).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit App UI
st.set_page_config(page_title="ATS Resume Expert")
st.header("📄 ATS Tracking System")

input_text = st.text_area("✍️ Job Description:", key="input")
uploaded_file = st.file_uploader("📎 Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.success("✅ PDF Uploaded Successfully!")

# Prompt templates
input_prompt1 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
Your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches
the job description. First the output should come as percentage, then keywords missing, and lastly final thoughts.
"""

# Buttons
submit1 = st.button("🧠 Tell Me About the Resume")
submit2 = st.button("💡 How Can I Improvise My Skills")
submit3 = st.button("📊 Percentage Match")

# Button actions
if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("📝 The Response is")
        st.write(response)
    else:
        st.warning("⚠️ Please upload the resume.")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("📈 The Response is")
        st.write(response)
    else:
        st.warning("⚠️ Please upload the resume.")
