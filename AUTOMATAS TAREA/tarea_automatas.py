import tkinter as tk
from funciones_interfaz import *
from logica import *

# === Pantalla ===
root = tk.Tk()
root.title("Simulador de Autómata Pushdown Determinista (APD)")

tk.Label(root, text="Simulador de Autómata Pushdown Determinista (APD)", font=("Arial", 16, "bold")).pack(pady=10)

frame_contenedor = tk.Frame(root)
frame_contenedor.pack(padx=10, pady=5, fill="x")
frame_contenedor.columnconfigure((0, 1, 2), weight=1, uniform="col")

# === Transiciones ===
frame_transiciones = tk.LabelFrame(frame_contenedor, text="Transiciones del APD", bg="#E6F7FF")
frame_transiciones.grid(row=0, column=0, padx=(0,10), sticky="nsew")
tk.Label(frame_transiciones, text="δ ( q, símbolo, tope_pila ) : ( q', pila')", bg="#E6F7FF").grid(row=0, column=0, columnspan=13)

agregar_transicion(frame_transiciones)
agregar_transicion(frame_transiciones)

btn_frame_trans = tk.Frame(frame_transiciones, bg="#E6F7FF")
btn_frame_trans.grid(row=100, column=0, columnspan=13, pady=5)
tk.Button(btn_frame_trans, text="Agregar transición", command=lambda: agregar_transicion(frame_transiciones)).pack(side="left", padx=5)
tk.Button(btn_frame_trans, text="Editar transiciones", command=lambda: editar_todas_las_transiciones(frame_transiciones)).pack(side="left", padx=5)

# === Estados ===
frame_estados = tk.LabelFrame(frame_contenedor, text="Estados", bg="#F9F7E8")
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
frame_palabras = tk.LabelFrame(frame_contenedor, text="Palabras de entrada", bg="#FDEDEC")
frame_palabras.grid(row=0, column=2, padx=(10,0), sticky="nsew")

agregar_palabra(frame_palabras)
agregar_palabra(frame_palabras)

tk.Button(frame_palabras, text="Agregar palabra", command=lambda: agregar_palabra(frame_palabras)).grid(row=100, column=0, columnspan=2, pady=5)

# === Botones inferiores ===
frame_botones = tk.Frame(root)
frame_botones.pack(pady=15)

tk.Button(frame_botones, text="Simular", width=12, command=simularAPD).grid(row=0, column=0, padx=10)
tk.Button(frame_botones, text="Limpiar", width=12).grid(row=0, column=1, padx=10)
tk.Button(frame_botones, text="Salir", width=12, command=root.destroy).grid(row=0, column=2, padx=10)

root.mainloop()