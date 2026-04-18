import google.generativeai as genai

# 🔑 Add your Gemini API key
genai.configure(api_key="YOUR_GEMINI_API_KEY")

# Load transcript
with open("transcript.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Load model
model = genai.GenerativeModel("gemini-1.5-pro")

# Ask Gemini to summarize
response = model.generate_content(
    f"""
    You are an AI assistant that summarizes meetings.

    Convert this meeting transcript into:
    - Bullet points
    - Key decisions
    - Action items

    Transcript:
    {text}
    """
)

summary = response.text

print("\n===== SUMMARY =====\n")
print(summary)

# Save output
with open("summary.txt", "w", encoding="utf-8") as f:
    f.write(summary)