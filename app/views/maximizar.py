# Mis funciones
def metodo_simplex_maximizar(tablas):
    resultado_final = tablas.copy()
    mensaje = ""

    while True:
        ultima_tabla = resultado_final[-1]
        funcion_objetivo = ultima_tabla[0]

        # Si todas las filas son positiva se ha terminado el problema
        if all([True if numero >= 0 else False for numero in funcion_objetivo]):
            break

        index_columna, index_fila, no_acotada = fila_pivote(ultima_tabla, columna_pivote(funcion_objetivo))    

        # Si en la columna pivote son todos negativos
        if no_acotada:
            mensaje = no_acotada
            break

        elemento_pivote = ultima_tabla[index_fila][index_columna]
        nueva_tabla = ultima_tabla.copy()
        nueva_tabla[index_fila] = elemento_pivote_en_uno(ultima_tabla[index_fila], elemento_pivote)
        resultado_final.append(fila_nueva(nueva_tabla, index_columna, index_fila))

    return resultado_final, mensaje


# Formula
def fila_nueva(matriz, index_columna, index_fila):
    convertir_cero = []
    for fila in matriz:
        for index, variable in enumerate(fila):
            if index == index_columna:
                convertir_cero.append(variable)

    for index_fila_pivote, fila in enumerate(matriz):
        if index_fila_pivote != index_fila:
            matriz[index_fila_pivote] = list(map(lambda x, y: round((convertir_cero[index_fila_pivote]*-1) * x + y, 3), matriz[index_fila], matriz[index_fila_pivote]))
    return matriz


# La posicion de la columna a convertir en 1
def columna_pivote(funcion_objetivo):
    minimo = funcion_objetivo[0]
    posicion = 0
    for index, numero in enumerate(funcion_objetivo):
        if minimo > numero:
            minimo = numero
            posicion = index
    return posicion


# La posicion de la fila a convertir en 1
def fila_pivote(tabla, columna_pivote):
    length = len(tabla[0]) - 1
    fila_solucion = []
    columna_solucion = []
    solucion_acotada = ""

    for fila in tabla:
        for index, columna in enumerate(fila):
            if index == columna_pivote:
                fila_solucion.append(columna)
            if length == index:
                columna_solucion.append(columna)
    columna_solucion.pop(0) # Funcion objetivo no se incluye
    fila_solucion.pop(0) # Funcion objetivo no se incluye

    # Si son todos negativos no tiene solucion optima
    if all([True if numero < 0 else False for numero in fila_solucion]):
        solucion_acotada = "El problema tiene solución ilimitada (no acotada), es decir, una variable debe de entrar pero ninguna puede salir."
        return ..., ..., solucion_acotada

    fila_solucion = list(map(lambda x, y: x / y if y > 0 and x > 0 else "No se puede", columna_solucion, fila_solucion)) # Division fila pivote
    return columna_pivote, fila_solucion.index(min(e for e in fila_solucion if isinstance(e, int) or isinstance(e, float))) + 1, solucion_acotada


# Todo entre elemento pivote
def elemento_pivote_en_uno(tabla, elemento_pivote):
    salida = []
    for numero in tabla:
        salida.append(round(numero/elemento_pivote, 3))
    return salida