import tkinter as tk

# === Datos ===
lineas_transiciones = []
transiciones_data = []
transiciones_texto = []

palabras_entries = []
palabras_texto = []
palabras_resultados = []

transiciones = {}
palabras_entrada = []

# === Funciones ===
def agregar_transicion(frame_transiciones):
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

    entradas[-1].bind("<Return>", lambda event, idx=index: transformar_transicion_a_texto(idx, frame_transiciones))

    lineas_transiciones.append(entradas)
    transiciones_data.append([""] * 5)
    transiciones_texto.append(None)

def transformar_transicion_a_texto(index, frame_transiciones):
    fila = index + 1
    datos = [e.get() for e in lineas_transiciones[index]]
    if not all(datos):
        return

    transiciones[(datos[0], datos[1], datos[2])] = (datos[3], datos[4])

    transiciones_data[index] = datos

    for widget in frame_transiciones.grid_slaves(row=fila):
        widget.destroy()

    texto = f"{index+1}. δ({datos[0]}, {datos[1]}, {datos[2]}) : ({datos[3]}, {datos[4]})"
    label = tk.Label(frame_transiciones, text=texto, bg="#E6F7FF", anchor="w")
    label.grid(row=fila, column=0, columnspan=13, sticky="w")

    transiciones_texto[index] = (label,)

def editar_todas_las_transiciones(frame_transiciones):
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

        entradas[-1].bind("<Return>", lambda event, idx=idx: transformar_transicion_a_texto(idx, frame_transiciones))

        lineas_transiciones[idx] = entradas
        transiciones_texto[idx] = None

def agregar_palabra(frame_palabras):
    index = len(palabras_entries)
    entry = tk.Entry(frame_palabras, width=20)
    entry.grid(row=index, column=0, pady=2, sticky="w")
    entry.bind("<Return>", lambda event, idx=index: transformar_palabra_a_texto(idx, frame_palabras))
    palabras_entries.append(entry)
    palabras_texto.append(None)
    palabras_resultados.append(None)

def transformar_palabra_a_texto(index, frame_palabras):
    texto = palabras_entries[index].get()
    if not texto:
        return

    palabras_entrada.append(list(texto))

    palabras_entries[index].grid_remove()
    label = tk.Label(frame_palabras, text=f"{index+1}. {texto}", bg="#FDEDEC", anchor="w")
    label.grid(row=index, column=0, sticky="w")
    palabras_texto[index] = (label,)
    
def mostrar_resultados_palabras(resultados): # funcion dada por chat para los resultados
    for index, resultado in enumerate(resultados):
        # Si ya hay un resultado previo, eliminarlo
        if palabras_resultados[index] is not None:
            palabras_resultados[index].destroy()
        
        # Solo mostrar resultado si la palabra ya está convertida a texto
        if palabras_texto[index] is not None:
            simbolo = "✓" if resultado else "✗"
            color = "green" if resultado else "red"
            
            resultado_label = tk.Label(
                palabras_texto[index][0].master,  # Usar el mismo frame padre
                text=simbolo,
                fg=color,
                bg="#FDEDEC",
                font=("Arial", 12, "bold")
            )
            resultado_label.grid(row=index, column=1, sticky="w", padx=(5, 0))
            palabras_resultados[index] = resultado_label

def limpiar_resultados_palabras(): # funcion dada por chat para limpiar
    for index in range(len(palabras_resultados)):
        if palabras_resultados[index] is not None:
            palabras_resultados[index].destroy()
            palabras_resultados[index] = None

def actualizar_estado_final_entry(aceptacion_var, estado_final_entry):
    if aceptacion_var.get() == "estado_final":
        estado_final_entry.config(state="normal")
    else:
        estado_final_entry.delete(0, "end")
        estado_final_entry.config(state="disabled")