from funciones_interfaz import transiciones, palabras_entrada, mostrar_resultados_palabras

def verificarDatos(estado_inicial_entry, estado_final_entry, aceptacion_var):
    # Obtener estado inicial
    estado_inicial = estado_inicial_entry.get().strip()
    
    # Obtener estado final solo si la aceptación es por estado final
    if aceptacion_var.get() == "estado_final":
        estado_final = estado_final_entry.get().strip()
    else:
        estado_final = None
    
    # Validaciones (falta implementar ventanas emergentes de tkinter)
    # y ponerles try exception
    if not estado_inicial:
        print("Error: Debe especificar el estado inicial")
        return
    
    if not transiciones:
        print("Error: Debe especificar al menos una transición")
        return
    
    if not palabras_entrada:
        print("Error: Debe especificar al menos una palabra de entrada")
        return
    
    if aceptacion_var.get() == "estado_final" and not estado_final:
        print("Error: Debe especificar el estado final cuando la aceptación es por estado final")
        return
    
    resultados = []
    
    for palabra in palabras_entrada:
        resultado = simularAPD(transiciones, estado_inicial, estado_final, palabra, aceptacion_var.get())
        resultados.append(resultado)
    
    mostrar_resultados_palabras(resultados)

def simularAPD(transiciones: dict, estado_inicial: str, estado_final: str, palabra: list, modo_aceptacion: str):
    stack = ["R"]
    estado_actual = estado_inicial
    
    palabra_con_epsilon = palabra + ["E"]

    for simbolo in palabra_con_epsilon:
        if stack:
            tope_pila = stack[-1]
        else:
            tope_pila = None
        clave = (estado_actual, simbolo, tope_pila)

        if clave not in transiciones:
            # Si es epsilon y no hay transición, continuamos (no es error)
            if simbolo == "E":
                break
            return False  # No hay transición válida para símbolo normal

        nuevo_estado, accion_pila = transiciones[clave]
        estado_actual = nuevo_estado

        if stack:
            stack.pop()

        for simbolo_pila in reversed(accion_pila):
            if simbolo_pila != "E" and simbolo_pila != "":
                stack.append(simbolo_pila)

    # Verificación de aceptación
    if modo_aceptacion == "estado_final":
        return estado_actual == estado_final
    elif modo_aceptacion == "stack_vacio":
        return len(stack) == 0
    return False
