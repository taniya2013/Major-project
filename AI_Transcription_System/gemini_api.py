import os
import time
from dotenv import load_dotenv
import os
import time
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_all(text):

    combined_prompt = f"""
The transcript may contain speech recognition errors.

Before generating the output:
- Correct grammar and spelling.
- Correct obvious pronunciation mistakes.
- If <PERSON> refers to the speaker's name, replace it with "Taniya".
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

    # Retry up to 3 times if server is busy
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",  
    messages=[
        {
            "role": "user",
            "content": combined_prompt
        }
    ]
)

            response_text = response.choices[0].message.content

        except Exception as e:
            if "503" in str(e) and attempt < 2:
                time.sleep(5)
            else:
                raise e

    try:
        summary = response_text.split("NOTES:")[0].replace("SUMMARY:", "").strip()

        notes_part = response_text.split("NOTES:")[1]
        notes = notes_part.split("Q&A:")[0].strip()

        qa = response_text.split("Q&A:")[1].strip()

    except Exception:
        summary = response_text
        notes = response_text
        qa = response_text

    return summary, notes, qa