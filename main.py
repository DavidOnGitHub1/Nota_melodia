import sys
import subprocess
import os
from antlr4 import *
from lenguajeLexer import lenguajeLexer
from lenguajeParser import lenguajeParser

# Diccionario actualizado para soportar octava 3 y octava 4 (con sostenidos)
notas_lilypond = {
    # --- Octava 3 (Notas más graves / "gruesas") ---
    12: "c",     # c3 / do grave
    14: "d",     # d3 / re grave
    16: "e",     # e3 / mi grave
    17: "f",     # f3 / fa grave
    19: "g",     # g3 / sol grave
    21: "a",     # a3 / la grave
    22: "ais",   # ais3 / la# grave
    23: "b",     # b3 / si grave

    # --- Octava 4 (Octava central) ---
    24: "c'",    # c4 / do
    25: "cis'",  # c#4 / do#
    26: "d'",    # d4 / re
    27: "dis'",  # d#4 / re#
    28: "e'",    # e4 / mi
    29: "f'",    # f4 / fa
    30: "fis'",  # f#4 / fa#
    31: "g'",    # g4 / sol
    32: "gis'",  # g#4 / sol#
    33: "a'",    # a4 / la
    34: "ais'",  # a#4 / la#
    35: "b'"     # b4 / si
}

def ejecutar_proyecto():
    # Recibir el nombre de la canción enviado desde la interfaz
    nombre_cancion = sys.argv[1] if len(sys.argv) > 1 else "mi_cancion"
    
    # Asegurar que la carpeta programa exista
    os.makedirs("programa", exist_ok=True)
    
    # Manejar rutas flexibles por si cambia el directorio de trabajo
    if os.path.basename(os.getcwd()) == "programa":
        archivo_bzl = f"{nombre_cancion}.bzl"
        nombre_base = f"{nombre_cancion}"
    else:
        archivo_bzl = f"programa/{nombre_cancion}.bzl"
        nombre_base = f"programa/{nombre_cancion}"
    
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

    # 2. Extraer notas del archivo .bzl
    secuencia_notas = []
    try:
        with open(archivo_bzl, "r", encoding="utf-8") as f:
            for linea in f:
                if "(:)" in linea:
                    partes = linea.split("(:)")
                    if len(partes) > 1:
                        num = int(partes[1].strip())
                        if num in notas_lilypond:
                            secuencia_notas.append(notas_lilypond[num] + "4")
    except Exception as e:
        print(f"Error leyendo las notas: {e}")

    if not secuencia_notas:
        secuencia_notas = ["c'4", "e'4", "g'4"]

    string_notas = " ".join(secuencia_notas)

    # 3. Código dinámico para LilyPond (Asegurando \version "2.24.4" estricto en la línea 1)
    codigo_ly = f'\\version "2.24.4"\\n\\header {{ tagline = ##f }}\\n\\score {{\n  {{\n    \\clef treble\n    \\time 4/4\n    \\tempo 4 = 90\n    \\stemDown\n    {string_notas}\n  }}\n  \\layout {{ }}\n  \\midi {{ }}\n}}\n'
    
    ly_path = f"{nombre_base}.ly"
    with open(ly_path, "w", encoding="utf-8") as f:
        f.write(codigo_ly)

    print(f"Generando partitura PDF y audio para '{nombre_cancion}'...")

    # 4. LilyPond compila a .pdf y .midi
    subprocess.run(["lilypond", "-o", nombre_base, ly_path])

    midi_path = f"{nombre_base}.midi"
    wav_path = f"{nombre_base}.wav"
    mp3_path = f"{nombre_base}.mp3"

    # 5. Timidity convierte MIDI a WAV
    resultado = subprocess.run(["timidity", midi_path, "-Ow", "-o", wav_path])
    
    if resultado.returncode == 0:
        # 6. FFmpeg convierte WAV a MP3
        subprocess.run(["ffmpeg", "-y", "-i", wav_path, "-af", "volume=12dB", mp3_path])
        print(f"¡Listo! Archivos generados: {nombre_cancion}.pdf y {nombre_cancion}.mp3")
    else:
        print("Hubo un detalle convirtiendo el audio con timidity.")

if __name__ == "__main__":
    ejecutar_proyecto()