import sys
import os
# Truco para ver los modulos hermanos
sys.path.append(os.getcwd())

from src.scraper import buscar_noticias
from src.database import guardar_noticias_db
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Error: API Key no encontrada.")

client = genai.Client(api_key=api_key)

def analizar_riesgo(lugar):
    print(f"Iniciando analisis de seguridad enfocado en turismo/civil para: {lugar}")
    
    # INTENTO 1: Busqueda Especifica
    print("Buscando noticias recientes en Google (Intento 1)...")
    query = f"{lugar} violencia inseguridad balacera"
    df = buscar_noticias(query, dias=7)
    
    # INTENTO 2: Si no sale nada, buscamos mas general
    if df is None or df.empty:
        print("   -> Nada especifico, intentando busqueda general...")
        query_backup = f"{lugar} noticias policiacas"
        df = buscar_noticias(query_backup, dias=7)

    if df is None or df.empty:
        return f"REPORTE {lugar}: Google News no arrojó reportes policiacos en los últimos 7 días. Podría estar tranquilo, pero verifica fuentes locales (Twitter/FB)."

    # 2. ANALISIS DE INTELIGENCIA
    print(f"Analizando {len(df)} noticias con IA...")
    
    lista_titulos = [f"- {row['title']} ({row['published date']})" for _, row in df.iterrows()]
    texto_evidencia = "\n".join(lista_titulos[:20]) 

    prompt = f"""
    Actúa como un experto en seguridad para civiles en México. Cliente: Turista/Civil en {lugar}.

    Noticias recientes encontradas:
    {texto_evidencia}

    TU MISION:
    1. FILTRA: Ignora grilla política o incautaciones sin violencia.
    2. ENFÓCATE: Busca asaltos, bloqueos, balaceras o violencia directa.
    3. UBICA: Si mencionan colonias específicas, dilo.

    CALIBRACIÓN (0-100):
    - 0-30: Tranquilo (Incidentes aislados).
    - 31-60: Precaución (Robos comunes, no andar de noche).
    - 61-80: Peligroso (Violencia activa, asaltos violentos).
    - 81-100: ZONA DE GUERRA (Bloqueos, enfrentamientos pesados).

    FORMATO:
    NIVEL DE RIESGO: [Numero]
    ZONA CRITICA: [Todo el municipio o colonias especificas]
    RESUMEN: [Breve explicacion para el ciudadano]
    VEREDICTO: [¿Vas o no vas?]
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error al consultar el modelo: {e}"

if __name__ == "__main__":
    lugar_prueba = input("Ingrese la zona a consultar: ")
    print("\n" + "="*40)
    print(analizar_riesgo(lugar_prueba))
    print("="*40)