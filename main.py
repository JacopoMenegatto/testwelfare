# Ricreo il file main.py che includeva il prompt con le regole (quello che funzionava prima di stasera),
# quando GPT rispondeva ma con output "sporco", non JSON strutturato ma con messaggi utili.

main_con_regole = """
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
    prompt = f\"""Hai ricevuto questo testo OCR:\\n{request.file_text}\\n
Controlla se la pratica è valida secondo le regole UNICREDIT – CATEGORIA SCUOLA E ISTRUZIONE. Rispondi SOLO in JSON nei due formati previsti:

✅ Se la pratica è corretta:
{{
  "esito": "VALIDA",
  "motivazione": "ok"
}}

❌ Se NON è valida:
{{
  "esito": "NON VALIDA",
  "motivazione": "spiega cosa manca o cosa è sbagliato"
}}

🧠 Applica le seguenti regole:

1. Il nome e cognome del beneficiario deve essere specificato.
2. Il codice fiscale deve essere corretto e di 16 caratteri.
3. La causale deve contenere parole chiave come “iscrizione”, “gita scolastica”, “retta”, “libri”, ecc.
4. La data deve essere compresa tra ottobre 2024 e dicembre 2025.
5. L'importo deve essere > 0.
6. Se manca qualcosa, spiegalo.
\"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return response.choices[0].message.content
"""

# Salvo il file aggiornato
file_path = "/mnt/data/main_con_regole.py"
with open(file_path, "w") as f:
    f.write(main_con_regole)

file_path
