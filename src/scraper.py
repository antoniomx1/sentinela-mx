from gnews import GNews
import pandas as pd
from datetime import datetime
import os
import sys

# Agregamos el directorio actual al path para poder importar modulos hermanos
sys.path.append(os.getcwd())

from src.database import guardar_noticias_db

def buscar_noticias(tema, dias=2):
    """
    Busca noticias en Google News y las guarda en la BD.
    """
    print(f"Iniciando busqueda para: '{tema}' (Ultimos {dias} dias)")
    
    google_news = GNews(language='es', country='MX', period=f'{dias}d')
    
    try:
        noticias = google_news.get_news(tema)
    except Exception as e:
        print(f"Error al conectar con GNews: {e}")
        return None
    
    if not noticias:
        print("No se encontraron resultados.")
        return None

    # Procesamiento
    df = pd.DataFrame(noticias)
    
    if 'publisher' in df.columns:
        df['publisher'] = df['publisher'].apply(lambda x: x.get('title') if isinstance(x, dict) else x)

    # Filtrar columnas
    cols_to_keep = ['published date', 'title', 'url', 'publisher']
    existing_cols = [c for c in cols_to_keep if c in df.columns]
    df_limpio = df[existing_cols]
    
    print(f"Registros encontrados: {len(df_limpio)}")
    
    # GUARDADO EN BASE DE DATOS
    print("Guardando en base de datos...")
    guardar_noticias_db(df_limpio)
    
    return df_limpio

if __name__ == "__main__":
    # Puedes cambiar el tema aqui
    temas = ["Asaltos CDMX", "Balacera Estado de Mexico", "Crimen Organizado Mexico"]
    
    for tema in temas:
        buscar_noticias(tema)