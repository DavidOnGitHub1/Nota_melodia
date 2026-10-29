import sys
import subprocess
import os
import re
from antlr4 import *
from lenguajeLexer import lenguajeLexer
from lenguajeParser import lenguajeParser

def ejecutar_proyecto():
    nombre_cancion = sys.argv[1] if len(sys.argv) > 1 else "mi_cancion"
    os.makedirs("programa", exist_ok=True)
    
    archivo_bzl = f"programa/{nombre_cancion}.bzl"
    if not os.path.exists(archivo_bzl):
        archivo_bzl = f"{nombre_cancion}.bzl"
    
    # 1. ANTLR
    try:
        input_stream = FileStream(archivo_bzl, encoding='utf-8')
        lexer = lenguajeLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = lenguajeParser(stream)
        tree = parser.programa()
        print(f"¡Análisis sintáctico exitoso para '{nombre_cancion}'!")
    except Exception as e:
        print(f"ERROR ANTLR: {e}")
        return

    # 2. Extraer notas
    secuencia_notas = []
    try:
        with open(archivo_bzl, "r", encoding="utf-8") as f:
            for linea in f:
                linea_limpia = linea.strip()
                if not linea_limpia or "|" in linea_limpia or "Main" in linea_limpia or "Beethoven" in linea_limpia:
                    continue
                
                match = re.match(r"^([a-zA-Z]+)([0-9]+)$", linea_limpia)
                if match:
                    nota = match.group(1).lower()
                    octava = match.group(2)
                    if octava == '4':
                        secuencia_notas.append(f"{nota}'4")
                    elif octava == '3':
                        secuencia_notas.append(f"{nota}4")
                    else:
                        secuencia_notas.append(f"{nota}{octava}")
    except Exception as e:
        print(f"ERROR leyendo notas: {e}")

    if not secuencia_notas:
        secuencia_notas = ["c'4", "e'4", "g'4"]

    string_notas = " ".join(secuencia_notas)

    # 3. LilyPond .ly
    codigo_ly = '\\version "2.24.4"\n\\header { tagline = ##f }\n\\score {\n  {\n    \\clef treble\n    \\time 4/4\n    \\tempo 4 = 90\n    \\stemDown\n    ' + string_notas + '\n  }\n  \\layout { }\n  \\midi { }\n}\n'
    
    ly_path = f"programa/{nombre_cancion}.ly"
    with open(ly_path, "w", encoding="utf-8") as f:
        f.write(codigo_ly)

    base_output = f"programa/{nombre_cancion}"

    # 4. LilyPond
    print( ejecutando_lily := f"Ejecutando LilyPond para {ly_path}..." )
    res_lily = subprocess.run(["lilypond", "-o", base_output, ly_path], capture_output=True, text=True)
    print(res_lily.stdout)
    if res_lily.returncode != 0:
        print("ERROR LILYPOND:", res_lily.stderr)
        return

    midi_path = f"programa/{nombre_cancion}.midi"
    wav_path = f"programa/{nombre_cancion}.wav"
    mp3_path = f"programa/{nombre_cancion}.mp3"

    # 5. TiMidity
    print("Ejecutando TiMidity...")
    res_timidity = subprocess.run(["timidity", midi_path, "-Ow", "-o", wav_path], capture_output=True, text=True)
    print(res_timidity.stdout)
    if res_timidity.returncode != 0:
        print("ERROR TIMIDITY:", res_timidity.stderr)
        return

    # 6. FFmpeg
    print("Ejecutando FFmpeg...")
    res_ffmpeg = subprocess.run(["ffmpeg", "-y", "-i", wav_path, "-acodec", "libmp3lame", "-b:a", "128k", mp3_path], capture_output=True, text=True)
    if res_ffmpeg.returncode == 0:
        print(f"¡ÉXITO TOTAL! Archivo MP3 generado en {mp3_path}")
    else:
        print("ERROR FFMPEG:", res_ffmpeg.stderr)

if __name__ == "__main__":
    ejecutar_proyecto()