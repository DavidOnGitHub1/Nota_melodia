import sys
import subprocess
import os
from antlr4 import *
from lenguajeLexer import lenguajeLexer
from lenguajeParser import lenguajeParser

def ejecutar_proyecto():
    # Recibir el nombre de la canción enviado desde la interfaz
    nombre_cancion = sys.argv[1] if len(sys.argv) > 1 else "mi_cancion"
    
    # Asegurar que la carpeta programa exista
    os.makedirs("programa", exist_ok=True)
    
    # Definir la ruta del archivo .bzl de entrada
    archivo_bzl = f"programa/{nombre_cancion}.bzl"
    if not os.path.exists(archivo_bzl):
        archivo_bzl = f"{nombre_cancion}.bzl"
    
    # 1. Leer con ANTLR
    try:
        input_stream = FileStream(archivo_bzl, encoding='utf-8')
        lexer = lenguajeLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = lenguajeParser(stream)
        tree = parser.programa()
        print(f"¡Análisis sintáctico exitoso para '{nombre_cancion}'!")
    except Exception as e:
        print(f"Error al analizar con ANTLR: {e}")
        return

    # 2. Extraer notas directamente del archivo .bzl (ej. f4 -> f'4)
    secuencia_notas = []
    try:
        with open(archivo_bzl, "r", encoding="utf-8") as f:
            for linea in f:
                nota_limpia = linea.strip().lower()
                if nota_limpia:
                    # Si la nota es de octava 4 (ej. f4, g4), LilyPond usa f'4, g'4
                    if nota_limpia.endswith('4'):
                        nombre_nota = nota_limpia[:-1] # quita el '4'
                        secuencia_notas.append(f"{nombre_nota}'4")
                    elif nota_limpia.endswith('3'):
                        nombre_nota = nota_limpia[:-1] # quita el '3'
                        secuencia_notas.append(f"{nombre_nota}4")
                    else:
                        secuencia_notas.append(f"{nota_limpia}4")
    except Exception as e:
        print(f"Error leyendo las notas: {e}")

    if not secuencia_notas:
        secuencia_notas = ["c'4", "e'4", "g'4"]

    string_notas = " ".join(secuencia_notas)

    # 3. Código LilyPond
    codigo_ly = '\\version "2.24.4"\n\\header { tagline = ##f }\n\\score {\n  {\n    \\clef treble\n    \\time 4/4\n    \\tempo 4 = 90\n    \\stemDown\n    ' + string_notas + '\n  }\n  \\layout { }\n  \\midi { }\n}\n'
    
    ly_path = f"programa/{nombre_cancion}.ly"
    with open(ly_path, "w", encoding="utf-8") as f:
        f.write(codigo_ly)

    print(f"Generando partitura PDF y audio para '{nombre_cancion}'...")

    base_output = f"programa/{nombre_cancion}"

    # 4. LilyPond compila a PDF y MIDI
    subprocess.run(["lilypond", "-o", base_output, ly_path])

    midi_path = f"programa/{nombre_cancion}.midi"
    wav_path = f"programa/{nombre_cancion}.wav"
    mp3_path = f"programa/{nombre_cancion}.mp3"

    # 5. Timidity convierte MIDI a WAV
    resultado = subprocess.run(["timidity", midi_path, "-Ow", "-o", wav_path])
    
    if resultado.returncode == 0:
        # 6. FFmpeg genera el MP3
        subprocess.run(["ffmpeg", "-y", "-i", wav_path, "-acodec", "libmp3lame", "-b:a", "128k", mp3_path])
        print(f"¡Listo! Archivos generados en carpeta programa/: {nombre_cancion}.pdf y {nombre_cancion}.mp3")
    else:
        print("Hubo un detalle convirtiendo el audio con timidity.")

if __name__ == "__main__":
    ejecutar_proyecto()