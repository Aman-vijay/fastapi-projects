from fastapi import FastAPI
import uvicorn
from db import create_tables, drop_tables
from sqlmodel import Session
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    print("Tables created")
    yield
    print("Tables dropped")
    drop_tables()

app = FastAPI(
    title="BookExchange Api", 
    description="API for the BookExchange project",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

@app.get("/")
def read_root():
    return {"message": "Hello World from BookExchange Api"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
