
import streamlit as st
import os
import tempfile
from pathlib import Path
import traceback
from utils.pdf_processor import PDFProcessor
from utils.ocr_processor import OCRProcessor
from utils.word_generator import WordGenerator
from utils.genai_processor import GenAIProcessor

def main():
    st.title("📄 PDF to Word Converter (with Handwriting, Vision & AI Cleanup)")
    st.markdown("Convert your PDF documents to Word format. Now with Google Vision OCR & Gemini AI cleanup!")

    with st.sidebar:
        st.header("Advanced OCR (Optional)")
        vision_json = st.file_uploader("Google Vision Service Account JSON", type="json")
        gemini_api_key = st.text_input("Gemini API Key", type="password")

    st.header("Upload PDF Document")
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=['pdf'],
        help="Upload a PDF document to convert to Word format. Supports both typed and handwritten documents."
    )

    st.header("Processing Options")
    col1, col2, col3 = st.columns(3)
    with col1:
        force_ocr = st.checkbox("Force OCR Processing", help="Use for handwritten or image-based PDFs")
    with col2:
        preserve_formatting = st.checkbox("Preserve Formatting", value=True)
    with col3:
        ocr_engine = st.selectbox("OCR Engine", ["Tesseract (Free/Local)", "Google Vision (High Accuracy)"])
    
    use_gemini = st.checkbox("AI Cleanup with Gemini", help="Enhance accuracy/grammar of extracted text")

    if uploaded_file is not None and st.button("Convert to Word", type="primary"):
        convert_pdf_to_word(uploaded_file, force_ocr, preserve_formatting, ocr_engine, vision_json, gemini_api_key, use_gemini)

def convert_pdf_to_word(uploaded_file, force_ocr, preserve_formatting, ocr_engine, vision_json, gemini_api_key, use_gemini):
    import io

    vision_client = None
    if ocr_engine == "Google Vision (High Accuracy)" and vision_json:
        import tempfile, os
        from google.cloud import vision
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as f:
            f.write(vision_json.read())
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = f.name
        vision_client = vision.ImageAnnotatorClient()

    genai_processor = GenAIProcessor(gemini_api_key) if use_gemini and gemini_api_key else None

    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            pdf_path = os.path.join(temp_dir, "input.pdf")
            with open(pdf_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            
            pdf_processor = PDFProcessor()
            ocr_processor = OCRProcessor()
            word_generator = WordGenerator()
            progress_bar = st.progress(0)
            status_text = st.empty()
            status_text.text("Analyzing PDF structure...")
            progress_bar.progress(10)
            has_text = pdf_processor.has_extractable_text(pdf_path)

            if has_text and not force_ocr:
                st.info("📝 Document contains extractable text. Using direct text extraction.")
                status_text.text("Extracting text from PDF...")
                progress_bar.progress(30)
                extracted_content = pdf_processor.extract_text_with_formatting(pdf_path)
                progress_bar.progress(60)
            else:
                if force_ocr:
                    st.info("🔍 OCR processing requested. Converting PDF to images...")
                else:
                    st.info("🔍 No extractable text found. Using OCR processing...")
                status_text.text("Converting PDF pages to images...")
                progress_bar.progress(20)
                images = pdf_processor.convert_to_images(pdf_path)
                progress_bar.progress(40)
                status_text.text("Performing OCR on images...")
                progress_bar.progress(50)
                ocr_mode = "vision" if ocr_engine == "Google Vision (High Accuracy)" and vision_client else "tesseract"
                extracted_content = ocr_processor.process_images(images, engine=ocr_mode, vision_client=vision_client)
                progress_bar.progress(80)

            if genai_processor is not None:
                status_text.text("Enhancing text with Gemini AI...")
                extracted_content = genai_processor.clean_text(extracted_content)
                progress_bar.progress(90)
            else:
                progress_bar.progress(90)
            
            word_path = os.path.join(temp_dir, "output.docx")
            word_generator.create_document(extracted_content, word_path, preserve_formatting)
            progress_bar.progress(100)
            status_text.text("Conversion completed successfully!")
            st.success("✅ Conversion completed successfully!")
            st.header("Preview")
            preview_text = extracted_content[:1000] + "..." if len(extracted_content) > 1000 else extracted_content
            st.text_area("Document Preview", preview_text, height=200)
            with open(word_path, "rb") as f:
                word_content = f.read()
            original_name = Path(uploaded_file.name).stem
            download_name = f"{original_name}_converted.docx"
            st.download_button(
                label="📥 Download Word Document",
                data=word_content,
                file_name=download_name,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
            st.header("Conversion Statistics")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Characters", len(extracted_content))
            with col2:
                words = len(extracted_content.split())
                st.metric("Words", words)
            with col3:
                lines = len(extracted_content.split('\n'))
                st.metric("Lines", lines)
        except Exception as e:
            st.error(f"❌ Error during conversion: {str(e)}")
            with st.expander("Show detailed error"):
                st.code(traceback.format_exc())

if __name__ == "__main__":
    st.set_page_config(
        page_title="PDF to Word Converter",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    with st.sidebar:
        st.header("Instructions")
        st.markdown("""
        1. Upload a PDF file  
        2. Choose OCR engine (Tesseract or Google Vision)  
        3. Optionally enable AI Cleanup (Gemini)  
        4. Download the converted document  
        """)
        st.header("About")
        st.markdown("""
        This application uses:  
        - **PyPDF2**, **Tesseract**, **Google Vision** for OCR  
        - **Gemini AI** for enhancement  
        - **python-docx** for Word generation  
        """)
    main()
