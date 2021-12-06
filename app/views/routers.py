from settings import templates
from fastapi import APIRouter, Request
from app.views.minimizar import Minimizar
from app.views.maximizar import Maximizar
from app.views.manipular import EntradaDinamica

router_views = APIRouter(tags=["Views"])


@router_views .get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request":request})

@router_views.get("/problema")
def problema(request: Request):
    return templates.TemplateResponse("problema.html", {"request":request})

@router_views.post("/solucion")
async def solucion(request: Request):
    # Obtener cada uno de los input de forma dinamica (vuelve el valor en binario)
    form: bytes = await request.body() 

    entrada = EntradaDinamica(form) 
    entrada.str_to_dict()
    entrada.dimension_matriz()
    entrada.extraer_valor_dict()
    entrada.crear_matriz_inicial()

    if entrada.operacion == "maximizar":
        objeto = Maximizar(entrada.init_matriz, entrada.restriccion, entrada.objetivo)
    elif entrada.operacion == "minimizar":
        objeto = Minimizar(entrada.init_matriz, entrada.restriccion, entrada.objetivo)

    objeto.metodo_simplex()
    objeto.salida_de_variables()
    return templates.TemplateResponse("solucion.html", { "request":request, "objeto": objeto })