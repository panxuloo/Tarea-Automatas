def simularAPDFake():
    print("Simulador de APD (versión fake)")
    return

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

    print(stack)

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

def main():
    print("Simulador de APD")
    T1 = {
        "δ(q0,a,R)": "(q1,AR)",
        "δ(q1,b,A)": "(q2,AA)",
        "δ(q2,c,A)": "(q3,E)",
        "δ(q3,d,A)": "(q4,E)",
        "δ(q4,e,R)": "(q5,R)"
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
    F1 = "q5"
    F2 = "q2"
    palabra1 = "abcde"
    palabra = "aaaaaabbbE"

    simularAPD(T1, Q, F1, palabra1, "estado_final")

    simularAPD(T2, Q, F2, palabra, "stack_vacio")


if __name__ == "__main__":
    main()
