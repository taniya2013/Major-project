from flask import Flask, render_template, request, session
import os
from flask import Flask, render_template, request, session, send_file
import io
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

    # Gemini AI
    summary, notes, qa = generate_all(transcript)

    # Store in session
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
        summary=session.get("summary", "No summary available")
    )


@app.route("/notes")
def notes():
    return render_template(
        "notes.html",
        notes=session.get("notes", "No notes available")
    )


@app.route("/interview")
def interview():
    return render_template(
        "interview.html",
        qa=session.get("qa", "No Q&A available")
    )


@app.route("/downloads")
def downloads():
    return render_template("downloads.html")
@app.route("/download/transcript")
def download_transcript():

    data = session.get("transcript", "No transcript available")

    return send_file(
        io.BytesIO(data.encode("utf-8")),
        as_attachment=True,
        download_name="Transcript.txt",
        mimetype="text/plain"
    )


@app.route("/download/summary")
def download_summary():

    data = session.get("summary", "No summary available")

    return send_file(
        io.BytesIO(data.encode("utf-8")),
        as_attachment=True,
        download_name="Summary.txt",
        mimetype="text/plain"
    )


@app.route("/download/notes")
def download_notes():

    data = session.get("notes", "No notes available")

    return send_file(
        io.BytesIO(data.encode("utf-8")),
        as_attachment=True,
        download_name="Notes.txt",
        mimetype="text/plain"
    )


@app.route("/download/qa")
def download_qa():

    data = session.get("qa", "No Q&A available")

    return send_file(
        io.BytesIO(data.encode("utf-8")),
        as_attachment=True,
        download_name="Interview_QA.txt",
        mimetype="text/plain"
    )

if __name__ == "__main__":
    app.run(debug=True)