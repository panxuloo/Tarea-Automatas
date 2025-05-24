import tkinter as tk

# === Datos ===
lineas_transiciones = []
transiciones_data = []
transiciones_texto = []

palabras_entries = []
palabras_texto = []

# === Funciones ===
def agregar_transicion():
    index = len(lineas_transiciones)
    fila = index + 1
    entradas = []

    tk.Label(frame_transiciones, text=f"{index+1}. δ (", bg="#E6F7FF").grid(row=fila, column=0, sticky="e")

    for i in range(3):
        e = tk.Entry(frame_transiciones, width=6)
        e.grid(row=fila, column=1 + 2 * i)
        entradas.append(e)
        if i < 2:
            tk.Label(frame_transiciones, text=",", bg="#E6F7FF").grid(row=fila, column=2 + 2 * i)

    tk.Label(frame_transiciones, text=") : (", bg="#E6F7FF").grid(row=fila, column=7)

    for i in range(2):
        e = tk.Entry(frame_transiciones, width=6)
        e.grid(row=fila, column=8 + 2 * i)
        entradas.append(e)
        if i == 0:
            tk.Label(frame_transiciones, text=",", bg="#E6F7FF").grid(row=fila, column=9)

    tk.Label(frame_transiciones, text=")", bg="#E6F7FF").grid(row=fila, column=12)

    entradas[-1].bind("<Return>", lambda event, idx=index: transformar_transicion_a_texto(idx))

    lineas_transiciones.append(entradas)
    transiciones_data.append([""] * 5)
    transiciones_texto.append(None)

def transformar_transicion_a_texto(index):
    fila = index + 1
    datos = [e.get() for e in lineas_transiciones[index]]
    if not all(datos):
        return

    transiciones_data[index] = datos

    for widget in frame_transiciones.grid_slaves(row=fila):
        widget.destroy()

    texto = f"{index+1}. δ({datos[0]}, {datos[1]}, {datos[2]}) : ({datos[3]}, {datos[4]})"
    label = tk.Label(frame_transiciones, text=texto, bg="#E6F7FF", anchor="w")
    label.grid(row=fila, column=0, columnspan=13, sticky="w")

    transiciones_texto[index] = (label,)

def editar_todas_las_transiciones():
    for idx, texto_info in enumerate(transiciones_texto):
        if texto_info is None:
            continue
        fila = idx + 1
        texto_info[0].destroy()

        entradas = []
        tk.Label(frame_transiciones, text=f"{idx+1}. δ (", bg="#E6F7FF").grid(row=fila, column=0, sticky="e")

        for i in range(3):
            e = tk.Entry(frame_transiciones, width=6)
            e.insert(0, transiciones_data[idx][i])
            e.grid(row=fila, column=1 + 2 * i)
            entradas.append(e)
            if i < 2:
                tk.Label(frame_transiciones, text=",", bg="#E6F7FF").grid(row=fila, column=2 + 2 * i)

        tk.Label(frame_transiciones, text=") : (", bg="#E6F7FF").grid(row=fila, column=7)

        for i in range(2):
            e = tk.Entry(frame_transiciones, width=6)
            e.insert(0, transiciones_data[idx][3 + i])
            e.grid(row=fila, column=8 + 2 * i)
            entradas.append(e)
            if i == 0:
                tk.Label(frame_transiciones, text=",", bg="#E6F7FF").grid(row=fila, column=9)

        tk.Label(frame_transiciones, text=")", bg="#E6F7FF").grid(row=fila, column=12)

        entradas[-1].bind("<Return>", lambda event, idx=idx: transformar_transicion_a_texto(idx))

        lineas_transiciones[idx] = entradas
        transiciones_texto[idx] = None

def agregar_palabra():
    index = len(palabras_entries)
    entry = tk.Entry(frame_palabras, width=20)
    entry.grid(row=index, column=0, pady=2, sticky="w")
    entry.bind("<Return>", lambda event, idx=index: transformar_palabra_a_texto(idx))
    palabras_entries.append(entry)
    palabras_texto.append(None)

def transformar_palabra_a_texto(index):
    texto = palabras_entries[index].get()
    if not texto:
        return

    palabras_entries[index].grid_remove()
    label = tk.Label(frame_palabras, text=f"{index+1}. {texto}", bg="#FDEDEC", anchor="w")
    label.grid(row=index, column=0, sticky="w")
    palabras_texto[index] = (label,)

# === Interfaz ===
root = tk.Tk()
root.title("Simulador de Autómata Pushdown Determinista (APD)")

tk.Label(root, text="Simulador de Autómata Pushdown Determinista (APD)", font=("Arial", 16, "bold")).pack(pady=10)

frame_contenedor = tk.Frame(root)
frame_contenedor.pack(padx=10, pady=5, fill="x")
frame_contenedor.columnconfigure((0, 1, 2), weight=1, uniform="col")

# Transiciones
frame_transiciones = tk.LabelFrame(frame_contenedor, text="Transiciones del APD", bg="#E6F7FF")
frame_transiciones.grid(row=0, column=0, padx=(0,10), sticky="nsew")

tk.Label(frame_transiciones, text="δ ( q, símbolo, tope_pila ) : ( q', pila')", bg="#E6F7FF").grid(row=0, column=0, columnspan=13)

agregar_transicion()
agregar_transicion()

btn_frame_trans = tk.Frame(frame_transiciones, bg="#E6F7FF")
btn_frame_trans.grid(row=100, column=0, columnspan=13, pady=5)
tk.Button(btn_frame_trans, text="Agregar transición", command=agregar_transicion).pack(side="left", padx=5)
tk.Button(btn_frame_trans, text="Editar transiciones", command=editar_todas_las_transiciones).pack(side="left", padx=5)

# Estados
frame_estados = tk.LabelFrame(frame_contenedor, text="Estados", bg="#F9F7E8")
frame_estados.grid(row=0, column=1, padx=10, sticky="nsew")

tk.Label(frame_estados, text="Estado inicial:", bg="#F9F7E8").grid(row=0, column=0, sticky="w")
estado_inicial_entry = tk.Entry(frame_estados, width=15)
estado_inicial_entry.grid(row=0, column=1, pady=2)

tk.Label(frame_estados, text="Aceptación por:", bg="#F9F7E8").grid(row=1, column=0, sticky="w", pady=(10,0))
aceptacion_var = tk.StringVar(value="estado_final")
tk.Radiobutton(frame_estados, text="Estado final", variable=aceptacion_var, value="estado_final", bg="#F9F7E8").grid(row=2, column=0, columnspan=2, sticky="w")
tk.Radiobutton(frame_estados, text="Stack vacío", variable=aceptacion_var, value="stack_vacio", bg="#F9F7E8").grid(row=3, column=0, columnspan=2, sticky="w")

tk.Label(frame_estados, text="Estado final:", bg="#F9F7E8").grid(row=4, column=0, sticky="w", pady=(10,0))
estado_final_entry = tk.Entry(frame_estados, width=15)
estado_final_entry.grid(row=4, column=1, pady=2)

# Palabras
frame_palabras = tk.LabelFrame(frame_contenedor, text="Palabras de entrada", bg="#FDEDEC")
frame_palabras.grid(row=0, column=2, padx=(10,0), sticky="nsew")

agregar_palabra()
agregar_palabra()

tk.Button(frame_palabras, text="Agregar palabra", command=agregar_palabra).grid(row=100, column=0, columnspan=2, pady=5)

# Botones inferiores
frame_botones = tk.Frame(root)
frame_botones.pack(pady=15)

tk.Button(frame_botones, text="Simular", width=12).grid(row=0, column=0, padx=10)
tk.Button(frame_botones, text="Limpiar", width=12).grid(row=0, column=1, padx=10)
tk.Button(frame_botones, text="Salir", width=12, command=root.destroy).grid(row=0, column=2, padx=10)

root.mainloop()