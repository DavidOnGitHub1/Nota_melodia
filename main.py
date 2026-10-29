import sys
import subprocess
import os

def ejecutar_proyecto():
    nombre_cancion = sys.argv[1] if len(sys.argv) > 1 else "mi_cancion"
    os.makedirs("programa", exist_ok=True)
    
    archivo_bzl = f"programa/{nombre_cancion}.bzl"
    if not os.path.exists(archivo_bzl):
        archivo_bzl = f"{nombre_cancion}.bzl"
    
    # Leer las notas directamente línea por línea
    secuencia_notas = []
    try:
        with open(archivo_bzl, "r", encoding="utf-8") as f:
            for linea in f:
                nota_limpia = linea.strip().lower()
                # Ignorar líneas vacías o de estructura
                if not nota_limpia or "|" in nota_limpia or "main" in nota_limpia or "beethoven" in nota_limpia:
                    continue
                
                # Si la nota termina en 4 (ej. f4, g4), LilyPond usa f'4, g'4
                if nota_limpia.endswith('4'):
                    nombre = nota_limpia[:-1]
                    secuencia_notas.append(f"{nombre}'4")
                elif nota_limpia.endswith('3'):
                    nombre = nota_limpia[:-1]
                    secuencia_notas.append(f"{nombre}4")
                else:
                    secuencia_notas.append(f"{nota_limpia}4")
        
        print(f"Notas extraídas con éxito: {secuencia_notas}")
    except Exception as e:
        print(f"Error leyendo las notas: {e}")

    if not secuencia_notas:
        secuencia_notas = ["c'4", "e'4", "g'4"]

    string_notas = " ".join(secuencia_notas)

    # Generar código LilyPond
    codigo_ly = '\\version "2.24.4"\n\\header { tagline = ##f }\n\\score {\n  {\n    \\clef treble\n    \\time 4/4\n    \\tempo 4 = 90\n    \\stemDown\n    ' + string_notas + '\n  }\n  \\layout { }\n  \\midi { }\n}\n'
    
    ly_path = f"programa/{nombre_cancion}.ly"
    with open(ly_path, "w", encoding="utf-8") as f:
        f.write(codigo_ly)

    base_output = f"programa/{nombre_cancion}"

    # 1. LilyPond -> PDF y MIDI
    res_lily = subprocess.run(["lilypond", "-o", base_output, ly_path], capture_output=True, text=True)
    if res_lily.returncode != 0:
        print("ERROR LILYPOND:", res_lily.stderr)
        return

    midi_path = f"programa/{nombre_cancion}.midi"
    wav_path = f"programa/{nombre_cancion}.wav"
    mp3_path = f"programa/{nombre_cancion}.mp3"

    # 2. TiMidity -> MIDI a WAV
    res_timidity = subprocess.run(["timidity", midi_path, "-Ow", "-o", wav_path], capture_output=True, text=True)
    if res_timidity.returncode != 0:
        print("ERROR TIMIDITY:", res_timidity.stderr)
        return

    # 3. FFmpeg -> WAV a MP3 robusto
    res_ffmpeg = subprocess.run(["ffmpeg", "-y", "-i", wav_path, "-acodec", "libmp3lame", "-b:a", "128k", mp3_path], capture_output=True, text=True)
    if res_ffmpeg.returncode == 0:
        print(f"¡ÉXITO! Archivo MP3 generado correctamente en {mp3_path}")
    else:
        print("ERROR FFMPEG:", res_ffmpeg.stderr)

if __name__ == "__main__":
    ejecutar_proyecto()