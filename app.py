

import os
import json
import streamlit as st
from dotenv import load_dotenv
from extractor import MedicalPDFExtractor
from utils import initialize_record, merge_records
from save_to_csv import save_to_csv
from PIL import Image

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Ensure data folder exists
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

st.title("🩺 Medical Report Extractor (PDFs + Images)")

uploaded_files = st.file_uploader(
    "Upload one or more medical reports (PDFs or Images)", 
    type=["pdf", "png", "jpg", "jpeg"], 
    accept_multiple_files=True
)

if uploaded_files:
    extractor = MedicalPDFExtractor(api_key)
    all_data = []  # store all results for CSV + JSON

    for uploaded_file in uploaded_files:
        st.subheader(f"📄 Processing: {uploaded_file.name}")
        ext = uploaded_file.name.lower().split(".")[-1]

        merged_data = initialize_record()

        if ext == "pdf":
            # Save temp file into data/
            temp_path = os.path.join(DATA_DIR, f"temp_{uploaded_file.name}")
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.read())

            # Convert PDF to images
            pages = extractor.pdf_to_images(temp_path)

        else:
            # Save uploaded image into data/
            temp_path = os.path.join(DATA_DIR, uploaded_file.name)
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.read())

            # Open as image
            image = Image.open(temp_path).convert("RGB")
            pages = [image]

        # Process each page
        for idx, page in enumerate(pages, 1):
            st.info(f"Processing page {idx}/{len(pages)}...")
            base64_img = extractor.encode_image(page)
            if base64_img:
                page_data = extractor.extract_medical_data(base64_img)
                if page_data:
                    merged_data = merge_records(merged_data, page_data)

        # Show results
        st.json(merged_data)

        # Individual JSON download
        json_str = json.dumps(merged_data, indent=4)
        st.download_button(
            label=f"📥 Download {uploaded_file.name} JSON",
            data=json_str,
            file_name=f"{uploaded_file.name}_extracted.json",
            mime="application/json"
        )

        # Store data with file name
        all_data.append((merged_data, uploaded_file.name))

    # Save all data to CSV inside data/
    output_file = os.path.join(DATA_DIR, "extracted_reports.csv")
    for data, file_name in all_data:
        save_to_csv(data, file_name, output_file)

    st.success(f"✅ Extracted data from {len(all_data)} reports. Saved to {output_file}")

    # CSV download
    with open(output_file, "rb") as f:
        st.download_button(
            label="📥 Download All Extracted Data as CSV",
            data=f,
            file_name="extracted_reports.csv",
            mime="text/csv",
        )

    # JSON download (all reports together)
    all_json = {file_name: data for data, file_name in all_data}
    all_json_str = json.dumps(all_json, indent=4)
    st.download_button(
        label="📥 Download All Extracted Data as JSON",
        data=all_json_str,
        file_name="extracted_reports.json",
        mime="application/json",
    )
