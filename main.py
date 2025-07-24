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

1. ❗ **Causale unica per pratica**: ogni pratica può contenere UNA sola causale (es. retta, mensa, gita). Anche se il pagamento contiene più voci, l'importo richiesto deve riferirsi a UNA sola causale.

2. 💶 **Importo richiesto**: l'importo indicato nel portale può essere qualsiasi cifra compresa tra 0,01 € e l’importo effettivamente pagato (non l’importo della fattura). È normale che l’importo richiesto sia solo una parte.

3. 🏷️ **Nome beneficiario**: deve essere specificato il nome del figlio beneficiario, leggibile nel giustificativo o nel pagamento. Il cognome può essere diverso da quello del titolare.

4. 📅 **Anno corretto**: il pagamento o la prestazione devono riferirsi all’anno selezionato nel portale (es. 2025). Per Unicredit sono accettate anche spese di ottobre, novembre e dicembre dell’anno precedente.

5. 💳 **Metodo di pagamento ammesso**:
   - Bonifico, MAV, PagoPA, carta, bancomat, Satispay, estratto conto, ricevuta fiscale.
   - Non sono ammessi contanti (salvo casi eccezionali con conferma esplicita).

6. 🧾 **Giustificativi validi**: tra i giustificativi ammessi: ricevuta fiscale, fattura, ricevuta elettronica, MAV, dichiarazione della scuola con data, firma e intestazione.

7. 🏫 **Intestatario del pagamento**: il pagamento può essere intestato al titolare del piano o al figlio beneficiario. È importante che almeno uno dei due sia chiaramente visibile.

8. ⚠️ **Spese non rimborsabili**: non sono ammesse:
   - Quota associativa, tesseramento, materiale scolastico, feste, picnic, foto di classe, assicurazioni.
   - Multe, more, penalità.
   - Voucher, bollo, commissioni.

Verifica attentamente che la pratica rispetti TUTTI questi criteri. Se manca anche uno solo, classifica come NON VALIDA e spiega perché.
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
