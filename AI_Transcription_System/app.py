from flask import Flask, render_template, request, session
import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from speech_to_text import transcribe_audio
from gemini_api import (
    generate_summary,
    generate_notes,
    generate_qa
)

app = Flask(__name__)

app.secret_key = "ai_transcription_secret_key"

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Home Upload Page
@app.route("/")
def home():
    return render_template("index.html")


# Upload and Process File
@app.route("/upload", methods=["POST"])
def upload():

    file = request.files.get("file")

    if file is None or file.filename == "":
        return "❌ Please select an audio or video file."


    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(filepath)


    # Speech To Text
    transcript = transcribe_audio(filepath)


    # Gemini AI Processing
    summary = generate_summary(transcript)
    notes = generate_notes(transcript)
    qa = generate_qa(transcript)


    # Store Data
    session["transcript"] = transcript
    session["summary"] = summary
    session["notes"] = notes
    session["qa"] = qa


    return render_template(
    "index.html",
    transcript=transcript,
    summary=summary,
    notes=notes,
    qa=qa
)
# Transcript Page
@app.route("/transcript")
def transcript():

    data = session.get("transcript", "No transcript available")

    return render_template(
        "transcript.html",
        transcript=data
    )


# Summary Page
@app.route("/summary")
def summary():

    data = session.get("summary", "No summary available")

    return render_template(
        "summary.html",
        summary=data
    )


# Notes Page
@app.route("/notes")
def notes():

    data = session.get("notes", "No notes available")

    return render_template(
        "notes.html",
        notes=data
    )


# Interview Q&A Page
@app.route("/interview")
def interview():

    data = session.get("qa", "No Q&A available")

    return render_template(
        "interview.html",
        qa=data
    )


# Download Page
@app.route("/downloads")
def downloads():
    return render_template("downloads.html")


if __name__ == "__main__":
    app.run(debug=True)