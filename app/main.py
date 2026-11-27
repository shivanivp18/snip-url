

from fastapi import FastAPI
from app.routers.auth import router as auth_router

app = FastAPI(
    title="Snip URL API"
)

app.include_router(auth_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to Snip URL API",
        "status": "running"

        @router.get("/me", response_model=ClientResponse)
    }

