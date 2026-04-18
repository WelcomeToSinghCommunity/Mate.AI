import requests

def summarize_meeting(transcript_text):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi3",
            "prompt": f"""
You are a meeting assistant.
Summarize the following meeting transcript in 5-7 bullet points.
Focus on:
- Key decisions
- Tasks and deadlines
- Important discussions

Transcript:
{transcript_text}
""",
            "stream": False
        }
    )
    return response.json()["response"]
