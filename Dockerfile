FROM python:3.10-slim

# Instalar dependencias del sistema: Java, LilyPond, TiMidity, sonidos (freepats), FFmpeg y herramientas
RUN apt-get update && apt-get install -y \
    default-jre \
    lilypond \
    timidity \
    freepats \
    ffmpeg \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Descargar ANTLR completo en el contenedor
RUN curl -o /usr/local/lib/antlr-4.13.1-complete.jar https://www.antlr.org/download/antlr-4.13.1-complete.jar

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements e instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código del proyecto al contenedor
COPY . .

# Generar automáticamente los archivos de ANTLR dentro de Render
RUN java -jar /usr/local/lib/antlr-4.13.1-complete.jar -Dlanguage=Python3 -visitor -listener lenguaje.g4

# Exponer el puerto de Flask
EXPOSE 10000

# Comando para arrancar la aplicación web
CMD ["python3", "app.py"]