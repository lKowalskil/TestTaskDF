import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-8b')

def summarize_text(text: str) -> str:
    if not GEMINI_API_KEY:
        return f"This is a sample summary of the note. Original length: {len(text)} characters."
    try:
        prompt = f"Please provide a concise summary of the following text:\n\n{text}"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return "Failed to generate summary due to an API error."