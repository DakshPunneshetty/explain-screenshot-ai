import streamlit as st
from PIL import Image
import pytesseract
from groq import Groq

# --- PAGE CONFIG ---
st.set_page_config(page_title="Explain Screenshot AI", page_icon="🤖")

# --- GROQ CLIENT ---
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# --- TESSERACT PATH ---
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# --- HEADER ---
st.header("📸 AI Screenshot Explainer")
st.write("Upload a screenshot of a question or paragraph and the AI will explain it.")

# --- EXPLANATION LEVEL ---
level = st.selectbox(
    "Choose explanation level:",
    [
        "Explain like I'm 10",
        "Student level explanation",
        "Detailed explanation"
    ]
)

# --- FILE UPLOADER ---
uploaded_file = st.file_uploader(
    "Upload Screenshot",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file:

    # OPEN IMAGE
    image = Image.open(uploaded_file)

    st.image(image, caption="Uploaded Screenshot", use_container_width=True)

    # OCR TEXT EXTRACTION
    extracted_text = pytesseract.image_to_string(image)

    st.subheader("📝 Extracted Text")
    st.write(extracted_text)

    # --- EXPLAIN BUTTON ---
    if st.button("🎓 Explain"):

        with st.spinner("AI is thinking..."):

            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a helpful tutor. {level}. Explain clearly."
                    },
                    {
                        "role": "user",
                        "content": extracted_text
                    }
                ]
            )

            explanation = response.choices[0].message.content

            st.subheader("🤖 AI Explanation")
            st.write(explanation)

    # --- SUMMARISE BUTTON ---
    if st.button("✂ Summarise"):

        with st.spinner("Summarising..."):

            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": "Summarise the following text in a short and clear way."
                    },
                    {
                        "role": "user",
                        "content": extracted_text
                    }
                ]
            )

            summary = response.choices[0].message.content

            st.subheader("📌 Summary")
            st.write(summary)