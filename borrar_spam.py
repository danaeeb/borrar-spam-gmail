import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

CLIENT_ID = os.environ["GMAIL_CLIENT_ID"]
CLIENT_SECRET = os.environ["GMAIL_CLIENT_SECRET"]
REFRESH_TOKEN = os.environ["GMAIL_REFRESH_TOKEN"]

creds = Credentials(
    token=None,
    refresh_token=REFRESH_TOKEN,
    token_uri="https://oauth2.googleapis.com/token",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
)

creds.refresh(Request())

gmail = build("gmail", "v1", credentials=creds)

# Buscar correos considerados spam o promociones
consulta = "{label:spam category:promotions}"

resultado = gmail.users().messages().list(
    userId="me",
    q=consulta
).execute()

mensajes = resultado.get("messages", [])

print(f"Se han encontrado {len(mensajes)} correos candidatos.")

for mensaje in mensajes:
    gmail.users().messages().trash(
        userId="me",
        id=mensaje["id"]
    ).execute()

    print(f"Correo enviado a la papelera: {mensaje['id']}")

print("PROCESO TERMINADO.")
   
