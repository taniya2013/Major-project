import google.generativeai as genai

API_KEY = "AQ.Ab8RN6KiUAont9b0O7AiP5jXAFy1B93uZuE4P3hPNni6W-XyXg"

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-flash-latest")


def generate_all(text):

    correction = """
The transcript may contain speech recognition errors.

Before generating the output:
- Correct grammar and spelling.
- Correct obvious pronunciation mistakes.
- If "Anya" refers to the speaker's name, replace it with "Taniya".
- Use the corrected transcript for every output.
"""

    summary_prompt = f"""
{correction}

Generate a short summary in simple English.

Transcript:
{text}
"""

    notes_prompt = f"""
{correction}

Generate organized lecture notes.

Rules:
- Use headings.
- Use bullet points.
- Simple English.

Transcript:
{text}
"""

    qa_prompt = f"""
{correction}

Generate 5 Interview Question & Answer pairs.

Rules:
- Questions should be based on the corrected transcript.
- If the speaker's name is detected as "Anya", use "Taniya".
- Keep answers short and simple.

Transcript:
{text}
"""

    summary = model.generate_content(summary_prompt).text
    notes = model.generate_content(notes_prompt).text
    qa = model.generate_content(qa_prompt).text

    return summary, notes, qa