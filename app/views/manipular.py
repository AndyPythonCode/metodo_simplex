from typing import List


class EntradaDinamica:
    def __init__(self, entrada_de_datos) -> None:
        self.entrada_de_datos: bytes = entrada_de_datos.decode("utf-8") # Decodificar el binario
        self.restriccion: int = 0
        self.objetivo: int = 0
        self.matriz: List = []
        self.operacion: str = ""
        self.init_matriz: List[List] = [[]]

    # Aca obtengo todos lo datos sin ningun caracter raro (limpiando)
    def str_to_dict(self):
        self.entrada_de_datos = self.entrada_de_datos.replace("=", "':'")
        self.entrada_de_datos = self.entrada_de_datos.replace("&", "','")
        self.entrada_de_datos = "{'" + self.entrada_de_datos
        self.entrada_de_datos = eval(self.entrada_de_datos + "'}")

    # Determinar la dimension de la matriz a trabajar (dinamico)
    def dimension_matriz(self) -> None:
        for i in self.entrada_de_datos:
            if i.startswith("objetivo"):
                self.objetivo += 1
            if i.startswith("ecuacion"):
                self.restriccion += 1

    # Guardar los datos entrado por el usuario en un arreglo
    def extraer_valor_dict(self) -> None:
        for elemento in self.entrada_de_datos:
            if elemento.startswith("objetivo"):
                # Multiplicar por (-1) la fila objetivo
                self.matriz.append(self.determinar_valor(self.entrada_de_datos[elemento]) * -1)
            if elemento.startswith("variable"):
                self.matriz.append(self.determinar_valor(self.entrada_de_datos[elemento]))
            if elemento.startswith("igualdad"):
                self.matriz.append(self.determinar_valor(self.entrada_de_datos[elemento]))
            if elemento.startswith("operacion"):
                self.operacion += self.entrada_de_datos[elemento]
    

    # Matriz inicial con sus variables de holgura y matriz identidad
    def crear_matriz_inicial(self) -> None:
        # Funcion objetivo (Colamos el 1 en la 'Z', seguido de las variables objetivo y completamos con 0)
        self.init_matriz[0].append([1] + self.matriz[:self.objetivo] + [0 for _ in range(self.restriccion+1)])  

        self.agregar_restricciones()

        #'S1, S2 .... Sn'
        holgura = self.Sn(self.restriccion)

        for index in range(self.restriccion):
            # Elimino y guardo el valor de la igualdad de la inecuacion
            igualdad = self.init_matriz[0][index + 1].pop()
            # Agrego la matriz identidad y el valor que elimine previamente
            self.init_matriz[0][index + 1] += next(holgura) + [igualdad]

    # Recorrer las restricciones y armar parte de la primera matriz
    def agregar_restricciones(self) -> None:
        fila = []
        for element in self.matriz[self.objetivo:]:
            fila.append(element)
            # Si es igual a mi variables + la igualdad tenemos la primera retriccion
            if len(fila) == self.objetivo + 1: 
                # Valor de 'Z' mas restriccion
                self.init_matriz[0].append([0] + fila)
                fila = []

    # Ver si es un valor entero o flotante
    @staticmethod
    def determinar_valor(valor: str) -> int or float:
        if valor.find(".") != -1:  # Si se encuentra el punto es float
            return float(valor)
        return int(valor)

    """
    Agregar una matriz identidad, ejemplo:
                    1 0 0
                    0 1 0
                    0 0 1
    """
    @staticmethod
    def Sn(numero: int):
        for col in range(numero):
            yield [1 if row == col else 0 for row in range(numero)]