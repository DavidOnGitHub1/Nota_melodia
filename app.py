from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import os
import subprocess

app = Flask(__name__)

# Directorio donde se guardarán los archivos generados
OUTPUT_DIR = '.'

@app.route('/')
def index():
    return render_template('index.html', audio_file=None)

@app.route('/generate', methods=['POST'])
def generate():
    song_name = request.form.get('song_name', 'melodia')
    notes = request.form.get('notes', '')
    
    # Aquí va la lógica de tu compilador o la llamada a tus scripts (LilyPond / TiMidity / FFmpeg)
    # Por ejemplo, guardamos las notas en un archivo .bzl temporal y ejecutamos tu lógica:
    bzl_filename = f"{song_name}.bzl"
    with open(bzl_filename, 'w') as f:
        f.write(notes)
    
    # Ejemplo de ejecución de tu backend (ajusta esto según cómo proceses tu lenguaje):
    # subprocess.run(["python3", "main.py", bzl_filename])
    
    # Nombre del archivo MP3 que genera tu sistema
    audio_filename = f"{song_name}.mp3"
    
    return render_template('index.html', audio_file=audio_filename)

# Ruta clave para que el navegador pueda descargar y reproducir el audio generado
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(OUTPUT_DIR, filename)

if __name__ == '__main__':
    # Render asigna dinámicamente el puerto mediante la variable de entorno PORT
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=True)