import tkinter as tk
from funciones_interfaz import *
from logica import *

def limpiar_todo(): # funcion para limpiar todos los entrys, dada por chat 
    global lineas_transiciones, transiciones_data, transiciones_texto
    global palabras_entries, palabras_texto, palabras_resultados
    global transiciones, palabras_entrada
    
    # Limpiar datos globales
    lineas_transiciones.clear()
    transiciones_data.clear()
    transiciones_texto.clear()
    palabras_entries.clear()
    palabras_texto.clear()
    palabras_resultados.clear()
    transiciones.clear()
    palabras_entrada.clear()
    
    # Limpiar campos de entrada
    estado_inicial_entry.delete(0, tk.END)
    estado_final_entry.delete(0, tk.END)
    
    # Limpiar frames y recrear elementos iniciales
    for widget in frame_transiciones.winfo_children():
        if isinstance(widget, tk.Frame) and widget.winfo_name() != "btn_frame_trans":
            continue
        elif not isinstance(widget, tk.Frame):
            widget.destroy()
    
    for widget in frame_palabras.winfo_children():
        if not isinstance(widget, tk.Button):
            widget.destroy()
    
    # Recrear elementos iniciales
    tk.Label(frame_transiciones, text="δ ( q, símbolo, tope_pila ) : ( q', pila')", bg="#E6F7FF").grid(row=0, column=0, columnspan=13)
    agregar_transicion(frame_transiciones)
    agregar_transicion(frame_transiciones)
    
    agregar_palabra(frame_palabras)
    agregar_palabra(frame_palabras)

# === Pantalla ===
root = tk.Tk()
root.title("Simulador de Autómata Pushdown Determinista (APD)")

tk.Label(root, text="Simulador de Autómata Pushdown Dedterminista (APD)", font=("Arial", 16, "bold")).pack(pady=10)

frame_contenedor = tk.Frame(root)
frame_contenedor.pack(padx=10, pady=5, fill="x")
frame_contenedor.columnconfigure((0, 1, 2), weight=1, uniform="col")

# === Transiciones ===
frame_transiciones = tk.LabelFrame(frame_contenedor, text="Transiciones del APD", font=("Arial", 12, "bold"), bg="#E6F7FF")
frame_transiciones.grid(row=0, column=0, padx=(0,10), sticky="nsew")
tk.Label(frame_transiciones, text="δ ( q, símbolo, tope_pila ) = ( q', pila')", bg="#E6F7FF").grid(row=0, column=0, columnspan=13)

agregar_transicion(frame_transiciones)
agregar_transicion(frame_transiciones)

btn_frame_trans = tk.Frame(frame_transiciones, bg="#E6F7FF")
btn_frame_trans.grid(row=100, column=0, columnspan=13, pady=5)
tk.Button(btn_frame_trans, text="Agregar transición", command=lambda: agregar_transicion(frame_transiciones)).pack(side="left", padx=5)
tk.Button(btn_frame_trans, text="Editar transiciones", command=lambda: editar_todas_las_transiciones(frame_transiciones)).pack(side="left", padx=5)

# === Estados ===
frame_estados = tk.LabelFrame(frame_contenedor, text="Estados", font=("Arial", 12, "bold"), bg="#F9F7E8")
frame_estados.grid(row=0, column=1, padx=10, sticky="nsew")

tk.Label(frame_estados, text="Estado inicial:", bg="#F9F7E8").grid(row=0, column=0, sticky="w")
estado_inicial_entry = tk.Entry(frame_estados, width=15)
estado_inicial_entry.grid(row=0, column=1, pady=2)

tk.Label(frame_estados, text="Aceptación por:", bg="#F9F7E8").grid(row=1, column=0, sticky="w", pady=(10,0))
aceptacion_var = tk.StringVar(value="estado_final")
tk.Radiobutton(
    frame_estados, text="Estado final", variable=aceptacion_var, value="estado_final",
    bg="#F9F7E8", command=lambda: actualizar_estado_final_entry(aceptacion_var, estado_final_entry)
).grid(row=2, column=0, columnspan=2, sticky="w")

tk.Radiobutton(
    frame_estados, text="Stack vacío", variable=aceptacion_var, value="stack_vacio",
    bg="#F9F7E8", command=lambda: actualizar_estado_final_entry(aceptacion_var, estado_final_entry)
).grid(row=3, column=0, columnspan=2, sticky="w")

tk.Label(frame_estados, text="Estado final:", bg="#F9F7E8").grid(row=4, column=0, sticky="w", pady=(10,0))
estado_final_entry = tk.Entry(frame_estados, width=15)
estado_final_entry.grid(row=4, column=1, pady=2)
actualizar_estado_final_entry(aceptacion_var, estado_final_entry)

# === Palabras ===
frame_palabras = tk.LabelFrame(frame_contenedor, text="Palabras de entrada", font=("Arial", 12, "bold"), bg="#FDEDEC")
frame_palabras.grid(row=0, column=2, padx=(10,0), sticky="nsew")

agregar_palabra(frame_palabras)
agregar_palabra(frame_palabras)

tk.Button(frame_palabras, text="Agregar palabra", command=lambda: agregar_palabra(frame_palabras)).grid(row=100, column=0, columnspan=2, pady=5)
tk.Button(frame_palabras, text="Editar palabras", command=lambda: editar_todas_las_palabras(frame_palabras)).grid(row=100, column=3, columnspan=2, pady=5)

# === Botones inferiores ===
frame_botones = tk.Frame(root)
frame_botones.pack(pady=15)

tk.Button(frame_botones, text="Simular", width=12, 
          command=lambda: verificarDatos(frame_transiciones, frame_palabras, estado_inicial_entry, estado_final_entry, aceptacion_var)).grid(row=0, column=0, padx=10)
tk.Button(frame_botones, text="Limpiar", width=12, command=limpiar_todo).grid(row=0, column=1, padx=10)
tk.Button(frame_botones, text="Salir", width=12, command=root.destroy).grid(row=0, column=2, padx=10)

root.mainloop()