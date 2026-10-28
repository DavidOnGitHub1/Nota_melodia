import sys
import subprocess
import os
from antlr4 import *
from lenguajeLexer import lenguajeLexer
from lenguajeParser import lenguajeParser

# Diccionario actualizado para soportar octava 3 y octava 4 (con sostenidos)
notas_lilypond = {
    # --- Octava 3 (Notas más graves) ---
    12: "c",     
    14: "d",     
    16: "e",     
    17: "f",     
    19: "g",     
    21: "a",     
    22: "ais",   
    23: "b",     

    # --- Octava 4 (Octava central) ---
    24: "c'",    
    25: "cis'",  
    26: "d'",    
    27: "dis'",  
    28: "e'",    
    29: "f'",    
    30: "fis'",  
    31: "g'",    
    32: "gis'",  
    33: "a'",    
    34: "ais'",  
    35: "b'"     
}

def ejecutar_proyecto():
    # Recibir el nombre de la canción enviado desde la interfaz
    nombre_cancion = sys.argv[1] if len(sys.argv) > 1 else "mi_cancion"
    
    # Definir la ruta del archivo .bzl de entrada
    if os.path.basename(os.getcwd()) == "programa":
        archivo_bzl = f"{nombre_cancion}.bzl"
    else:
        if os.path.exists(f"programa/{nombre_cancion}.bzl"):
            archivo_bzl = f"programa/{nombre_cancion}.bzl"
        else:
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

    # 3. Código estricto asegurando \version en la primera línea exacta
    codigo_ly = '\\version "2.24.4"\n\\header { tagline = ##f }\n\\score {\n  {\n    \\clef treble\n    \\time 4/4\n    \\tempo 4 = 90\n    \\stemDown\n    ' + string_notas + '\n  }\n  \\layout { }\n  \\midi { }\n}\n'
    
    ly_path = f"{nombre_cancion}.ly"
    with open(ly_path, "w", encoding="utf-8") as f:
        f.write(codigo_ly)

    print(f"Generando partitura PDF y audio para '{nombre_cancion}'...")

    # 4. LilyPond compila directamente
    subprocess.run(["lilypond", "-o", nombre_cancion, ly_path])

    midi_path = f"{nombre_cancion}.midi"
    wav_path = f"{nombre_cancion}.wav"
    mp3_path = f"{nombre_cancion}.mp3"

    # 5. Timidity convierte MIDI a WAV
    resultado = subprocess.run(["timidity", midi_path, "-Ow", "-o", wav_path])
    
    if resultado.returncode == 0:
        # 6. FFmpeg genera el MP3 robusto
        subprocess.run(["ffmpeg", "-y", "-i", wav_path, "-acodec", "libmp3lame", "-b:a", "128k", mp3_path])
        print(f"¡Listo! Archivos generados: {nombre_cancion}.pdf y {nombre_cancion}.mp3")
    else:
        print("Hubo un detalle convirtiendo el audio con timidity.")

if __name__ == "__main__":
    ejecutar_proyecto()