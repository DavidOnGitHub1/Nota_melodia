from flask import Flask, render_template, request, send_from_directory
import os
import subprocess

app = Flask(__name__)

# Directorio donde se guardan los archivos del programa
PROGRAMA_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'programa')

@app.route('/')
def index():
    return render_template('index.html', audio_file=None)

@app.route('/generate', methods=['POST'])
def generate():
    song_name = request.form.get('song_name', 'melodia_dta')
    notes = request.form.get('notes', '')
    
    # Ruta del archivo .bzl dentro de la carpeta programa
    bzl_path = os.path.join(PROGRAMA_DIR, f"{song_name}.bzl")
    
    # Guardar las notas ingresadas en el archivo .bzl
    with open(bzl_path, 'w', encoding='utf-8') as f:
        f.write(notes)
    
    try:
        # Ejecutar tu main.py pasando el archivo o procesando la melodía
        # Ajusta esto si tu main.py recibe argumentos específicos
        subprocess.run(["python3", "main.py"], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el compilador: {e}")
    
    # El archivo MP3 resultante que lee el reproductor
    audio_filename = f"{song_name}.mp3"
    
    return render_template('index.html', audio_file=audio_filename)

# Ruta para servir el audio desde la carpeta 'programa'
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(PROGRAMA_DIR, filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=True)