from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import os
import subprocess
import time

app = Flask(__name__)

PROGRAMA_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'programa')

@app.route('/')
def index():
    return render_template('index.html', audio_file=None, pdf_file=None, notes="")

@app.route('/generate', methods=['GET', 'POST'])
def generate():
    if request.method == 'POST':
        song_name_input = request.form.get('song_name', 'melodia')
        song_name = f"{song_name_input}_{int(time.time())}"
        raw_notes = request.form.get('notes', '')
        
        os.makedirs(PROGRAMA_DIR, exist_ok=True)
        bzl_path = os.path.join(PROGRAMA_DIR, f"{song_name}.bzl")
        
        with open(bzl_path, 'w', encoding='utf-8') as f:
            f.write(raw_notes)
        
        try:
            subprocess.run(["python3", "main.py", song_name], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error al ejecutar el compilador: {e}")
        
        audio_filename = f"{song_name}.mp3"
        pdf_filename = f"{song_name}.pdf"
        
        # Devolvemos también 'notes=raw_notes' para que no se borre el texto de la caja
        return render_template('index.html', audio_file=audio_filename, pdf_file=pdf_filename, notes=raw_notes)
    
    return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(PROGRAMA_DIR, filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=True)