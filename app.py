# Step 1: Import libraries
import whisper
from transformers import pipeline

# Step 2: Function for transcribing audio (speech → text)
def transcribe_audio(file_path):
    model = whisper.load_model("base")   # whisper model load karo
    result = model.transcribe(file_path) # audio file ko text me badlo
    return result["text"]

# Step 3: Function for summarizing text
def summarize_text(text):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(text, max_length=120, min_length=40, do_sample=False)
    return summary[0]['summary_text']

# Step 4: Run the program
if __name__ == "__main__":
    # File name manually likho
    file_path = "my_podcast.mp3"   # apni podcast file ka naam
    print("🎙️ Transcribing audio...")
    transcript = transcribe_audio(file_path)
    
    print("\n--- Transcript (first 300 words) ---\n")
    words = transcript.split()[:300]   # sirf 300 words lo
    print(" ".join(words))
    
    print("\n📝 Summarizing transcript...\n")
    summary = summarize_text(transcript)
    print("✅ Podcast Summary:\n", summary)

    # Save summary automatically
    with open("podcast_summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)

    print("✅ Summary automatically saved to podcast_summary.txt")
