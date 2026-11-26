
from fastapi import FastAPI

app = FastAPI(
    title="Snip URL API",
    description="URL Shortener with Analytics",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to Snip URL API",
        "status": "running"
    }
