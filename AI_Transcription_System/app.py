from flask import Flask, render_template, request, session
import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from speech_to_text import transcribe_audio
from gemini_api import generate_all

app = Flask(__name__)

app.secret_key = "ai_transcription_secret_key"

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    file = request.files.get("file")

    if file is None or file.filename == "":
        return "❌ Please select an audio or video file."

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    # Speech To Text
    transcript = transcribe_audio(filepath)

    # Only ONE Gemini API Call
    result = generate_all(transcript)

    session["transcript"] = transcript
    session["result"] = result

    return render_template(
        "index.html",
        transcript=transcript,
        result=result
    )


@app.route("/transcript")
def transcript():
    return render_template(
        "transcript.html",
        transcript=session.get("transcript", "No transcript available")
    )


@app.route("/summary")
def summary():
    return render_template(
        "summary.html",
        summary=session.get("result", "No result available")
    )


@app.route("/notes")
def notes():
    return render_template(
        "notes.html",
        notes=session.get("result", "No result available")
    )


@app.route("/interview")
def interview():
    return render_template(
        "interview.html",
        qa=session.get("result", "No result available")
    )


@app.route("/downloads")
def downloads():
    return render_template("downloads.html")


if __name__ == "__main__":
    app.run(debug=False)