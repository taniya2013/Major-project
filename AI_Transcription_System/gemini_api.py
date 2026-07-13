import os
from dotenv import load_dotenv
import google.generativeai as genai

# .env file load karo
load_dotenv()

# API key .env se lo
API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini configure karo
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-flash-latest")

def generate_all(text):

    combined_prompt = f"""
The transcript may contain speech recognition errors.

Before generating the output:
- Correct grammar and spelling.
- Correct obvious pronunciation mistakes.
- If "Anya" refers to the speaker's name, replace it with "Taniya".
- Use the corrected transcript for every output.

Generate output in this exact format:

SUMMARY:
(write short summary)

NOTES:
(use headings and bullet points)

Q&A:
(generate 5 interview question answers)

Transcript:
{text}
"""

    response = model.generate_content(combined_prompt).text


    # Output ko 3 parts me divide karna
    try:
        summary = response.split("NOTES:")[0].replace("SUMMARY:", "").strip()

        notes_part = response.split("NOTES:")[1]
        notes = notes_part.split("Q&A:")[0].strip()

        qa = response.split("Q&A:")[1].strip()

    except:
        summary = response
        notes = response
        qa = response


    return summary, notes, qa