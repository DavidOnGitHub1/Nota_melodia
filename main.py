import sys
import subprocess
import os
import re
import shutil

def ejecutar_proyecto():
    nombre_cancion = sys.argv[1] if len(sys.argv) > 1 else "mi_cancion"
    os.makedirs("programa", exist_ok=True)
    
    # Buscar el archivo .bzl en programa/ o en la raíz
    archivo_bzl = os.path.join("programa", f"{nombre_cancion}.bzl")
    if not os.path.exists(archivo_bzl):
        archivo_bzl = f"{nombre_cancion}.bzl"
    
    # Leer y traducir notas inteligentemente
    secuencia_notas = []
    try:
        with open(archivo_bzl, "r", encoding="utf-8") as f:
            for linea in f:
                nota_limpia = linea.strip().lower()
                if not nota_limpia or "|" in nota_limpia or "main" in nota_limpia or "beethoven" in nota_limpia:
                    continue
                
                match = re.match(r"^([a-zA-Z]+)([0-9])$", nota_limpia)
                if match:
                    nombre = match.group(1)
                    octava = int(match.group(2))
                    
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
                    
                    secuencia_notas.append(f"{nombre}{sufijo_octava}4")
                else:
                    secuencia_notas.append(f"{nota_limpia}4")
        
        print(f"Notas traducidas para LilyPond: {secuencia_notas}")
    except Exception as e:
        print(f"Error leyendo las notas: {e}")

    if not secuencia_notas:
        secuencia_notas = ["c'4", "e'4", "g'4"]

    string_notas = " ".join(secuencia_notas)

    # Crear el archivo .ly en la RAIZ (evita el error de LilyPond)
    # El código .ly debe tener layout (para PDF) y midi (para audio)
   codigo_ly = '\\version "2.24.4"\n\\header { tagline = ##f }\n\\score {\n  {\n    \\clef treble\n    \\time 4/4\n    \\tempo 4 = 72\n    \\stemDown\n    ' + string_notas + '\n  }\n  \\layout { }\n  \\midi { }\n}\n'
    with open(ly_file, "w", encoding="utf-8") as f:
        f.write(codigo_ly)

    print(f"Ejecutando LilyPond para {ly_file}...")
    res_lily = subprocess.run(["lilypond", ly_file], capture_output=True, text=True)
    print(res_lily.stdout)
    if res_lily.returncode != 0:
        print("ERROR LILYPOND:", res_lily.stderr)
        return

    midi_file = f"{nombre_cancion}.midi"
    wav_file = f"{nombre_cancion}.wav"
    mp3_file = f"{nombre_cancion}.mp3"
    pdf_file = f"{nombre_cancion}.pdf"

    # TiMidity: MIDI a WAV
    print("Ejecutando TiMidity...")
    res_timidity = subprocess.run(["timidity", midi_file, "-Ow", "-o", wav_file], capture_output=True, text=True)
    if res_timidity.returncode != 0:
        print("ERROR TIMIDITY:", res_timidity.stderr)
        return

    # FFmpeg: WAV a MP3
    print("Ejecutando FFmpeg...")
    res_ffmpeg = subprocess.run(["ffmpeg", "-y", "-i", wav_file, "-acodec", "libmp3lame", "-b:a", "128k", mp3_file], capture_output=True, text=True)
    if res_ffmpeg.returncode != 0:
        print("ERROR FFMPEG:", res_ffmpeg.stderr)
        return

    # Mover todo lo generado a la carpeta programa/ para que Flask los encuentre
    for ext in [".ly", ".midi", ".wav", ".mp3", ".pdf", ".bzl"]:
        archivo_local = f"{nombre_cancion}{ext}"
        if os.path.exists(archivo_local):
            shutil.move(archivo_local, os.path.join("programa", archivo_local))

    print(f"¡ÉXITO TOTAL! Archivos movidos a programa/ con éxito.")

if __name__ == "__main__":
    ejecutar_proyecto()