# sentinela-mx
Bot de análisis de seguridad usando Open Data y Gemini AI
# Sentinela AI: Sistema de Inteligencia de Seguridad en Tiempo Real

> Plataforma "End-to-End" de análisis de riesgos basada en IA Generativa y Web Scraping.

Este proyecto implementa un pipeline automatizado que monitorea, extrae y analiza noticias sobre crimen y violencia en México para generar reportes de seguridad accionables para civiles y turistas.

---

## Arquitectura del Sistema

El sistema opera bajo una arquitectura modular de microservicios lógicos:

1.  **Ingesta de Datos (ETL):** Un scraper automatizado extrae noticias en tiempo real de Google News filtrando por zonas geográficas y palabras clave de alto impacto.
2.  **Almacenamiento:** Persistencia de datos históricos en Supabase (PostgreSQL) mediante SQLAlchemy ORM.
3.  **Motor de Inteligencia (AI Core):** Integración con Google Gemini 2.5 Flash para realizar análisis semántico:
    * Filtrado de "ruido" (política, delitos administrativos).
    * Clasificación de riesgo (0-100%).
    * Detección de entidades nombradas (colonias, carreteras específicas).
4.  **Interfaz de Usuario:** Despliegue de un Bot de Telegram asíncrono que entrega los reportes bajo demanda.

---

## Stack Tecnológico

* **Lenguaje:** Python 3.10+
* **IA / NLP:** Google Generative AI SDK (Gemini 2.5 Flash)
* **Base de Datos:** PostgreSQL (Supabase), SQLAlchemy
* **Data Engineering:** Pandas, Requests (Scraping)
* **Interfaz:** Python-Telegram-Bot (Async)
* **Control de Versiones:** Git / GitHub

---

## Funcionalidades Clave

* **Análisis de Sentimiento Contextual:** La IA distingue entre una noticia de "política criminal" (riesgo bajo para el civil) y "violencia en vía pública" (riesgo alto).
* **Zonificación Crítica:** Identifica si la violencia es generalizada en el municipio o focalizada en colonias específicas.
* **Respuesta en Tiempo Real:** Consulta noticias de los últimos 7 días al momento de la solicitud.
* **Interfaz Móvil:** Acceso inmediato a través de Telegram sin necesidad de dashboards complejos.

---

## Demo



> Ejemplo de Output:
> User: "Culiacán"
> Bot: "NIVEL DE RIESGO: 85. ZONA CRÍTICA: Todo el municipio... VEREDICTO: NO VAYAS."

---

## Configuración e Instalación

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/antoniomx1/sentinela-mx.git](https://github.com/antoniomx1/sentinela-mx.git)
    cd sentinela-mx
    ```

2.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configurar Variables de Entorno (.env):**
    Crea un archivo .env en la raíz con las siguientes credenciales:
    ```ini
    DATABASE_URL="postgresql://usuario:password@host:port/database"
    GEMINI_API_KEY="tu_api_key_de_google"
    TELEGRAM_TOKEN="tu_token_de_telegram"
    ```

4.  **Ejecutar el Bot:**
    ```bash
    python src/bot_telegram.py
    ```

---

## Autor

**Antonio Velázquez**
*Data Engineer *
[LinkedIn](https://www.linkedin.com/in/antonio-velazquez-mx) | [GitHub](https://github.com/antoniomx1)

---
*Este proyecto es de uso educativo y demostrativo.*