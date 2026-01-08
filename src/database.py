import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from datetime import datetime

# Cargar variables de entorno
load_dotenv()

# Configuracion de la BD
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("Error: No se encontro la variable DATABASE_URL en el archivo .env")

# Crear el motor de conexion
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Definicion del Modelo
class Noticia(Base):
    __tablename__ = "noticias"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    url = Column(String, unique=True, nullable=False)
    fuente = Column(String)
    fecha_publicacion = Column(String)
    fecha_captura = Column(DateTime, default=datetime.utcnow)

# Funcion para inicializar la BD
def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        print("Tablas creadas o verificadas exitosamente en Supabase.")
    except Exception as e:
        print(f"Error al conectar con la base de datos: {e}")

# Funcion para guardar un DataFrame
def guardar_noticias_db(df):
    session = SessionLocal()
    contador = 0
    try:
        for _, row in df.iterrows():
            # Validar existencia para evitar duplicados
            existe = session.query(Noticia).filter_by(url=row['url']).first()
            if not existe:
                nueva_noticia = Noticia(
                    titulo=row['title'],
                    url=row['url'],
                    fuente=row['publisher'],
                    fecha_publicacion=row['published date']
                )
                session.add(nueva_noticia)
                contador += 1
        
        session.commit()
        print(f"Se guardaron {contador} noticias nuevas en la base de datos.")
    except Exception as e:
        session.rollback()
        print(f"Error durante la transaccion: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    print("Iniciando prueba de conexion...")
    init_db()