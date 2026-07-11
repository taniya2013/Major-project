import google.generativeai as genai

API_KEY = "AQ.Ab8RN6IqdO5rdk__cPu5EyElZVrV-65TiulmjX1tYIiG5lfcSg"

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-flash-latest")


def generate_all(text):

    summary_prompt = f"""
The transcript may contain speech recognition errors.
Correct names, grammar, and obvious pronunciation mistakes using context before generating the output.

Transcript:
{text}
"""

    notes_prompt = f"""
Convert this transcript into organized notes.

Rules:
- Use headings.
- Use bullet points.
- Simple English.

Transcript:
{text}
"""

    qa_prompt = f"""
Create 5 useful Question & Answer pairs from this transcript.

Rules:
- Simple English.
- Short answers.

Transcript:
{text}
"""

    summary = model.generate_content(summary_prompt).text
    notes = model.generate_content(notes_prompt).text
    qa = model.generate_content(qa_prompt).text

    return summary, notes, qa