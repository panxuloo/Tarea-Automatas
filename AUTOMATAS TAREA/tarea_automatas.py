import tkinter as tk
from funciones_interfaz import *
from logica import *

def crear_frame_scrollable_contenedor(parent, titulo, bg_color):
    contenedor = tk.LabelFrame(parent, text=titulo, font=("Arial", 12, "bold"), bg=bg_color)
    
    # Crear canvas con tamaño mínimo
    canvas = tk.Canvas(contenedor, bg=bg_color, highlightthickness=0, width=200, height=300)
    scrollbar = tk.Scrollbar(contenedor, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=bg_color)

    # Configurar el sistema de scroll
    def configurar_scroll(event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))
        # Forzar actualización del scrollbar
        canvas.update_idletasks()
    
    scrollable_frame.bind("<Configure>", configurar_scroll)

    # Crear ventana en el canvas
    canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Ajustar el ancho del frame scrollable al canvas
    def ajustar_ancho(event=None):
        canvas_width = canvas.winfo_width()
        canvas.itemconfig(canvas_window, width=canvas_width)
    
    canvas.bind('<Configure>', ajustar_ancho)

    # Empacar elementos
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    return contenedor, scrollable_frame, canvas

def bind_mousewheel(widget, canvas):
    def _on_mousewheel(event):
        # Verificar los límites antes de desplazar
        canvas.update_idletasks()
        bbox = canvas.bbox("all")
        
        if bbox is None:
            return
            
        # Obtener la vista actual
        try:
            y0, y1 = canvas.yview()
            canvas_height = canvas.winfo_height()
            content_height = bbox[3] - bbox[1] if bbox else 0
            
            # Solo desplazar si hay contenido que se pueda desplazar
            if content_height > canvas_height:
                delta = int(-1 * (event.delta / 120)) if hasattr(event, 'delta') else -1 if event.num == 4 else 1
                canvas.yview_scroll(delta, "units")
        except:
            # En caso de error, intentar scroll básico
            canvas.yview_scroll(int(-1 * (event.delta / 120)) if hasattr(event, 'delta') else 0, "units")
    
    # Vincular a todos los widgets hijos
    def bind_recursive(w):
        try:
            w.bind("<MouseWheel>", _on_mousewheel)
            # También bind para Linux
            w.bind("<Button-4>", _on_mousewheel)
            w.bind("<Button-5>", _on_mousewheel)
            for child in w.winfo_children():
                bind_recursive(child)
        except:
            pass
    
    bind_recursive(widget)

def actualizar_scroll_region(canvas):
    def actualizar():
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
    
    # Programar la actualización para después de que se procesen otros eventos
    canvas.after_idle(actualizar)

def limpiar_todo():
    global lineas_transiciones, transiciones_data, transiciones_texto
    global palabras_entries, palabras_texto, palabras_resultados
    global transiciones, palabras_entrada
    
    lineas_transiciones.clear()
    transiciones_data.clear()
    transiciones_texto.clear()
    palabras_entries.clear()
    palabras_texto.clear()
    palabras_resultados.clear()
    transiciones.clear()
    palabras_entrada.clear()
    
    estado_inicial_entry.delete(0, tk.END)
    estado_final_entry.delete(0, tk.END)
    
    for widget in frame_transiciones.winfo_children():
        if isinstance(widget, tk.Frame) and widget.winfo_name() != "btn_frame_trans":
            continue
        elif not isinstance(widget, tk.Frame):
            widget.destroy()
    
    for widget in frame_palabras.winfo_children():
        if not isinstance(widget, tk.Button):
            widget.destroy()
    
    tk.Label(frame_transiciones, text="δ ( q, símbolo, tope_pila ) = ( q', pila')", bg="#E6F7FF").grid(row=0, column=0, columnspan=13, pady=(5,0))
    agregar_transicion(frame_transiciones)
    agregar_transicion(frame_transiciones)
    
    agregar_palabra(frame_palabras)
    agregar_palabra(frame_palabras)
    
    actualizar_alfabeto()
    
    # Actualizar region de scroll después de limpiar
    actualizar_scroll_region(canvas_trans)
    actualizar_scroll_region(canvas_palabras)

# === Pantalla ===
root = tk.Tk()
root.title("Simulador de Autómata Pushdown Determinista (APD)")
root.geometry("1300x500")
root.resizable(False, False)

tk.Label(root, text="Simulador de Autómata Pushdown Determinista (APD)", 
         font=("Arial", 16, "bold")).pack(pady=10)

frame_superior = tk.Frame(root)
frame_superior.pack(fill="x", padx=10, pady=(0, 5))

frame_contenedor = tk.Frame(root)
frame_contenedor.pack(padx=10, pady=5, fill="x")
frame_contenedor.columnconfigure(0, weight=2, uniform="col")  # Transiciones
frame_contenedor.columnconfigure(1, weight=1, uniform="col")  # Estados (ahora más chico)
frame_contenedor.columnconfigure(2, weight=1, uniform="col")  # Palabras (ahora más chico)
frame_contenedor.columnconfigure(3, weight=1, uniform="col")

# Alfabeto Σ
frame_alfabeto = tk.Frame(frame_superior, bg="white")
frame_alfabeto.pack(side="left", anchor="w")
label_alfabeto_global = crear_label_alfabeto(frame_alfabeto)
label_alfabeto_global.pack()

# === Transiciones con scrollbar ===
frame_transiciones_container, frame_transiciones, canvas_trans = crear_frame_scrollable_contenedor(
    frame_contenedor, "Transiciones del APD", "#E6F7FF"
)
frame_transiciones_container.grid(row=0, column=0, padx=(0,10), sticky="nsew")

tk.Label(frame_transiciones, text="δ ( q, símbolo, tope de la pila ) = ( q', pila')", bg="#E6F7FF").grid(row=0, column=0, columnspan=13, pady=(5,0))
agregar_transicion(frame_transiciones)
agregar_transicion(frame_transiciones)

btn_frame_trans = tk.Frame(frame_transiciones, bg="#E6F7FF", name="btn_frame_trans")
btn_frame_trans.grid(row=100, column=0, columnspan=13, pady=5)
tk.Button(btn_frame_trans, text="Agregar transición", 
          command=lambda: [agregar_transicion(frame_transiciones), 
                           actualizar_scroll_region(canvas_trans)]).pack(side="left", padx=5)
tk.Button(btn_frame_trans, text="Editar transiciones", 
          command=lambda: editar_todas_las_transiciones(frame_transiciones)).pack(side="left", padx=5)

# === Estados ===
frame_estados = tk.LabelFrame(frame_contenedor, text="Estados", 
                             font=("Arial", 12, "bold"), bg="#F9F7E8")
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

# === Palabras con scrollbar ===
frame_palabras_container, frame_palabras, canvas_palabras = crear_frame_scrollable_contenedor(
    frame_contenedor, "Palabras de entrada", "#FDEDEC"
)
frame_palabras_container.grid(row=0, column=2, padx=(10,0), sticky="nsew")

agregar_palabra(frame_palabras)
agregar_palabra(frame_palabras)

# Botones para palabras
btn_frame_palabras = tk.Frame(frame_palabras, bg="#FDEDEC")
btn_frame_palabras.grid(row=100, column=0, columnspan=5, pady=5, sticky="ew")

tk.Button(btn_frame_palabras, text="Agregar palabra", 
          command=lambda: [agregar_palabra(frame_palabras),
                           actualizar_scroll_region(canvas_palabras)]).pack(side="left", padx=5)
tk.Button(btn_frame_palabras, text="Editar palabras", 
          command=lambda: editar_todas_las_palabras(frame_palabras)).pack(side="left", padx=5)

# === Condiciones de uso ===
frame_condiciones = tk.LabelFrame(
    frame_contenedor,
    text="Condiciones de uso",
    font=("Arial", 12, "bold"),
    bg="#F0F4F8"       # color suave, armónico con los demás
)
frame_condiciones.grid(row=0, column=3, padx=(10,0), sticky="nsew")

# Dentro del frame, un texto explicativo:
texto_condiciones = (
    "El simbolo Epsilon está representado por una E."
)
tk.Label(
    frame_condiciones,
    text=texto_condiciones,
    wraplength=200,    # para que el texto se ajuste bien al ancho
    justify="left",
    bg="#F0F4F8"
).pack(padx=10, pady=10)

# === Botones inferiores ===
frame_botones = tk.Frame(root)
frame_botones.pack(pady=15)

tk.Button(frame_botones, text="Simular", width=12, 
          command=lambda: verificarDatos(frame_transiciones, frame_palabras, estado_inicial_entry, estado_final_entry, aceptacion_var)).grid(row=0, column=0, padx=10)
tk.Button(frame_botones, text="Limpiar", width=12, command=limpiar_todo).grid(row=0, column=1, padx=10)
tk.Button(frame_botones, text="Salir", width=12, command=root.destroy).grid(row=0, column=2, padx=10)

# Vincular eventos de scroll después de crear todos los elementos
bind_mousewheel(frame_transiciones_container, canvas_trans)
bind_mousewheel(frame_palabras_container, canvas_palabras)

# Actualizar scrollbars inicialmente
root.after(100, lambda: [actualizar_scroll_region(canvas_trans), actualizar_scroll_region(canvas_palabras)])

root.mainloop()