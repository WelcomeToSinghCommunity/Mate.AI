from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, Header
from pydantic import BaseModel
from passlib.context import CryptContext
import jwt
import whisper
from pipeline import generate_summary_and_tasks
from slack_sync import post_to_slack
from chatbot import chat_with_ollama
import tempfile

app = FastAPI()

# --- Auth setup ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "your_secret_key"
users_db = {}

class User(BaseModel):
    email: str
    password: str

@app.post("/signup")
def signup(user: User):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed_pw = pwd_context.hash(user.password)
    users_db[user.email] = hashed_pw
    return {"message": "Signup successful"}

@app.post("/login")
def login(user: User):
    if user.email not in users_db or not pwd_context.verify(user.password, users_db[user.email]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = jwt.encode({"email": user.email}, SECRET_KEY, algorithm="HS256")
    return {"token": token}

def verify_token(authorization: str = Header(...)):
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid auth scheme")
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["email"]
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# --- Whisper model ---
model = whisper.load_model("tiny")

@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    result = model.transcribe(tmp_path)
    transcript_text = result["text"]

    summary, tasks = generate_summary_and_tasks(transcript_text)

    with open("last_transcript.txt", "w", encoding="utf-8") as f:
        f.write(transcript_text)

    post_to_slack(summary, tasks)
    return {"status": "success", "summary": summary, "tasks": tasks}


@app.post("/chat")
async def chat_endpoint(question: str, filter: str = None):
    with open("last_transcript.txt", "r", encoding="utf-8") as f:
        transcript_text = f.read()

    answer = chat_with_ollama(transcript_text, question, filter)
    return {"question": question, "filter": filter, "answer": answer}

# --- Protected endpoints for dashboard ---
@app.get("/summary")
def get_summary(user: str = Depends(verify_token)):
    return {"summary": f"Meeting recap for {user}: Project deadline is April 30."}

@app.get("/tasks")
def get_tasks(user: str = Depends(verify_token)):
    return {"tasks": ["Finalize report", "Email client", "Prepare slides"]}

@app.get("/")
def home():
    return {"message": "Mate.AI backend is live!"}

