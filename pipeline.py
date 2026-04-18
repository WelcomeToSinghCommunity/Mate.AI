from summarizer import summarize_meeting
from tasks import extract_tasks

def generate_summary_and_tasks(transcript_text):
    summary = summarize_meeting(transcript_text)
    tasks = extract_tasks(transcript_text)
    return summary, tasks
