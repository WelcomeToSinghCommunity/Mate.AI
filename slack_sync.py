import os
import requests

SLACK_TOKEN = os.getenv("SLACK_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

def post_to_slack(summary, tasks):
    url = "https://slack.com/api/chat.postMessage"
    headers = {"Authorization": f"Bearer {SLACK_TOKEN}"}

    # Ensure tasks is a list
    if isinstance(tasks, str):
        tasks_list = tasks.split("\n")  # split string into lines
    else:
        tasks_list = tasks

    message = f"📋 *Meeting Summary*\n{summary}\n\n✅ *Tasks:*\n" + "\n".join([f"- {t}" for t in tasks_list])

    data = {"channel": CHANNEL_ID, "text": message}
    response = requests.post(url, headers=headers, json=data)

    if response.json().get("ok"):
        print("✅ Message posted successfully")
    else:
        print(f"❌ Error: {response.json()}")

