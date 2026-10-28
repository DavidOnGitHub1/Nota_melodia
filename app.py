import streamlit as st
import subprocess
import os
import unicodedata

st.title("Generador de Melodias con ANTLR y LilyPond")

# Campo para el nombre de la cancion
nombre_cancion = st.text_input("Nombre de la cancion:", "mi_melodia")

# Caja de texto para las notas
texto_ingresado = st.text_area("Escribe tus notas (ej: c4, d4, e4, do#):", "c4\nd4\ne4")

if st.button("Convertir y Generar"):
    # Limpiar nombre de archivo
    nombre_cancion = "".join(c if c.isalnum() or c in ('_', '-') else '_' for c in nombre_cancion).lower()
    
    # Diccionario de notas
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
        'la#': 34, 'a#': 34, 'ais': 34, 'ais3': 22,
        'si': 35, 'b': 35, 'b4': 35, 'b3': 23
    }
    
    lineas = texto_ingresado.split('\n')
    contenido_bzl = "Main |:\n    Beethoven 0\n:|\n\nBeethoven x |:\n"
    
    for linea in lineas:
        nota_limpia = linea.strip().lower()
        nota_limpia = ''.join(c for c in unicodedata.normalize('NFD', nota_limpia) if unicodedata.category(c) != 'Mn')
        if nota_limpia in tabla_notas:
            contenido_bzl += f"    (:) {tabla_notas[nota_limpia]}\n"
            
    contenido_bzl += ":|"
    
    # Asegurar la carpeta programa y guardar el archivo en la raiz y dentro de programa para evitar errores de ruta
    os.makedirs("programa", exist_ok=True)
    ruta_bzl_programa = f"programa/{nombre_cancion}.bzl"
    ruta_bzl_raiz = f"{nombre_cancion}.bzl"
    
    with open(ruta_bzl_programa, "w", encoding="utf-8") as f:
        f.write(contenido_bzl)
        
    with open(ruta_bzl_raiz, "w", encoding="utf-8") as f:
        f.write(contenido_bzl)
        
    with st.spinner("Compilando con ANTLR y LilyPond..."):
        resultado = subprocess.run(["python3", "main.py", nombre_cancion])
        
    if resultado.returncode == 0:
        st.success(f"Archivos generados correctamente para '{nombre_cancion}'")
        
        # Buscar el archivo MP3 en la carpeta programa o en la raiz
        ruta_mp3_prog = f"programa/{nombre_cancion}.mp3"
        ruta_mp3_raiz = f"{nombre_cancion}.mp3"
        
        if os.path.exists(ruta_mp3_prog):
            st.audio(ruta_mp3_prog, format="audio/mp3")
        elif os.path.exists(ruta_mp3_raiz):
            st.audio(ruta_mp3_raiz, format="audio/mp3")
            
        # Boton para descargar el PDF
        ruta_pdf_prog = f"programa/{nombre_cancion}.pdf"
        ruta_pdf_raiz = f"{nombre_cancion}.pdf"
        
        pdf_final = ruta_pdf_prog if os.path.exists(ruta_pdf_prog) else (ruta_pdf_raiz if os.path.exists(ruta_pdf_raiz) else None)
        
        if pdf_final:
            with open(pdf_final, "rb") as pdf_file:
                st.download_button("Descargar Partitura PDF", pdf_file, file_name=f"{nombre_cancion}.pdf")
    else:
        st.error("Hubo un error en la compilacion.")