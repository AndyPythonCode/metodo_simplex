from .metodo import MetodoSimplex


class Minimizar(MetodoSimplex):
    def __init__(self, matriz, restricciones, objetivos) -> None:
        super().__init__(matriz, restricciones, objetivos)

    def metodo_simplex(self):
        while True:
            self.ultima_tabla = self.matriz[-1]
            self.funcion_objetivo = self.ultima_tabla[0]

            self.columna_pivote()
            self.fila_pivote()
            self.lista_index_pivote.append((self.index_columna_pivote,self.index_fila_pivote))

            # Si todas las filas son negativa se ha terminado el problema
            if all([True if numero <= 0 else False for numero in self.funcion_objetivo[1:]]):
                break

            # Solucion no acotada
            if self.solucion_no_acotada:
                break

            self.elemento_pivote = self.ultima_tabla[self.index_fila_pivote][self.index_columna_pivote]
            self.nueva_tabla = self.ultima_tabla.copy()
            self.nueva_tabla[self.index_fila_pivote] = self.elemento_pivote_en_uno()
            self.fila_nueva()

    # La posicion de la columna a convertir en 1
    def columna_pivote(self) -> None:
        posicion = 1
        maximo = self.funcion_objetivo[posicion]
        for index, numero in enumerate(self.funcion_objetivo):
            if maximo < numero and index != 0:
                maximo = numero
                posicion = index
        self.index_columna_pivote = posicion
