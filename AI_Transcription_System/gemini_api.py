import google.generativeai as genai

API_KEY = "enter your key here"

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_summary(text):

    prompt = f"""
You are an AI assistant.

The transcript may contain speech recognition mistakes.
Correct obvious spelling and name errors using context before creating the output.

Create a simple English summary.
Ignore greetings and focus on meaningful information.


Rules:
- Always write the summary in simple English.
- Use easy words that everyone can understand.
- Ignore greetings and speaker introductions.
- Focus on the main topic, important points, and conclusion.

Transcript:
{text}
"""

    response = model.generate_content(prompt)
    return response.text

def generate_notes(text):

    prompt = f"""
Convert this transcript into organized lecture notes.

Rules:
- Write only in simple English.
- Use headings and bullet points.
- Make notes clear for students.
- Remove unnecessary introductions.

Transcript:
{text}
"""

    response = model.generate_content(prompt)
    return response.text



def generate_qa(text):

    prompt = f"""
Create useful Question and Answer pairs from this transcript.

Rules:
- Write all questions and answers in simple English.
- Keep answers short and understandable.
- Do not include greetings or introductions.

Transcript:
{text}
"""

    response = model.generate_content(prompt)
    return response.text