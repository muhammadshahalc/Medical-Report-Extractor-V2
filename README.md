# Medical Report Extractor

A **Streamlit-based tool** for extracting structured medical information from PDFs or images of medical reports.  
It leverages **Groq LLM** for text and image understanding to output patient details, lab tests, and diagnosis in **JSON** and **CSV** formats.

---

## Features
- Upload **PDFs or images** of medical reports
- Extract **Patient Details**: Name, Age, Gender, Report Date
- Extract **Tests**: Test name, value, unit
- Extract **Diagnosis/Observations**
- Download results as:
  - Individual **JSON** per report
  - Combined **CSV** for all reports
  - Combined **JSON** for all reports

---

## Installation
1. Clone the repository:
```bash
git clone https://github.com/muhammadshahalc/Medical-Report-Extractor-V2

1. Install dependencies:
```bash
pip install -r requirements.txt


1. Add your Groq API key to a .env file:
```bash
GROQ_API_KEY=your_api_key_here
