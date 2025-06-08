from funciones_interfaz import transiciones, palabras_entrada

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
    
    for palabra in palabras_entrada:
        resultado = simularAPD(transiciones, estado_inicial, estado_final, palabra, aceptacion_var.get())
    

def simularAPD(transiciones: dict, estado_inicial: str, estado_final: str, palabra: list, modo_aceptacion: str):
    stack = ["R"]
    estado_actual = estado_inicial

    for simbolo in palabra:
        tope_pila = stack[-1] if stack else None
        clave = (estado_actual, simbolo, tope_pila)

        if clave not in transiciones:
            return False  # No hay transición válida

        nuevo_estado, accion_pila = transiciones[clave]
        estado_actual = nuevo_estado

        if stack:
            stack.pop()

        for simbolo_pila in reversed(accion_pila):
            if simbolo_pila != "E" and simbolo_pila != "":
                stack.append(simbolo_pila)

    # Manejo de transiciones ε post-palabra
    max_epsilon = 10
    epsilon_aplicadas = 0

    while epsilon_aplicadas < max_epsilon:
        tope_pila = stack[-1] if stack else None
        clave_epsilon = (estado_actual, "E", tope_pila)

        if clave_epsilon not in transiciones:
            break

        nuevo_estado, accion_pila = transiciones[clave_epsilon]
        estado_actual = nuevo_estado

        if stack:
            stack.pop()

        for simbolo_pila in reversed(accion_pila):
            if simbolo_pila != "E" and simbolo_pila != "":
                stack.append(simbolo_pila)

        epsilon_aplicadas += 1

    # Verificación de aceptación
    if modo_aceptacion == "estado_final":
        return estado_actual == estado_final
    elif modo_aceptacion == "stack_vacio":
        return len(stack) == 0
    return False
    

def main():
    # Definir el APD
    estado_inicial = "q0"
    estado_final = "qf"
    
    transiciones = {
        ("q0", "a", "R"): ("q0", ["A", "R"]),    # Primera 'a'
        ("q0", "a", "A"): ("q0", ["A", "A"]),    # Más 'a's
        ("q0", "b", "A"): ("q1", ["E"]),          # Primera 'b'
        ("q1", "b", "A"): ("q1", ["E"]),          # Más 'b's
        ("q1", "E", "R"): ("qf", ["R"])            # Aceptar si solo queda R
    }
    
    # Palabras de prueba
    palabras_prueba = [
        ["a", "b"],           # ✅ Debería aceptar
        ["a", "a", "b", "b"], # ✅ Debería aceptar  
        ["a", "a", "b"],      # ❌ Debería rechazar
        ["a", "b", "b"],      # ❌ Debería rechazar
        ["b", "a", "b"],           # ❌ Debería rechazar
    ]
    
    # Probar cada palabra
    for i, palabra in enumerate(palabras_prueba):
        print(f"\n📝 PRUEBA {i+1}: {''.join(palabra)}")
        print("-" * 40)
        resultado = simularAPD(transiciones, estado_inicial, estado_final, palabra, "estado_final")
        print(f"🏁 Resultado: {'ACEPTADA' if resultado else 'RECHAZADA'}")
        print("=" * 60)


if __name__ == "__main__":
    main()
