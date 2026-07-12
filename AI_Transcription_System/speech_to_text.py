import whisper

model = whisper.load_model("medium")

def transcribe_audio(file_path):
    result = model.transcribe(
        file_path,
        task="transcribe",
        language="en",  
        fp16=False
      
    )

    return result["text"]