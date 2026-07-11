import google.genai as genai

API_KEY = "AQ.Ab8RN6JNY8lAEcBRGgEV9348hgUpH9kgxvk8eG_Zjn0gyDSIAw"

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_all(text):

    prompt = f"""
You are an AI Assistant.

The transcript may contain speech recognition mistakes.
Correct obvious spelling mistakes before generating the output.

Generate the following:

# Summary
(Simple English)

# Notes
(Headings + Bullet Points)

# Question & Answers
(Create 5 useful Question Answer pairs)

Transcript:
{text}
"""

    response = model.generate_content(prompt)
    return response.text