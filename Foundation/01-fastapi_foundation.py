from fastapi import FastAPI
from fastapi import Request
import uvicorn

app = FastAPI(
    title="Dune Service",
    description=(
        "All about dune"
        "Lisal Al Gaib"
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redocs",
    openapi_url="/openapi.json"

)


@app.get("/")
def read_root():
    """ Root Endpoint - Health check """
    return {
        "message":"Welcome to the world of dune",
        "status":"healthy"
        }



@app.get("/about")
def about():
    """ Return about this page""" 
    return {
        "theme":"dune theme",
        "cast" :"timothee,zendaya,robert pattinson"

    }


@app.get("/check")
def check(name: str | None = None, age: int | None = None):
    return {
        "message": "check endpoint is working",
        "name": name,
        "age": age,
    }


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8002)

