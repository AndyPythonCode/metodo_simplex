from fastapi.templating import Jinja2Templates

API_INFO = {
    "title":"Metodo Simplex",
    "description": "Proyecto",
    "version": "0.0.1"
    }

templates = Jinja2Templates(directory="templates")

STATIC_FILES = "static"