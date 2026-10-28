import tkinter as tk
import subprocess
import threading
import os
import unicodedata

# Diccionario ampliado para aceptar español, inglés y notación con números de octava
tabla_notas = {
    # Do / C
    'do': 24, 'c': 24, 'c4': 24, 'c3': 12,
    'do#': 25, 'c#': 25, 'cis': 25, 'cis4': 25,
   
    # Re / D
    're': 26, 'd': 26, 'd4': 26, 'd3': 14,
    're#': 27, 'd#': 27, 'dis': 27, 'dis4': 27,
   
    # Mi / E
    'mi': 28, 'e': 28, 'e4': 28, 'e3': 16,
   
    # Fa / F
    'fa': 29, 'f': 29, 'f4': 29, 'f3': 17,
    'fa#': 30, 'f#': 30, 'fis': 30, 'fis4': 30,
   
    # Sol / G
    'sol': 31, 'g': 31, 'g4': 31, 'g3': 19,
    'sol#': 32, 'g#': 32, 'gis': 32, 'gis4': 32,
   
    # La / A
    'la': 33, 'a': 33, 'a4': 33, 'a3': 21,
    'la#': 34, 'a#': 34, 'ais': 34, 'ais3': 22,
   
    # Si / B
    'si': 35, 'b': 35, 'b4': 35, 'b3': 23
}


def reproducir_audio(nombre_archivo):
    ruta_mp3 = f"programa/{nombre_archivo}.mp3"
    # Usamos comillas simples para proteger la ruta de espacios o caracteres raros
    os.system(f"ffplay -nodisp -autoexit '{ruta_mp3}' > /dev/null 2>&1")

def procesar_y_reproducir():
    # Obtener el nombre de la canción y limpiar espacios
    nombre_cancion = caja_nombre.get().strip()
    if not nombre_cancion:
        nombre_cancion = "mi_cancion"
    
    # Reemplazar espacios por guiones bajos para que la terminal no falle
    nombre_cancion = "".join(c if c.isalnum() or c in ('_', '-') else '_' for c in nombre_cancion).lower()

    # Obtener el texto exacto de las notas
    texto_ingresado = caja_notas.get("1.0", tk.END).strip().lower()
    lineas = texto_ingresado.split('\n')
    
    contenido_bzl = "Main |:\n    Beethoven 0\n:|\n\nBeethoven x |:\n"
    
    for linea in lineas:
        # Limpiar espacios y tildes, conservando el símbolo '#'
        nota_limpia = linea.strip().lower()
        nota_limpia = ''.join(c for c in unicodedata.normalize('NFD', nota_limpia) if unicodedata.category(c) != 'Mn')
        
        if nota_limpia in tabla_notas:
            numero = tabla_notas[nota_limpia]
            contenido_bzl += f"    (:) {numero}\n"
        elif nota_limpia:
            print(f"Nota desconocida ignorada: {nota_limpia}")
            
    contenido_bzl += ":|"
    
    os.makedirs("programa", exist_ok=True)
    ruta_bzl = f"programa/{nombre_cancion}.bzl"
    
    with open(ruta_bzl, "w", encoding="utf-8") as f:
        f.write(contenido_bzl)
        
    estado_lbl.config(text="Generando audio...", fg="yellow")
    ventana.update()
    
    # Ejecutar main.py pasando el nombre de la canción como argumento
    resultado = subprocess.run(["python3", "main.py", nombre_cancion])
    
    if resultado.returncode == 0:
        estado_lbl.config(text=f" Reproduciendo '{nombre_cancion}' ", fg="#4CAF50")
        
        hilo_audio = threading.Thread(target=reproducir_audio, args=(nombre_cancion,))
        hilo_audio.daemon = True
        hilo_audio.start()
    else:
        estado_lbl.config(text="Hubo un error en la compilación.", fg="red")

# --- CONFIGURACIÓN DE LA VENTANA GRÁFICA ---
ventana = tk.Tk()
ventana.title("Generador de Melodías con Sostenidos")
ventana.geometry("400x540")
ventana.configure(bg="#2b2b2b")

# Nombre de la canción
lbl_nombre = tk.Label(ventana, text="Nombre de la canción:", font=("Arial", 11, "bold"), fg="white", bg="#2b2b2b")
lbl_nombre.pack(pady=(15, 5))

caja_nombre = tk.Entry(ventana, font=("Arial", 11), bg="#1e1e1e", fg="white", insertbackground="white", width=25)
caja_nombre.pack(pady=5)
caja_nombre.insert(0, "melodia")


# Caja de texto
caja_notas = tk.Text(ventana, height=10, width=25, font=("Arial", 12), bg="#1e1e1e", fg="white", insertbackground="white")
caja_notas.pack(pady=5)

# Botón
btn_generar = tk.Button(ventana, text="Convertir", font=("Arial", 11, "bold"), bg="#4CAF50", fg="white", command=procesar_y_reproducir)
btn_generar.pack(pady=15)

# Estado
estado_lbl = tk.Label(ventana, text="", font=("Arial", 10), bg="#2b2b2b")
estado_lbl.pack(pady=5)

ventana.mainloop()