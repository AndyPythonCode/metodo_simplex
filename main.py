import settings
import urls
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI(**settings.API_INFO)

# Static files
app.mount("/static", StaticFiles(directory=settings.STATIC_FILES), name="static")

# Path
[app.include_router(path) for path in urls.URL_PATTERNS]

@app.on_event("startup")
async def startup():
    print("\nGo to: http://localhost:8000/\n")