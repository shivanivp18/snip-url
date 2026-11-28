

from fastapi import FastAPI
from app.routers.auth import router as auth_router

from app.routers.links import router as links_router
app = FastAPI(
    title="Snip URL API"
)

app.include_router(auth_router)
app.include_router(links_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to Snip URL API",
        "status": "running"

        @router.get("/me", response_model=ClientResponse)
    }

