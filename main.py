from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

app = FastAPI()

# Abilita tutte le origini (per FlutterFlow)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Usa la variabile d'ambiente OPENAI_API_KEY
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.post("/validate")
async def validate(
    testo_documento: str = Form(...),
    anno: str = Form(...),
    causale: str = Form(...),
    contanti: str = Form(...)
):
    prompt = f"""
Stai validando una pratica di welfare per il cliente UNICREDIT, causale SCUOLA, anno {anno}.

Il testo del documento fornito è il seguente:

\"\"\"{testo_documento}\"\"\"

Regole di validazione Unicredit – causale SCUOLA:
- La ricevuta deve essere intestata al titolare o a un familiare a carico.
- La spesa deve essere riferita all’anno {anno}, oppure ai mesi di ottobre, novembre o dicembre dell’anno precedente.
- Se il pagamento è stato effettuato in contanti (contanti = {contanti}):
  - Deve essere allegato un giustificativo valido (es. timbro, firma, ricevuta firmata).
- Se non è in contanti, il pagamento deve essere tracciabile (bonifico, pagoPA, carta, ecc.).
- Deve esserci una causale che dimostri la natura scolastica della spesa.

Valuta il contenuto del documento rispetto a queste regole.

Rispondi solo con il seguente JSON:
{{
  "valido": true o false,
  "messaggio": "VALIDATA" oppure "NON VALIDATA: <motivo>"
}}
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    risultato = response.choices[0].message.content.strip()
    return eval(risultato)
