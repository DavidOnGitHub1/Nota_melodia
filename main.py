import sys
import subprocess
import os
import streamlit as st
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
    
    # Definir la ruta del archivo .bzl de entrada manejando si se ejecuta desde programa o raíz
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

    # 2.