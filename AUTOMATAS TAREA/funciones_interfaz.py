import tkinter as tk
from tkinter import messagebox
from itertools import zip_longest

# === Datos ===
lineas_transiciones = []
transiciones_data = []
transiciones_texto = []

palabras_entries = []
palabras_texto = []
palabras_resultados = []

transiciones = {}
palabras_entrada = []

alfabeto_label = None

# === Funciones ===
def actualizar_alfabeto():
    global alfabeto_label
    simbolos = set()
    
    # Recolectar símbolos de transiciones completadas (modo texto)
    for idx, datos in enumerate(transiciones_data):
        if datos is not None and transiciones_texto[idx] is not None:
            simbolo = datos[1]  # El segundo elemento es el símbolo
            if simbolo and simbolo != "E":  # No incluir epsilon
                simbolos.add(simbolo)
    
    # Recolectar símbolos de transiciones en modo edición
    for idx, entradas in enumerate(lineas_transiciones):
        if entradas is not None and transiciones_texto[idx] is None:
            simbolo = entradas[1].get().strip()
            if simbolo and simbolo != "E":  # No incluir epsilon
                simbolos.add(simbolo)
    
    # Ordenar alfabéticamente
    alfabeto_ordenado = sorted(list(simbolos))
    
    # Actualizar el label del alfabeto
    if alfabeto_label:
        alfabeto_texto = f"Σ = {{{', '.join(alfabeto_ordenado)}}}"
        alfabeto_label.config(text=alfabeto_texto)

def crear_label_alfabeto(parent):
    global alfabeto_label
    alfabeto_label = tk.Label(parent, text="Σ = {}", font=("Arial", 10, "bold"), bg="#E6F7FF")
    return alfabeto_label

def agregar_transicion(frame_transiciones):
    # Encontrar el último índice no nulo
    ultimo_indice = -1
    for idx, entrada in enumerate(lineas_transiciones):
        if entrada is not None:
            ultimo_indice = idx
    
    # El nuevo índice será el siguiente al último no nulo
    index = ultimo_indice + 1
    fila = index + 1
    
    # Asegurarse de que las listas tienen suficiente espacio
    while len(lineas_transiciones) <= index:
        lineas_transiciones.append(None)
        transiciones_data.append(None)
        transiciones_texto.append(None)
    
    # Limpia cualquier widget existente en esta fila
    for widget in frame_transiciones.grid_slaves(row=fila):
        widget.destroy()
    
    # --- SOLUCIÓN: Elimina cualquier label de texto en esa fila antes de agregar widgets nuevos ---
    if transiciones_texto[index] is not None:
        label = transiciones_texto[index][0]
        label.destroy()
        transiciones_texto[index] = None
    entradas = []

    tk.Label(frame_transiciones, text=f"{index+1}. δ (", bg="#E6F7FF").grid(row=fila, column=0, sticky="e")

    for i in range(3):
        e = tk.Entry(frame_transiciones, width=6)
        e.grid(row=fila, column=1 + 2 * i)
        entradas.append(e)
        if i < 2:
            tk.Label(frame_transiciones, text=",", bg="#E6F7FF").grid(row=fila, column=2 + 2 * i)

    tk.Label(frame_transiciones, text=") = (", bg="#E6F7FF").grid(row=fila, column=7)

    for i in range(2):
        e = tk.Entry(frame_transiciones, width=6)
        e.grid(row=fila, column=8 + 2 * i)
        entradas.append(e)
        if i == 0:
            tk.Label(frame_transiciones, text=",", bg="#E6F7FF").grid(row=fila, column=9)

    # Agregar evento para actualizar alfabeto cuando se modifica el símbolo
    def on_simbolo_change(event):
        actualizar_alfabeto()

    entradas[1].bind("<KeyRelease>", on_simbolo_change)

    for i, entry in enumerate(entradas):
        def on_enter(event, idx=i):
            if idx + 1 < len(entradas):
                entradas[idx + 1].focus_set()
            actualizar_alfabeto()
        entry.bind("<Return>", on_enter)

    tk.Label(frame_transiciones, text=")", bg="#E6F7FF").grid(row=fila, column=12)

    #entradas[-1].bind("<Return>", lambda event, idx=index: transformar_transicion_a_texto(idx, frame_transiciones))
    entradas[-1].bind("<Return>", lambda event: event.widget.tk_focusNext().focus())

    
    # Botón para eliminar la fila, solo si no es la primera
    if index > 0:
        def eliminar_fila():
            for widget in frame_transiciones.grid_slaves(row=fila):
                widget.destroy()
            lineas_transiciones[index] = None
            transiciones_data[index] = None
            transiciones_texto[index] = None
            actualizar_indices_transiciones(frame_transiciones)
            actualizar_alfabeto()

        btn_eliminar = tk.Button(frame_transiciones, text="Eliminar", command=eliminar_fila, bg="#FFCCCC")
        btn_eliminar.grid(row=fila, column=13, padx=2)


    lineas_transiciones[index] = entradas
    transiciones_data[index] = [""] * 5
    transiciones_texto[index] = None

    actualizar_indices_transiciones(frame_transiciones)
    actualizar_alfabeto()

def actualizar_indices_transiciones(frame_transiciones):
    idx_visual = 1
    for idx, entradas in enumerate(lineas_transiciones):
        fila = idx + 1
        
        # Limpia TODOS los widgets antiguos en esta fila primero
        for widget in frame_transiciones.grid_slaves(row=fila):
            widget.grid_forget()
            
        if entradas is not None:
            # Modo editable: recrea los widgets
            nuevo_label = tk.Label(frame_transiciones, text=f"{idx_visual}. δ (", bg="#E6F7FF")
            nuevo_label.grid(row=fila, column=0, sticky="e")
            
            # Recrea los Entry y labels
            for i, entry in enumerate(entradas[:3]):
                entry.grid(row=fila, column=1 + 2 * i)
                if i < 2:
                    tk.Label(frame_transiciones, text=",", bg="#E6F7FF").grid(row=fila, column=2 + 2 * i)
            
            def on_simbolo_change(event):
                actualizar_alfabeto()
            entradas[1].bind("<KeyRelease>", on_simbolo_change)
            
            tk.Label(frame_transiciones, text=") = (", bg="#E6F7FF").grid(row=fila, column=7)
            
            for i, entry in enumerate(entradas[3:]):
                entry.grid(row=fila, column=8 + 2 * i)
                if i == 0:
                    tk.Label(frame_transiciones, text=",", bg="#E6F7FF").grid(row=fila, column=9)
                    
            tk.Label(frame_transiciones, text=")", bg="#E6F7FF").grid(row=fila, column=12)
            
            # Add delete button for non-first rows
            if idx > 0:
                def eliminar_fila(idx_local=idx):
                    for widget in frame_transiciones.grid_slaves(row=idx_local+1):
                        widget.destroy()
                    lineas_transiciones[idx_local] = None
                    transiciones_data[idx_local] = None
                    transiciones_texto[idx_local] = None
                    actualizar_indices_transiciones(frame_transiciones)
                    actualizar_alfabeto()
                
                btn_eliminar = tk.Button(frame_transiciones, text="Eliminar", 
                                       command=lambda idx=idx: eliminar_fila(idx), 
                                       bg="#FFCCCC")
                btn_eliminar.grid(row=fila, column=13, padx=2)
            
            idx_visual += 1
            
        elif transiciones_texto[idx] is not None:
            # Modo texto: solo muestra el label de texto
            label = transiciones_texto[idx][0]
            texto = label.cget("text")
            nuevo_texto = f"{idx_visual}" + texto[texto.find('.'):]
            label.config(text=nuevo_texto)
            label.grid(row=fila, column=0, columnspan=13, sticky="w")
            idx_visual += 1

def transformar_transicion_a_texto(index, frame_transiciones, idx_visual):
    fila = index + 1
    datos = [e.get() for e in lineas_transiciones[index]]
    if not all(datos):
        return

    transiciones[(datos[0], datos[1], datos[2])] = (datos[3], datos[4])
    transiciones_data[index] = datos

    # Eliminar solo los widgets de entrada, preservando el botón eliminar
    for widget in frame_transiciones.grid_slaves(row=fila):
        if not isinstance(widget, tk.Button):
            widget.grid_forget()

    texto = f"{idx_visual}. δ({datos[0]}, {datos[1]}, {datos[2]}) = ({datos[3]}, {datos[4]})"
    label = tk.Label(frame_transiciones, text=texto, bg="#E6F7FF", anchor="w")
    label.grid(row=fila, column=0, columnspan=12, sticky="w")
    transiciones_texto[index] = (label,)
    actualizar_alfabeto()
    # Ya no se agrega automáticamente una nueva fila al presionar Enter

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

        def on_simbolo_change(event):
            actualizar_alfabeto()
        entradas[1].bind("<KeyRelease>", on_simbolo_change)

        tk.Label(frame_transiciones, text=") : (", bg="#E6F7FF").grid(row=fila, column=7)

        for i in range(2):
            e = tk.Entry(frame_transiciones, width=6)
            e.insert(0, transiciones_data[idx][3 + i])
            e.grid(row=fila, column=8 + 2 * i)
            entradas.append(e)
            if i == 0:
                tk.Label(frame_transiciones, text=",", bg="#E6F7FF").grid(row=fila, column=9)

        tk.Label(frame_transiciones, text=")", bg="#E6F7FF").grid(row=fila, column=12)

        # Agregar botón eliminar si no es la primera transición
        if idx > 0:
            def eliminar_fila(idx_local=idx):
                for widget in frame_transiciones.grid_slaves(row=idx_local+1):
                    widget.destroy()
                lineas_transiciones[idx_local] = None
                transiciones_data[idx_local] = None
                transiciones_texto[idx_local] = None
                actualizar_indices_transiciones(frame_transiciones)
                actualizar_alfabeto()

            btn_eliminar = tk.Button(frame_transiciones, text="Eliminar",
                                   command=lambda idx=idx: eliminar_fila(idx),
                                   bg="#FFCCCC")
            btn_eliminar.grid(row=fila, column=13, padx=2)

        lineas_transiciones[idx] = entradas
        transiciones_texto[idx] = None
        
    actualizar_alfabeto()

def agregar_palabra(frame_palabras):
    # Encontrar el siguiente índice realmente disponible
    ultimo_indice = -1
    for idx in range(len(palabras_entries)):
        if palabras_entries[idx] is not None or palabras_texto[idx] is not None:
            ultimo_indice = idx
    
    # El nuevo índice será el siguiente al último usado
    index = ultimo_indice + 1
    
    # Expandir listas si es necesario
    while len(palabras_entries) <= index:
        palabras_entries.append(None)
        palabras_texto.append(None)
        palabras_resultados.append(None)
    
    # Limpiar cualquier widget existente en esta fila
    for widget in frame_palabras.grid_slaves(row=index):
        widget.destroy()
    
    # Crear widgets
    label = tk.Label(frame_palabras, text=f"{index+1}. ", bg="#FDEDEC")
    label.grid(row=index, column=0, sticky="e")
    
    entry = tk.Entry(frame_palabras, width=20)
    entry.grid(row=index, column=1, pady=2, sticky="w")
    entry.bind("<Return>", lambda event: event.widget.tk_focusNext().focus())
    entry.focus_set()  # Dar foco al nuevo entry

    # Agregar botón eliminar si no es la primera palabra
    if index > 0:
        btn_eliminar = tk.Button(
            frame_palabras, 
            text="Eliminar",
            command=lambda idx=index: eliminar_palabra(idx, frame_palabras),
            bg="#FFCCCC"
        )
        btn_eliminar.grid(row=index, column=3, padx=2)

    palabras_entries[index] = entry
    palabras_texto[index] = None
    palabras_resultados[index] = None
    actualizar_indices_palabras(frame_palabras)  # Añade esta línea

def transformar_palabra_a_texto(index, frame_palabras):
    if palabras_entries[index] is None:
        return

    texto = palabras_entries[index].get()
    if not texto:
        return

    # Limpiar widgets existentes excepto botón eliminar
    for widget in frame_palabras.grid_slaves(row=index):
        if not isinstance(widget, tk.Button):
            widget.destroy()

    # NO AGREGAR AQUÍ A palabras_entrada

    label = tk.Label(frame_palabras, text=f"{index+1}. {texto}", bg="#FDEDEC", anchor="w")
    label.grid(row=index, column=0, columnspan=2, sticky="w")
    palabras_texto[index] = (label,)
    palabras_entries[index] = None
    
    # Mantener el botón eliminar en su posición
    if index > 0:
        btn_eliminar = frame_palabras.grid_slaves(row=index, column=3)
        if btn_eliminar:
            btn_eliminar[0].lift()

def mostrar_resultados_palabras(resultados):
    limpiar_resultados_palabras()
    resultado_idx = 0
    for idx, texto_info in enumerate(palabras_texto):
        if texto_info is not None:
            if resultado_idx < len(resultados):
                simbolo = "✓" if resultados[resultado_idx] else "✗"
                color = "green" if resultados[resultado_idx] else "red"
                resultado_label = tk.Label(
                    texto_info[0].master,
                    text=simbolo,
                    fg=color,
                    bg="#FDEDEC",
                    font=("Arial", 12, "bold")
                )
                resultado_label.grid(row=idx, column=2, sticky="w", padx=(5, 0))
                palabras_resultados[idx] = resultado_label
                resultado_idx += 1
            else:
                # Si hay más palabras visuales que resultados, limpia el resultado
                palabras_resultados[idx] = None
        else:
            # Si no hay palabra en esta fila, limpia el resultado
            palabras_resultados[idx] = None

def limpiar_resultados_palabras(): # funcion dada por chat para limpiar
    for index in range(len(palabras_resultados)):
        if palabras_resultados[index] is not None:
            palabras_resultados[index].destroy()
            palabras_resultados[index] = None

def editar_todas_las_palabras(frame_palabras):
    for idx, texto_info in enumerate(palabras_texto):
        if texto_info is None:
            continue
            
        # Obtener el texto sin el índice
        texto_original = texto_info[0].cget("text")
        palabra = texto_original.split('.')[-1].strip()
        
        # Limpiar widgets existentes excepto botón eliminar
        for widget in frame_palabras.grid_slaves(row=idx):
            if not isinstance(widget, tk.Button):
                widget.destroy()
        
        # Crear label de índice
        tk.Label(frame_palabras, text=f"{idx+1}. ", bg="#FDEDEC").grid(row=idx, column=0, sticky="e")
        
        # Crear entry con el texto
        entry = tk.Entry(frame_palabras, width=20)
        entry.insert(0, palabra)
        entry.grid(row=idx, column=1, pady=2, sticky="w")
        
        # Recrear botón eliminar si no es la primera palabra
        if idx > 0:
            def eliminar_palabra(idx_local=idx):
                for widget in frame_palabras.grid_slaves(row=idx_local):
                    widget.destroy()
                palabras_entries[idx_local] = None
                palabras_texto[idx_local] = None
                if idx_local < len(palabras_entrada):
                    palabras_entrada.pop(idx_local)
                if idx_local < len(palabras_resultados):
                    if palabras_resultados[idx_local]:
                        palabras_resultados[idx_local].destroy()
                    palabras_resultados[idx_local] = None
                actualizar_indices_palabras(frame_palabras)
            
            btn_eliminar = tk.Button(frame_palabras, text="Eliminar", 
                                   command=lambda idx=idx: eliminar_palabra(idx, frame_palabras), 
                                   bg="#FFCCCC")
            btn_eliminar.grid(row=idx, column=3, padx=2)
        
        # Actualizar las listas de control
        palabras_entries[idx] = entry
        palabras_texto[idx] = None
        
        # Bind Enter para mover al siguiente campo
        entry.bind("<Return>", lambda event: event.widget.tk_focusNext().focus())
    actualizar_indices_palabras(frame_palabras)

def transformar(frame_transiciones, frame_palabras):
    # Limpiar palabras_entrada antes de recolectar las nuevas
    palabras_entrada.clear()
    
    # Verificar transiciones
    transiciones.clear()  # <-- Limpia el diccionario antes de reconstruirlo
    idx_visual = 1
    for idx, entradas in enumerate(lineas_transiciones):
        if entradas is not None:
            datos = [e.get() for e in entradas]
            if all(datos):
                transiciones[(datos[0], datos[1], datos[2])] = (datos[3], datos[4])
                transiciones_data[idx] = datos
                transformar_transicion_a_texto(idx, frame_transiciones, idx_visual)
                idx_visual += 1
    
    # Recolectar todas las palabras (solo en modo texto)
    palabras_encontradas = False
    
    # Primero transformar palabras en modo edición a texto (pero NO agregarlas a palabras_entrada)
    for idx, entry in enumerate(palabras_entries):
        if entry is not None:
            palabra = entry.get().strip()
            if palabra:  # Solo si no está vacía
                transformar_palabra_a_texto(idx, frame_palabras)
                palabras_encontradas = True
    
    # Luego procesar palabras que ya están en modo texto (estas sí van a palabras_entrada)
    for idx, texto_info in enumerate(palabras_texto):
        if texto_info is not None:
            label = texto_info[0]
            if not label.winfo_exists():
                continue
            texto_completo = label.cget("text")
            palabra = texto_completo.split('.', 1)[-1].strip()
            if palabra:
                palabras_entrada.append(list(palabra))
                palabras_encontradas = True
    
    if not palabras_encontradas:
        messagebox.showerror("Error", "ERROR: Debe especificar al menos una palabra de entrada")
        return False
    actualizar_indices_palabras(frame_palabras)
    actualizar_alfabeto()
    return True

def actualizar_estado_final_entry(aceptacion_var, estado_final_entry):
    if aceptacion_var.get() == "estado_final":
        estado_final_entry.config(state="normal")
    else:
        estado_final_entry.delete(0, "end")
        estado_final_entry.config(state="disabled")

def actualizar_indices_palabras(frame_palabras):
    idx_visual = 1
    idx_real = 0

    while idx_real < len(palabras_entries):
        if palabras_entries[idx_real] is not None or palabras_texto[idx_real] is not None:
            # Actualizar texto del label o entry según el modo
            if palabras_entries[idx_real] is not None:
                # Modo editable
                for widget in frame_palabras.grid_slaves(row=idx_real):
                    if isinstance(widget, tk.Label) and widget.cget("text").endswith(". "):
                        widget.config(text=f"{idx_visual}. ")
                # Elimina TODOS los botones previos en la fila antes de crear uno nuevo
                for widget in frame_palabras.grid_slaves(row=idx_real):
                    if isinstance(widget, tk.Button):
                        widget.destroy()
                # Recrear botón eliminar si no es la primera palabra
                if idx_real > 0:
                    btn_eliminar = tk.Button(
                        frame_palabras,
                        text="Eliminar",
                        command=lambda idx=idx_real: eliminar_palabra(idx, frame_palabras),
                        bg="#FFCCCC"
                    )
                    btn_eliminar.grid(row=idx_real, column=3, padx=2)
            elif palabras_texto[idx_real] is not None:
                # Modo texto
                label = palabras_texto[idx_real][0]
                if not label.winfo_exists():
                    palabras_texto[idx_real] = None
                    continue
                texto = label.cget("text")
                palabra = texto[texto.find(".")+1:].strip()
                label.config(text=f"{idx_visual}. {palabra}")
                # Elimina TODOS los botones previos en la fila antes de crear uno nuevo
                for widget in frame_palabras.grid_slaves(row=idx_real):
                    if isinstance(widget, tk.Button):
                        widget.destroy()
                # Recrear botón eliminar si no es la primera palabra
                if idx_real > 0:
                    btn_eliminar = tk.Button(
                        frame_palabras,
                        text="Eliminar",
                        command=lambda idx=idx_real: eliminar_palabra(idx, frame_palabras),
                        bg="#FFCCCC"
                    )
                    btn_eliminar.grid(row=idx_real, column=3, padx=2)
            idx_visual += 1
        idx_real += 1

def eliminar_palabra(idx, frame_palabras):
    # Elimina widgets de la fila idx (incluyendo todos los botones)
    for widget in frame_palabras.grid_slaves(row=idx):
        widget.destroy()
    # Borra de las estructuras de datos (solo pop en idx)
    if idx < len(palabras_entries):
        palabras_entries.pop(idx)
    if idx < len(palabras_texto):
        palabras_texto.pop(idx)
    if idx < len(palabras_resultados):
        if palabras_resultados[idx]:
            try:
                palabras_resultados[idx].destroy()
            except Exception:
                pass
        palabras_resultados.pop(idx)
    # Mueve widgets de filas inferiores una fila arriba
    max_filas = max(len(palabras_entries), len(palabras_texto))
    for i in range(idx + 1, max_filas + 1):
        for widget in frame_palabras.grid_slaves(row=i):
            widget.grid_configure(row=i-1)
    # Actualiza la interfaz y los botones
    actualizar_indices_palabras(frame_palabras)