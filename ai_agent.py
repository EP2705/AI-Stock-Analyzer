import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def get_ai_response(question):
    try:
        api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-flash-latest')
        response = model.generate_content(question)
        return response.text

    except Exception as e:
        print(f"An error occurred: {e}")
