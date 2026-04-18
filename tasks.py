import requests

def extract_tasks(transcript_text):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi3",
            "prompt": f"""
You are a meeting assistant.
Extract all tasks, deadlines, and assignees from the transcript.
Format them clearly as:

- Person → Task (Deadline)

If no deadline is mentioned, write "No deadline".
If no person is mentioned, write "Unassigned".

Transcript:
{transcript_text}
""",
            "stream": False
        }
    )
    return response.json()["response"]
