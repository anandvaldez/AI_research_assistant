import streamlit as st
import requests
import fitz  # PyMuPDF
from io import BytesIO

st.set_page_config(page_title="GenAI Paper Assistant", layout="wide")
st.title("📚 GenAI Academic Paper Assistant")

# --- SEARCH SECTION ---
st.subheader("1. Search for Papers (via arXiv)")
query = st.text_input("Enter research topic or keywords:", "graph neural networks for drug discovery")

if st.button("Search arXiv"):
    if query:
        search_url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=5"
        response = requests.get(search_url, verify=False)

        if response.status_code == 200:
            from xml.etree import ElementTree as ET
            feed = ET.fromstring(response.content)
            entries = feed.findall("{http://www.w3.org/2005/Atom}entry")

            for entry in entries:
                title = entry.find("{http://www.w3.org/2005/Atom}title").text
                summary = entry.find("{http://www.w3.org/2005/Atom}summary").text
                pdf_link = [l.attrib['href'] for l in entry.findall("{http://www.w3.org/2005/Atom}link") if l.attrib.get('title') == 'pdf']

                st.markdown(f"### 📄 {title}")
                st.write(summary.strip())
                if pdf_link:
                    st.markdown(f"[🔗 Download PDF]({pdf_link[0]})")

# --- UPLOAD AND VIEW SECTION ---
st.subheader("2. Upload a Paper PDF to View Text Content")
pdf_file = st.file_uploader("Upload PDF", type="pdf")

if pdf_file:
    st.info("Extracting text from PDF...")
    pdf_reader = fitz.open(stream=pdf_file.read(), filetype="pdf")
    full_text = ""
    for page in pdf_reader:
        full_text += page.get_text()

    st.success("Text extraction complete.")
    st.subheader("📄 Full Paper Text")
    st.text_area("Extracted Text", value=full_text, height=400)
