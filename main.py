import sys
import subprocess
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

    # 3. Código dinámico para LilyPond
    codigo_ly = f"""
    \\version "2.24.0"
    \\header {{ tagline = ##f }}
    \\score {{
      {{
        \\clef treble
        \\time 4/4
        \\tempo 4 = 90
        \\stemDown
        {string_notas}
      }}
      \\layout {{ }}
      \\midi {{ }}
    }}
    """
    
    with open(f"{nombre_base}.ly", "w", encoding="utf-8") as f:
        f.write(codigo_ly)

    print(f"Generando partitura PDF y audio para '{nombre_cancion}'...")

    # 4. LilyPond compila a .pdf y .midi
    subprocess.run(["lilypond", "-o", nombre_base, f"{nombre_base}.ly"])

    # 5. Timidity convierte MIDI a WAV
    resultado = subprocess.run(["timidity", f"{nombre_base}.midi", "-Ow", "-o", f"{nombre_base}.wav"])
    
    if resultado.returncode == 0:
        # 6. FFmpeg convierte WAV a MP3
        subprocess.run(["ffmpeg", "-y", "-i", f"{nombre_base}.wav", "-af", "volume=12dB", f"{nombre_base}.mp3"])
        print(f"¡Listo! Archivos generados: {nombre_cancion}.pdf y {nombre_cancion}.mp3")
    else:
        print("Hubo un detalle convirtiendo el audio con timidity.")

if __name__ == "__main__":
    ejecutar_proyecto()