from fastapi import FastAPI

from app.routers.authentication import router as authentication_router
from app.routers.tasks import router as tasks_router
from app.routers.workspaces import router as workspaces_router

app = FastAPI(
    title="TaskForge API",
    description="Full Backend with JWT Authentication and Tasks CRUD",
    version="1.0",
)


@app.get("/health", status_code=200)
def health():
    return {"status": "working"}


app.include_router(tasks_router)
app.include_router(authentication_router)
app.include_router(workspaces_router)
