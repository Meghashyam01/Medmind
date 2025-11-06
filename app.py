import os
import streamlit as st
import fitz  # PyMuPDF
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
# ---------- Setup ----------
# Read the API key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    st.error("❌ OpenAI API key not found! Please set it using environment variables.")
    st.stop()

client = OpenAI(api_key=openai_api_key)

# ---------- Streamlit UI ----------
st.set_page_config(page_title="MediSummarizer", page_icon="🩺", layout="centered")

st.title("🩺 MediMind AI")
st.write("Upload a **medical PDF report** to get a concise summary and key findings.")

uploaded_file = st.file_uploader("📂 Upload your report (PDF format)", type=["pdf"])

# ---------- Function to Extract Text ----------
def extract_text_from_pdf(pdf_file):
    text = ""
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text("text")
    return text

# ---------- Summarization ----------
# def summarize_text(text):
#     try:
#         response = client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[
#                 {"role": "system", "content": "You are a helpful medical assistant that summarizes reports accurately."},
#                 {"role": "user", "content": f"Summarize this medical report and list the key findings:\n\n{text}"}
#             ],
#             max_tokens=500,
#             temperature=0.5,
#         )
#         summary = response.choices[0].message.content
#         return summary.strip()
#     except Exception as e:
#         return f"⚠️ Error: {e}"

def summarize_text(text):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a highly skilled medical data analyst and summarizer. "
                        "You will read complex medical reports and generate structured, easy-to-understand summaries. "
                        "Ensure accuracy, neutrality, and patient privacy in your answers."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "Analyze the following medical report and summarize it clearly. "
                        "Your response must include these sections:\n\n"
                        "1️⃣ **Summary:** A concise overview of the report (2–3 sentences).\n"
                        "2️⃣ **Key Findings:** Bullet points listing abnormal results, diagnoses, or clinical impressions.\n"
                        "3️⃣ **Normal Observations:** Mention normal or within-range parameters briefly.\n"
                        "4️⃣ **Possible Concerns or Follow-up Recommendations:** Only if relevant, in professional tone.\n"
                        "5️⃣ **Patient-Friendly Explanation:** Rewrite in simple terms (so a non-medical person can understand).\n\n"
                        f"Here is the report text:\n{text}"
                    ),
                },
            ],
            max_tokens=800,
            temperature=0.4,
        )
        summary = response.choices[0].message.content
        return summary.strip()
    except Exception as e:
        return f"⚠️ Error: {e}"



# ---------- Processing ----------
if uploaded_file is not None:
    with st.spinner("🔍 Extracting and summarizing the report..."):
        text = extract_text_from_pdf(uploaded_file)
        if len(text) < 200:
            st.warning("The uploaded PDF seems too short or unreadable. Try another file.")
        else:
            summary = summarize_text(text)
            st.success("✅ Summary Generated Successfully!")
            st.subheader("🩸 Report Summary:")
            st.write(summary)
else:
    st.info("Please upload a PDF file to start.")

