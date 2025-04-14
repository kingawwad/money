import streamlit as st
import re
from PyPDF2 import PdfReader

def extract_and_sum(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    # Extract amounts
    amounts = re.findall(r'£\s*-?\d{1,3}(?:,\d{3})*(?:\.\d{2})?', text.replace(" ", ""))
    
    if not amounts:
        return None, None  # No amounts found

    # Clean and convert amounts
    cleaned = [float(amt.replace("£", "").replace(",", "").strip()) for amt in amounts]

    # Sum including negative values
    total = sum(cleaned)
    return total, cleaned

st.set_page_config(page_title="Transaction Total Calculator", page_icon="💷")
st.title("💷 PDF Transaction Total Calculator")
st.markdown("Drop your **PDF transaction report** below to instantly calculate the total amount.")

uploaded_file = st.file_uploader("📎 Upload PDF", type="pdf")

if uploaded_file:
    try:
        total, values = extract_and_sum(uploaded_file)
        if total is None:
            st.warning("⚠️ No transaction amounts found in this document.")
        else:
            st.success(f"✅ Total Transaction Amount: **£{total:.2f}**")
            with st.expander("📄 View extracted individual amounts"):
                st.write(values)
    except Exception as e:
        st.error(f"⚠️ Error processing file: {e}")
