# Imprimir resultado
def salida_de_variables(tabla, objetivo, restriccion):
    length = len(tabla[0])
    columna_entrada = ["Z"]
    columna_entrada += [f"{index+1}X" for index in range(objetivo)]
    columna_entrada += [f"{index+1}S" for index in range(restriccion)]
    respuesta = ""

    columnas = [[] for _ in range(length)]
    for fila in tabla:
        for dimension in range(length):
            columnas[dimension].append(fila[dimension])

    variables_de_salida = []
    for index, variables_de_entrada in enumerate(columnas):
        if variables_de_entrada.count(0) == restriccion:
            variables_de_salida.append((index, columnas[index].index(1)))

    for letra, lugar in variables_de_salida:
        respuesta += f" [{columna_entrada[letra]} = {columnas[-1][lugar]}]  "
    return f"{respuesta}"