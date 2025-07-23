from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

# Abilita CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class FileRequest(BaseModel):
    file_text: str

@app.post("/validate")
async def validate_practice(request: FileRequest):
    prompt = f"""Hai ricevuto questo testo OCR:\n{request.file_text}\n
Controlla se rispetta le regole UNICREDIT SCUOLA.
Rispondi SOLO con JSON. Se va bene:
{{
  "esito": "VALIDA",
  "motivazione": "ok"
}}
Se manca qualcosa, scrivi:
{{
  "esito": "NON VALIDA",
  "motivazione": "spiega cosa manca"
}}"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return response.choices[0].message.content
