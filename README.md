# PDF to Word Converter (with Handwriting, Vision & AI Cleanup)

Convert your PDF documents to Word format. Supports typed, scanned, and handwritten PDFs using OCR (Tesseract or Google Vision) and optional Gemini AI cleanup for enhanced accuracy.

---

## 🚀 Features
- **PDF to Word**: Converts PDF files to editable Word documents (.docx)
- **OCR Support**: Handles scanned and handwritten PDFs using Tesseract (local) or Google Vision (cloud)
- **AI Cleanup**: Optionally enhance extracted text with Gemini AI
- **Formatting**: Preserves basic formatting and page breaks
- **Statistics**: Shows character, word, and line counts

---

## 🖥️ How to Use

### 1. **Locally (with Python & Streamlit)**
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   streamlit run app.py
   ```
3. Open the provided local URL in your browser.

### 2. **On Streamlit Cloud**
1. Upload your project to GitHub (all `.py` files, `requirements.txt`, and this `README.md`).
2. Go to [Streamlit Cloud](https://streamlit.io/cloud) and connect your GitHub repo.
3. Deploy the app (entry point: `app.py`).

---

## ⚠️ Important Notes
- **Tesseract OCR**: Requires the Tesseract binary, which is not available on Streamlit Cloud. Use the **Google Vision** OCR option on Streamlit Cloud.
- **Google Vision & Gemini AI**: You must provide your own API keys/credentials in the sidebar for these features to work.
- **Large PDFs**: Processing large or image-heavy PDFs may take longer, especially with OCR.

---

## 🔑 Required API Keys
- **Google Vision**: Upload your Google Cloud Vision service account JSON in the sidebar.
- **Gemini AI**: Enter your Gemini API key in the sidebar for AI cleanup.

---

## 📂 Project Structure
```
app.py
requirements.txt
utils/
  ├── pdf_processor.py
  ├── ocr_processor.py
  ├── word_generator.py
  └── genai_processor.py
```

---

## 🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License
MIT 