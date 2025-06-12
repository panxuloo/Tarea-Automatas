import tkinter as tk
from funciones_interfaz import *
from logica import *

def crear_frame_scrollable_contenedor(parent, titulo, bg_color):
    contenedor = tk.LabelFrame(parent, text=titulo, font=("Arial", 12, "bold"), bg=bg_color)
    
    canvas = tk.Canvas(contenedor, bg=bg_color, highlightthickness=0)
    scrollbar = tk.Scrollbar(contenedor, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=bg_color)

    # Configurar el sistema de scroll
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

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
            
        y0, y1 = canvas.yview()
        y_pos = y0 * bbox[3]
        
        # Solo desplazar si hay contenido más allá de los límites visibles
        if (event.delta < 0 and y_pos < bbox[3] - canvas.winfo_height()) or \
           (event.delta > 0 and y_pos > 0):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    # Vincular a todos los widgets hijos
    def bind_recursive(w):
        w.bind("<MouseWheel>", _on_mousewheel)
        for child in w.winfo_children():
            bind_recursive(child)
    
    bind_recursive(widget)

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
    canvas_trans.configure(scrollregion=canvas_trans.bbox("all"))
    canvas_palabras.configure(scrollregion=canvas_palabras.bbox("all"))

# === Pantalla ===
root = tk.Tk()
root.title("Simulador de Autómata Pushdown Determinista (APD)")

tk.Label(root, text="Simulador de Autómata Pushdown Determinista (APD)", 
         font=("Arial", 16, "bold")).pack(pady=10)

frame_superior = tk.Frame(root)
frame_superior.pack(fill="x", padx=10, pady=(0, 5))

frame_contenedor = tk.Frame(root)
frame_contenedor.pack(padx=10, pady=5, fill="x")
frame_contenedor.columnconfigure((0, 1, 2), weight=1, uniform="col")

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
canvas_trans.config(height=300)

tk.Label(frame_transiciones, text="δ ( q, símbolo, tope_pila ) = ( q', pila')", bg="#E6F7FF").grid(row=0, column=0, columnspan=13, pady=(5,0))
agregar_transicion(frame_transiciones)
agregar_transicion(frame_transiciones)

btn_frame_trans = tk.Frame(frame_transiciones, bg="#E6F7FF", name="btn_frame_trans")
btn_frame_trans.grid(row=100, column=0, columnspan=13, pady=5)
tk.Button(btn_frame_trans, text="Agregar transición", 
          command=lambda: [agregar_transicion(frame_transiciones), 
                           canvas_trans.configure(scrollregion=canvas_trans.bbox("all"))]).pack(side="left", padx=5)
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
canvas_palabras.config(height=300)

agregar_palabra(frame_palabras)
agregar_palabra(frame_palabras)

tk.Button(frame_palabras, text="Agregar palabra", 
          command=lambda: [agregar_palabra(frame_palabras),
                           canvas_palabras.configure(scrollregion=canvas_palabras.bbox("all"))]).grid(row=100, column=0, columnspan=2, pady=5)
tk.Button(frame_palabras, text="Editar palabras", 
          command=lambda: editar_todas_las_palabras(frame_palabras)).grid(row=100, column=3, columnspan=2, pady=5)

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

root.mainloop()