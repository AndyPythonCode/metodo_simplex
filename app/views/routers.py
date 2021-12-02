from settings import templates
from fastapi import APIRouter, Request
from .metodo import metodo_simplex

router_views = APIRouter(tags=["Views"])

@router_views .get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request":request})

@router_views.get("/problema")
async def problema(request: Request):
    return templates.TemplateResponse("problema.html", {"request":request})

@router_views.post("/solucion")
async def solucion(request: Request):
    form = await request.body() # Obtener todos los valores de los input en binario
    form = form.decode("utf-8") # Decodificar el binario
    form = eval(string_query_to_dict(form)) # Aca obtengo todos lo datos sin ningun caracter extra;o
    objetivo, restriccion = numero_matriz(form) # Saber la dimencion de la matriz
    matriz = datos(form) # Armar la matriz en fila y columna
    matriz = crear_matriz(matriz, objetivo, restriccion) # Agregar variable de holgura y todo lo que hace falta
    tablas, variables, mensaje = metodo_simplex(matriz, objetivo, restriccion)
    return templates.TemplateResponse("solucion.html", {"request":request, "tablas":tablas, "objetivo":objetivo, 
                                                        "restriccion":restriccion, "salida":variables, "mensaje":mensaje})

# Funciones
def crear_matriz(matriz, objetivo, restriccion):
    init_matriz = []
    init_matriz.append([1] + matriz[:objetivo] + [0 for _ in range(restriccion+1)]) # Funcion objetivo

    agregar_restricciones(matriz, init_matriz, objetivo)

    #Adding 'S1, S2 .... Sn'
    holgura = Sn(restriccion)
    for index in range(restriccion):
        igualdad = init_matriz[index + 1].pop() # La cantidad igualada de las restricciones
        init_matriz[index + 1] += next(holgura) + [igualdad]
    return [init_matriz]

def agregar_restricciones(matriz, init_matriz, objetivo):
    fila = []
    for element in matriz[objetivo:]:
        fila.append(element)
        if len(fila) == objetivo + 1:
            init_matriz.append([0] + fila)
            fila = []

def Sn(numero):
    for col in range(numero):
        yield [1 if row == col else 0 for row in range(numero)]

def string_query_to_dict(form: str):
    form = form.replace("=","':'")
    form = form.replace("&","','")
    form = "{'" + form
    form = form + "'}"
    return form

def numero_matriz(form: dict):
    contar_variables_objetivo = 0
    contar_restricciones = 0
    for i in form:
        if i.startswith("objetivo"):
            contar_variables_objetivo += 1
        if not form[i].replace("-","").isdigit(): # Para los numeros negativos
            contar_restricciones += 1
    return contar_variables_objetivo , contar_restricciones - 1

def datos(form: dict):
    matriz = []
    for element in form:
        if element.startswith("objetivo"):
            matriz.append(int(form[element]) * -1)
        if element.startswith("variable"):
            matriz.append(int(form[element]))
        if element.startswith("igualdad"):
            matriz.append(int(form[element]))
    return matriz