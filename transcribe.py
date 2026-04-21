import whisper

model = whisper.load_model("small")

audio_file = "C:\\Users\\kisha\\Desktop\\Mate.AI\\sample.m4a"

result = model.transcribe(audio_file)
text = result["text"]

print("\n===== TRANSCRIPTION =====\n")
print(text)

with open("transcript.txt", "w", encoding="utf-8") as f:
    f.write(text)
