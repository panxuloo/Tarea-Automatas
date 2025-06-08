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
    

def simularAPD(T:dict, Q:str, F:str, palabra:str, aceptada:str):
    stack = ["R"]
    q = Q  # Estado inicial
    for letra in palabra:
        try:
            estado = f"δ({q},{letra},{stack.pop()})"    # δ(q0,a,R), con el pop() ya saco el elemento del tope de la pila, 
                                                        # si resultado es "E" no lo vuelvo a agregar
            resultado = T[estado]                       # (q1,AR)

            print(f"Transición: {estado}, resultado: {resultado}, pila actual: {stack}")

            q = resultado[1:3]                          # Actualizo estado actual 
            tope = resultado[4:-1]                      # Tomo lo que agregare a la pila  

            for a in tope[::-1]:
                if a != "E":
                    stack.append(a)                     # Agrego a la pila (si no es vacía)

        except:
            print("Palabra no aceptada")
            print(f"Error en la transición para {letra} con estado {q} y pila {stack}")
            break


    if aceptada == "estado_final":
        if q == F :
            print("ACEPTADA - Estado final alcanzado")
        else:
            print("RECHAZADA - Estado final no alcanzado")

    elif aceptada == "stack_vacio":
        if len(stack) == 0:
            print("ACEPTADA - Pila vacía")
        else:
            print("RECHAZADA - Pila no vacía")
    
    return

# función de chat
def simular_palabra(palabra, estado_inicial, estado_final, tipo_aceptacion):
    """
    Simula el procesamiento de una palabra por el APD
    """
    estado_actual = estado_inicial
    pila = ['$']  # Símbolo inicial de la pila
    posicion = 0
    
    print(f"Estado inicial: {estado_actual}, Pila: {pila}")
    
    while posicion < len(palabra):
        simbolo = palabra[posicion]
        tope_pila = pila[-1] if pila else None
        
        # Buscar transición aplicable
        clave_transicion = (estado_actual, simbolo, tope_pila)
        
        if clave_transicion in transiciones:
            nuevo_estado, accion_pila = transiciones[clave_transicion]
            
            # Aplicar transición
            estado_actual = nuevo_estado
            
            # Actualizar pila
            if tope_pila:
                pila.pop()  # Quitar el tope
            
            # Agregar nuevos símbolos a la pila (si no es epsilon)
            if accion_pila and accion_pila != 'ε' and accion_pila != '':
                # Si hay múltiples símbolos, agregarlos en orden inverso
                for simbolo_pila in reversed(accion_pila):
                    pila.append(simbolo_pila)
            
            print(f"Transición: ({estado_actual}, {simbolo}, {tope_pila}) -> ({nuevo_estado}, {accion_pila})")
            print(f"Estado: {estado_actual}, Pila: {pila}")
            
            posicion += 1
        else:
            print(f"No hay transición para ({estado_actual}, {simbolo}, {tope_pila})")
            return False
    
    # Verificar aceptación
    if tipo_aceptacion == "estado_final":
        return estado_actual == estado_final
    else:  # stack_vacio
        return len(pila) == 0 or (len(pila) == 1 and pila[0] == '$')
    
    
#simularAPD(transiciones, estado_inicial, estado_final, palabra, aceptacion_var.get())
def funcionSimularAPD(transiciones: dict, estado_inicial: str, estado_final: str, palabra: list, aceptacion_var: str):
    stack = ["R"]  # Pila inicial
    estado_actual = estado_inicial
    
    
    return

def main():
    print("Simulador de APD")
    T1 = {
        "δ(q0,a,R)": "(q0,AR)",
        "δ(q0,a,A)": "(q0,AA)",
        "δ(q0,b,A)": "(q1,BA)",
        "δ(q1,b,B)": "(q1,BB)",
        "δ(q1,c,B)": "(q2,E)",
        "δ(q2,c,B)": "(q2,E)",
        "δ(q2,c,A)": "(q2,E)",
        "δ(q2,E,R)": "(q3,E)"
    }
    T2 = {
        "δ(q0,a,R)": "(q0,ABR)",
        "δ(q0,a,A)": "(q0,E)",
        "δ(q0,a,B)": "(q0,ABB)",
        "δ(q0,b,B)": "(q1,E)",
        "δ(q1,b,B)": "(q1,E)",
        "δ(q1,E,R)": "(q2,E)"
    }
    Q = "q0"
    F1 = "q3"
    F2 = "q2"
    palabra1 = "aabbccccE"
    palabra = "aaaaaabbbE"

    simularAPD(T1, Q, F1, palabra1, "estado_final")

    simularAPD(T2, Q, F2, palabra, "stack_vacio")


if __name__ == "__main__":
    main()
