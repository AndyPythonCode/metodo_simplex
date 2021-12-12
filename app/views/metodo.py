from typing import List


class MetodoSimplex:
    def __init__(self, matriz, restricciones, objetivos) -> None:
        self.matriz: List[List] = matriz
        self.restricciones: int = restricciones
        self.objetivos: int = objetivos
        self.ultima_tabla: List[List] = [[]]
        self.funcion_objetivo: List = []
        self.solucion_no_acotada: str = ""
        self.index_fila_pivote: int = 0
        self.index_columna_pivote: int = 0
        self.lista_index_pivote: List = []
        self.elemento_pivote: int = 0
        self.nueva_tabla: List = []
        self.respuesta: str = ""
        self.columna_entrada = ["Z"] + [f"{index+1}X" for index in range(self.objetivos)] + [f"{index+1}S" for index in range(self.restricciones)]

    # La posicion de la fila a convertir en 1
    def fila_pivote(self) -> None:
        length = len(self.funcion_objetivo) - 1
        fila_solucion = []
        columna_solucion = []

        # Buscar la columna 'Sol' y 'Columna Pivote' para dividirla
        for fila in self.ultima_tabla:
            for index, columna in enumerate(fila):
                if index == self.index_columna_pivote:
                    # 'Columna Pivote'
                    fila_solucion.append(columna)
                if length == index:
                    # 'Columna Sol'
                    columna_solucion.append(columna)

        columna_solucion.pop(0)  # Funcion objetivo no se incluye
        fila_solucion.pop(0)  # Funcion objetivo no se incluye

        # Si son todos negativos en 'Columna Pivote' no tiene solucion optima
        if all([True if numero <= 0 else False for numero in fila_solucion]):
            self.solucion_no_acotada = f"El problema tiene solución ilimitada (no acotada), es decir, {self.columna_entrada[self.index_columna_pivote]} debe de entrar pero ninguna puede salir."  
        else:
            # Dividir 'Columna Pivote' / 'Columna Sol'
            fila_solucion = list(map(lambda x, y: x / y if y > 0 and x > 0 else "No se puede", columna_solucion, fila_solucion))
            try:
                self.index_fila_pivote = fila_solucion.index(min(e for e in fila_solucion if isinstance(e, int) or isinstance(e, float))) + 1
            except:
                self.solucion_no_acotada = "No se puede seleccionar una fila pivote para determinar la variable que debe dejar la base."

    # Dividir 'Fila pivote' / 'Elemento pivote' para convertir el 1 'Elemento pivote'
    def elemento_pivote_en_uno(self) -> float:
        salida = []
        for numero in self.ultima_tabla[self.index_fila_pivote]:
            salida.append(round(numero/self.elemento_pivote, 3))
        return salida
    
    # Formula
    def fila_nueva(self):
        convertir_cero = []
        
        # Buscar los numeros por encima o debajo de 'Elemento pivote'
        for fila in self.nueva_tabla:
            for index, variable in enumerate(fila):
                if index == self.index_columna_pivote:
                    convertir_cero.append(variable)
        
        # Aplicar formula a todas las filas que no sea 'Fila pivote'
        for index, fila in enumerate(self.nueva_tabla):
            if index != self.index_fila_pivote:
                # Numero encima o debajo del uno * -1 * Fila pivote + Fila a la que corresponde
                # Ejemplo: 5f2 + f1
                self.nueva_tabla[index] = list(map(lambda x, y: round((convertir_cero[index]*-1) * x + y, 3), 
                    self.nueva_tabla[self.index_fila_pivote], self.nueva_tabla[index]))
        self.matriz.append(self.nueva_tabla)
    
    # Imprimir resultado
    def salida_de_variables(self):
        length = len(self.ultima_tabla[0]) # Cantidad de columnas

        columnas = [[] for _ in range(length)] # Creamos cada columna

        # Llenamos cada columna
        for fila in self.ultima_tabla:
            for dimension in range(length):
                columnas[dimension].append(fila[dimension])

        variables_de_salida = []
        for index, variables_de_entrada in enumerate(columnas):
            if variables_de_entrada.count(0) == self.restricciones:
                # Columna y valor a la variable de salida
                try:
                    variables_de_salida.append((index, columnas[index].index(1)))
                except ValueError:
                    # Aveces contiene otro valores que no son "1" y saca una excepcion
                    ... 

        for letra, lugar in variables_de_salida:
            self.respuesta += f" [{self.columna_entrada[letra]} = {columnas[-1][lugar]}]  "