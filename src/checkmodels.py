import os
import sys
from dotenv import load_dotenv
from google import genai

# Cargar variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error: No hay API KEY.")
    sys.exit()

client = genai.Client(api_key=api_key)

print("Consultando modelos disponibles para tu cuenta...")
print("-" * 30)

try:
    # Listar todos los modelos que tengan 'gemini' en el nombre
    for m in client.models.list():
        if "gemini" in m.name:
            print(f"Nombre: {m.name}")
            
except Exception as e:
    print(f"Error al listar modelos: {e}")

print("-" * 30)