import requests

def chat_with_ollama(transcript_text, user_question, filter_type=None):
    filter_rules = ""
    if filter_type == "deadlines":
        filter_rules = "- Extract ONLY deadlines mentioned.\n"
    elif filter_type == "tasks":
        filter_rules = "- Extract ONLY tasks discussed.\n"
    elif filter_type == "decisions":
        filter_rules = "- Extract ONLY decisions made.\n"
    elif filter_type == "risks":
        filter_rules = "- Extract ONLY risks, blockers, or concerns.\n"
    elif filter_type == "mood":
        filter_rules = "- Analyze sentiment: positive, negative, stressed.\n"
    elif filter_type == "followups":
        filter_rules = "- List unanswered questions or follow-ups needed.\n"

    full_prompt = f"""
    You are a meeting assistant.

    Strict rules:
    - Answer ONLY from the transcript
    - If answer is not present, say: "Not mentioned in the transcript"
    - Give short and clear answers
    {filter_rules}

    Transcript:
    {transcript_text}

    Question:
    {user_question}
    """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "phi3", "prompt": full_prompt, "stream": False}
    )
    return response.json()["response"]
