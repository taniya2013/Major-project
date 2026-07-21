import whisper

model = None

def transcribe_audio(file_path):
    global model

    if model is None:
        model = whisper.load_model("tiny")   # base ki jagah tiny

    result = model.transcribe(
        file_path,
        task="transcribe",
        language="en",
        fp16=False
    )

    return result["text"]