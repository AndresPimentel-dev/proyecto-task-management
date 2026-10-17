# main.py
from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

# Importas el limiter centralizado
from app.limiter import limiter
from app.routers.authentication import router as authentication_router
from app.routers.tasks import router as tasks_router
from app.routers.workspaces import router as workspaces_router

app = FastAPI(
    title="TaskForge API",
    description="Full Backend with JWT Authentication and Tasks CRUD",
)

# 1. Asignas el limitador al estado global
app.state.limiter = limiter

# Nota: en algunas versiones de fastapi/slowapi se usa app.add_exception_handler como lo tenías:
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/health", status_code=200)
def health():
    return {"status": "working"}

@app.get("/")
def read_root():
  return {
      "message": "Bienvenido a TaskForge API",
      "docs": "Visita /docs para ver la documentación",
  }


# 3. Incluyes tus routers normalmente (SIN dependencies de limiter)
app.include_router(tasks_router)
app.include_router(authentication_router)
app.include_router(workspaces_router)
