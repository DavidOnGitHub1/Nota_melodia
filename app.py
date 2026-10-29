import os
import subprocess
import unicodedata
from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    audio_file = None
    pdf_file = None
    texto_ingresado = "c4\nd4\ne4"  # Notas por defecto

    if request.method == 'POST':
        nombre_cancion = request.form.get('nombre', 'melodia')
        texto_ingresado = request.form.get('notas', '')

        # Limpiar caracteres especiales del nombre
        nombre_cancion = "".join(c if c.isalnum() or c in ('_', '-') else '_' for c in nombre_cancion).lower()

        # Diccionario de notas musicales
        tabla_notas = {
            'do': 24, 'c': 24, 'c4': 24, 'c3': 12,
            'do#': 25, 'c#': 25, 'cis': 25, 'cis4': 25,
            're': 26, 'd': 26, 'd4': 26, 'd3': 14,
            're#': 27, 'd#': 27, 'dis': 27, 'dis4': 27,
            'mi': 28, 'e': 28, 'e4': 28, 'e3': 16,
            'fa': 29, 'f': 29, 'f4': 29, 'f3': 17,
            'fa#': 30, 'f#': 30, 'fis': 30, 'fis4': 30,
            'sol': 31, 'g': 31, 'g4': 31, 'g3': 19,
            'sol#': 32, 'g#': 32, 'gis': 32, 'gis4': 32,
            'la': 33, 'a': 33, 'a4': 33, 'a3': 21,
            'la#': 34, 'a#': 34, 'ais': 34, 'ais3': 22, 'ais4': 34, 'bes4': 34,
            'si': 35, 'b': 35, 'b4': 35, 'b3': 23,
            'eb4': 27, 'f5': 41, 'g5': 43, 'a5': 45, 'c5': 36, 'd5': 38, 'e5': 40,
            'f#4': 30, 'f#5': 42, 'g#4': 32, 'c#5': 37
        }

        lineas = texto_ingresado.split('\n')
        contenido_bzl = "Main |:\n    Beethoven 0\n:|\n\nBeethoven x |:\n"

        for linea in lineas:
            nota_limpia = linea.strip().lower()
            nota_limpia = ''.join(c for c in unicodedata.normalize('NFD', nota_limpia) if unicodedata.category(c) != 'Mn')
            if nota_limpia in tabla_notas:
                contenido_bzl += f"    (:) {tabla_notas[nota_limpia]}\n"

        contenido_bzl += ":|"

        os.makedirs("programa", exist_ok=True)
        ruta_bzl = f"programa/{nombre_cancion}.bzl"
        with open(ruta_bzl, "w", encoding="utf-8") as f:
            f.write(contenido_bzl)

        # Ejecutar el script principal de compilación
        subprocess.run(["python3", "main.py", nombre_cancion])

        if os.path.exists(f"programa/{nombre_cancion}.mp3"):
            audio_file = f"{nombre_cancion}.mp3"
        if os.path.exists(f"programa/{nombre_cancion}.pdf"):
            pdf_file = f"{nombre_cancion}.pdf"

    return render_template('index.html', audio_file=audio_file, pdf_file=pdf_file, notas_ingresadas=texto_ingresado)

@app.route('/programa/<filename>')
def download_file(filename):
    return send_from_directory('programa', filename)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)