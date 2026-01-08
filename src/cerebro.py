import os
import sys
from dotenv import load_dotenv
from google import genai  # <--- Esta es la nueva libreria
from sqlalchemy.orm import sessionmaker

# Agregar directorio actual al path
sys.path.append(os.getcwd())

from src.database import engine, Noticia

# 1. Configuracion Inicial
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Error: No se encontro la GEMINI_API_KEY en el .env")

# Creamos el cliente con la nueva sintaxis
client = genai.Client(api_key=api_key)

# 2. Funcion para traer noticias de la BD
def obtener_noticias_recientes(limite=50):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        noticias = session.query(Noticia).order_by(Noticia.fecha_captura.desc()).limit(limite).all()
        return noticias
    except Exception as e:
        print(f"Error al leer la BD: {e}")
        return []
    finally:
        session.close()

# 3. Funcion para preguntarle a Gemini
def generar_reporte_seguridad():
    print("Leyendo noticias de la base de datos...")
    noticias = obtener_noticias_recientes()
    
    if not noticias:
        print("No hay noticias para analizar.")
        return

    # Preparamos el texto
    lista_titulos = [f"- {n.titulo} ({n.fuente})" for n in noticias]
    texto_noticias = "\n".join(lista_titulos)

    prompt = f"""
    Actua como un experto analista de seguridad.
    Analiza estos titulares recientes sobre crimen en Mexico:

    {texto_noticias}

    Genera un 'Reporte de Situacion' (Max 200 palabras) con:
    1. Resumen de tendencias.
    2. Puntos criticos (lugares).
    3. Nivel de Riesgo (Bajo/Medio/Alto).
    
    Formato limpio y directo.
    """

    print("Enviando datos a Gemini")
    
    try:
        # Nueva forma de llamar al modelo
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        print("\n" + "="*40)
        print("REPORTE DE INTELIGENCIA SENTINELA")
        print("="*40)
        print(response.text)
        print("="*40)
        
    except Exception as e:
        print(f"Error al generar el reporte: {e}")

if __name__ == "__main__":
    generar_reporte_seguridad()