# Usamos una imagen oficial de Python
FROM python:3.10-slim

# Instalamos LilyPond, Timidity y FFmpeg directamente en el servidor de la nube
RUN apt-get update && apt-get install -y \
    lilypond \
    timidity \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Directorio de trabajo en el contenedor
WORKDIR /app

# Copiamos los archivos del proyecto al contenedor
COPY . /app

# Instalamos las librerías de Python
RUN pip install --no-cache-dir -r requirements.txt

# Puerto en el que correrá Streamlit
EXPOSE 8501

# Comando para iniciar la aplicación web
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
