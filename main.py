import whisper
from fastapi import FastAPI, UploadFile, File
import uvicorn
from transformers import pipeline   # ✅ yeh missing tha

# Create FastAPI app
app = FastAPI()

# 🟢 Load models once (fast performance ke liye)
whisper_model = whisper.load_model("base")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# 🟢 Home route (just to test if server works)
@app.get("/")
def home():
    return {"message": "Podcast Summarizer API is running!"}


# 🟢 Summarizer route (upload audio, get summary)
@app.post("/summarize")
async def summarize_podcast(file: UploadFile = File(...)):
    # 1. Save uploaded file temporarily
    contents = await file.read()
    with open("temp_audio.mp3", "wb") as f:
        f.write(contents)

    # 2. Transcribe audio
    transcript = transcribe_audio("temp_audio.mp3")

    # 3. Summarize transcript
    summary = summarize_text(transcript)

    # 4. Send result back as JSON
    return {"transcript": transcript, "summary": summary}


# 🟢 Transcription function
def transcribe_audio(file_path):
    result = whisper_model.transcribe(file_path)
    return result["text"]

# 🟢 Summarization function
def summarize_text(text):
    summary = summarizer(text, max_length=120, min_length=40, do_sample=False)
    return summary[0]['summary_text']


# 🟢 Run FastAPI server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
