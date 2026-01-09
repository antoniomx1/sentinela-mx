import sys
import os
# Truco para ver los modulos hermanos
sys.path.append(os.getcwd())

from src.scraper import buscar_noticias
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Error: API Key no encontrada.")

client = genai.Client(api_key=api_key)

def analizar_riesgo(lugar):
    print(f"Iniciando analisis de seguridad para: {lugar}")
    
    # INTENTO 1: Busqueda Especifica
    print("Buscando noticias recientes en Google (Intento 1)...")
    query = f"{lugar} violencia crimen balacera seguridad"
    df = buscar_noticias(query, dias=7)
    
    # INTENTO 2: Si no sale nada, buscamos mas general
    if df is None or df.empty:
        print("   -> Nada especifico, intentando busqueda secundaria...")
        query_backup = f"{lugar} noticias policiacas"
        df = buscar_noticias(query_backup, dias=7)

    if df is None or df.empty:
        return f"REPORTE {lugar}: Google News no arrojó reportes policiacos en los últimos 7 días. Verifica fuentes locales."

    # 2. ANALISIS DE INTELIGENCIA
    print(f"Analizando {len(df)} noticias con IA (Filtro Geografico Activado)...")
    
    # --- CORRECCION AQUI: Quitamos row['source'] que causaba el error ---
    lista_titulos = [f"- {row['title']} - Fecha: {row['published date']}" for _, row in df.iterrows()]
    texto_evidencia = "\n".join(lista_titulos[:25]) 

    prompt = f"""
    Actúa como un analista de inteligencia experto en geografía de México.
    Tu cliente quiere saber si es seguro ir a: {lugar}.

    NOTICIAS ENCONTRADAS:
    {texto_evidencia}

    TU MISIÓN (FILTRO GEOGRÁFICO ESTRICTO):
    1. **DETECTA HOMÓNIMOS:** Muchas noticias mencionan CALLES (ej. "Calle Donato Guerra") en otras ciudades. SI LA NOTICIA OCURRIÓ EN OTRA CIUDAD Y SOLO COMPARTE EL NOMBRE DE LA CALLE, **DESCÁRTALA INMEDIATAMENTE**.
    2. **VALIDA CONTEXTO:** Si el usuario busca un municipio del Edomex y la noticia menciona lugares que NO existen ahí (ej. "Alsuper", "Frontera"), es una noticia falsa para esta búsqueda. IGNÓRALA.
    3. **SEPARA GRILLA:** Ignora pleitos políticos. Busca violencia real.

    SI DESPUÉS DE FILTRAR NO QUEDA NADA RELEVANTE:
    Dilo claramente: "Las noticias encontradas se refieren a calles con este nombre en otras ciudades, no al municipio."

    FORMATO DE RESPUESTA:
    NIVEL DE RIESGO: [0-100] (Si descartaste todo, pon 10).
    ZONA CRITICA: [Menciona dónde es el problema REAL, o "Ninguna detectada"].
    ANÁLISIS DE VERACIDAD: [Explica brevemente si descartaste noticias de otros lugares].
    RESUMEN: [Situación real del lugar solicitado].
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