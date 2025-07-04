
import google.generativeai as genai

class GenAIProcessor:
    def __init__(self, api_key):
        self.api_key = api_key
        if api_key:
            genai.configure(api_key=api_key)
    
    def clean_text(self, text):
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"Clean up the following OCR output for spelling, grammar, and formatting. Keep the meaning unchanged:\n\n{text}"
        response = model.generate_content(prompt)
        return response.text.strip()
