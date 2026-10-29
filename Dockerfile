FROM python:3.10-slim

# Instalar dependencias del sistema (LilyPond, Timidity, FFmpeg)
RUN apt-get update && apt-get install -y \
    lilypond \
    timidity \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Exponer el puerto que usa Render
ENV PORT=10000
EXPOSE 10000

# Comando para iniciar la app Flask
CMD ["python3", "app.py"]