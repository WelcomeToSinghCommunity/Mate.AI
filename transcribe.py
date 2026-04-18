import whisper

model = whisper.load_model("base")

audio_file = "C:\\Users\\kisha\\Desktop\\Mate.AI\\sample.m4a"

result = model.transcribe(audio_file)
text = result["text"]

print("\n===== TRANSCRIPTION =====\n")
print(text)

# Save transcript to file
with open("transcript.txt", "w", encoding="utf-8") as f:
    f.write(text)