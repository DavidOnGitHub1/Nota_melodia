import sys
import subprocess
import os
import re

def ejecutar_proyecto():
    nombre_cancion = sys.argv[1] if len(sys.argv) > 1 else "mi_cancion"
    os.makedirs("programa", exist_ok=True)
    
    archivo_bzl = f"programa/{nombre_cancion}.bzl"
    if not os.path.exists(archivo_bzl):
        archivo_bzl = f"{nombre_cancion}.bzl"
    
    # Leer y traducir notas inteligentemente (soporta octavas 3, 4, 5 y sostenidos/bemoles)
    secuencia_notas = []
    try:
        with open(archivo_bzl, "r", encoding="utf-8") as f:
            for linea in f:
                nota_limpia = linea.strip().lower()
                if not nota_limpia or "|" in nota_limpia or "main" in nota_limpia or "beethoven" in nota_limpia:
                    continue
                
                # Expresión regular para separar nombre de nota (ej. f, ais, c) y octava (ej. 3, 4, 5)
                match = re.match(r"^([a-zA-Z]+)([0-9])$", nota_limpia)
                if match:
                    nombre = match.group(1)
                    octava = int(match.group(2))
                    
                    # Convertir octava a formato LilyPond absoluto (c' es el Do central / octava 4)
                    if octava == 3:
                        sufijo_octava = ""
                    elif octava == 4:
                        sufijo_octava = "'"
                    elif octava == 5:
                        sufijo_octava = "''"
                    elif octava == 2:
                        sufijo_octava = ","
                    else:
                        sufijo_octava = "'" * (octava - 4) if octava > 4 else "," * (4 - octava)
                    
                    # Agregar nota con duración de negra (4) por defecto
                    secuencia_notas.append(f"{nombre}{sufijo_octava}4")
                else:
                    # Si viene limpia sin número, la dejamos tal cual con duración 4
                    secuencia_notas.append(f"{nota_limpia}4")
        
        print(f"Notas traducidas para LilyPond: {secuencia_notas}")
    except Exception as e:
        print(f"Error leyendo las notas: {e}")

    if not secuencia_notas:
        secuencia_notas = ["c'4", "e'4", "g'4"]

    string_notas = " ".join(secuencia_notas)

    # Crear el archivo .ly en la carpeta programa/
    codigo_ly = '\\version "2.24.4"\n\\header { tagline = ##f }\n\\score {\n  {\n    \\clef treble\n    \\time 4/4\n    \\tempo 4 = 100\n    \\stemDown\n    ' + string_notas + '\n  }\n  \\layout { }\n  \\midi { }\n}\n'
    
    ly_path = os.path.join("programa", f"{nombre_cancion}.ly")
    with open(ly_path, "w", encoding="utf-8") as f:
        f.write(codigo_ly)

    print(f"Ejecutando LilyPond para {ly_path}...")
    base_output = os.path.join("programa", nombre_cancion)
    res_lily = subprocess.run(["lilypond", "-o", base_output, ly_path], capture_output=True, text=True)
    if res_lily.returncode != 0:
        print("ERROR LILYPOND:", res_lily.stderr)
        return

    midi_path = os.path.join("programa", f"{nombre_cancion}.midi")
    wav_path = os.path.join("programa", f"{nombre_cancion}.wav")
    mp3_path = os.path.join("programa", f"{nombre_cancion}.mp3")

    # TiMidity: MIDI a WAV
    print("Ejecutando TiMidity...")
    res_timidity = subprocess.run(["timidity", midi_path, "-Ow", "-o", wav_path], capture_output=True, text=True)
    if res_timidity.returncode != 0:
        print("ERROR TIMIDITY:", res_timidity.stderr)
        return

    # FFmpeg: WAV a MP3
    print("Ejecutando FFmpeg...")
    res_ffmpeg = subprocess.run(["ffmpeg", "-y", "-i", wav_path, "-acodec", "libmp3lame", "-b:a", "128k", mp3_path], capture_output=True, text=True)
    if res_ffmpeg.returncode != 0:
        print("ERROR FFMPEG:", res_ffmpeg.stderr)
        return

    print(f"¡ÉXITO TOTAL! Audio y partitura generados correctamente en programa/.")

if __name__ == "__main__":
    ejecutar_proyecto()