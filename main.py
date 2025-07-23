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
    prompt = f"""
Hai ricevuto questo testo OCR:
{request.file_text}

Controlla se rispetta le regole UNICREDIT SCUOLA.
Rispondi SOLO in JSON.

Regole principali:
1. La data della fattura e del pagamento devono essere nell’anno corretto.
2. L’attestato di pagamento deve essere presente, leggibile e riferito alla fattura.
3. Il pagamento deve essere tracciabile (bonifico, carta, ecc. – no contanti).
4. L’importo richiesto nel portale (“Importo”) deve essere:
   - ≥ 0,01 €
   - ≤ importo effettivamente pagato (non della fattura).
   - Anche se la fattura è più alta, conta solo quanto è stato pagato.

Se tutto è ok:
{{
  "esito": "VALIDA",
  "motivazione": "ok"
}}
Se manca qualcosa:
{{
  "esito": "NON VALIDA",
  "motivazione": "spiega bene cosa manca"
}}
"""


    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return response.choices[0].message.content
