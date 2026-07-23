import uuid

from flask import Flask, render_template, request, session, send_file
import io
import os
import yt_dlp
from urllib.parse import urlparse


os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from speech_to_text import transcribe_audio
from gemini_api import generate_all

app = Flask(__name__)

app.secret_key = "ai_transcription_secret_key"

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ---------------- HOME ---------------- #

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- UPLOAD ---------------- #

@app.route("/upload", methods=["POST"])
def upload():
    try:
        file = request.files.get("file")

        if file is None or file.filename == "":
            return "Please select a file."

        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        print("1. File Saved")

        transcript = transcribe_audio(filepath)
        print("2. Transcription Done")

        summary, notes, qa = generate_all(transcript)
        print("3. Gemini Done")

        return render_template(
            "index.html",
            transcript=transcript,
            summary=summary,
            notes=notes,
            qa=qa
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        return str(e)

# ---------------- TRANSCRIPT ---------------- #

@app.route("/transcript")
def transcript():
    return render_template(
        "transcript.html",
        transcript=session.get("transcript", "No transcript available")
    )


# ---------------- SUMMARY ---------------- #

@app.route("/summary")
def summary():
    return render_template(
        "summary.html",
        summary=session.get("summary", "No summary available")
    )


# ---------------- NOTES ---------------- #

@app.route("/notes")
def notes():
    return render_template(
        "notes.html",
        notes=session.get("notes", "No notes available")
    )


# ---------------- INTERVIEW ---------------- #

@app.route("/interview")
def interview():
    return render_template(
        "interview.html",
        qa=session.get("qa", "No Q&A available")
    )


# ---------------- DOWNLOAD PAGE ---------------- #

@app.route("/downloads")
def downloads():
    return render_template("downloads.html")


# ---------------- DOWNLOAD TRANSCRIPT ---------------- #

@app.route("/download/transcript")
def download_transcript():

    data = session.get("transcript", "No transcript available")

    return send_file(
        io.BytesIO(data.encode("utf-8")),
        as_attachment=True,
        download_name="Transcript.txt",
        mimetype="text/plain"
    )


# ---------------- DOWNLOAD SUMMARY ---------------- #

@app.route("/download/summary")
def download_summary():

    data = session.get("summary", "No summary available")

    return send_file(
        io.BytesIO(data.encode("utf-8")),
        as_attachment=True,
        download_name="Summary.txt",
        mimetype="text/plain"
    )


# ---------------- DOWNLOAD NOTES ---------------- #

@app.route("/download/notes")
def download_notes():

    data = session.get("notes", "No notes available")

    return send_file(
        io.BytesIO(data.encode("utf-8")),
        as_attachment=True,
        download_name="Notes.txt",
        mimetype="text/plain"
    )


# ---------------- DOWNLOAD INTERVIEW QA ---------------- #

@app.route("/download/qa")
def download_qa():

    data = session.get("qa", "No Q&A available")

    return send_file(
        io.BytesIO(data.encode("utf-8")),
        as_attachment=True,
        download_name="Interview_QA.txt",
        mimetype="text/plain"
    )

@app.route("/profile")
def profile():
    return render_template("profile.html")
@app.route("/url_transcribe", methods=["POST"])
def url_transcribe():

    video_url = request.form["video_url"].strip()

    parsed = urlparse(video_url)

    if not parsed.scheme or not parsed.netloc:
        return render_template(
            "index.html",
            transcript="⚠️ Please enter a valid URL."
        )

       try:

        filename = "audio_" + str(uuid.uuid4())

        output_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        ydl_opts = {
            "format": "bestaudio/best",
            "cookiefile": "cookies.txt",
            "extractor_args": {
                "youtube": {
                    "player_client": ["android", "web"]
                }
            },
            "outtmpl": output_path + ".%(ext)s",
            "noplaylist": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ]
        }

        print("Downloading:", video_url)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)

        print("Downloaded:", info.get("title"))

        audio_file = output_path + ".mp3"

        transcript = transcribe_audio(audio_file)

        summary, notes, qa = generate_all(transcript)

        session["transcript"] = transcript
        session["summary"] = summary
        session["notes"] = notes
        session["qa"] = qa

        return render_template(
            "index.html",
            transcript=transcript,
            summary=summary,
            notes=notes,
            qa=qa,
        )

    except Exception as e:
        import traceback
        traceback.print_exc()

        return render_template(
            "index.html",
            transcript=f"❌ Error: {e}"
        )
# ---------------- RUN ---------------- #


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

