from fastapi import FastAPI
import uvicorn
from db import create_tables
from sqlmodel import Session
from contextlib import asynccontextmanager
from routes.users import users_router
from routes.books import books_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    print("Tables created")
    yield


app = FastAPI(
    title="BookExchange Api", 
    description="API for the BookExchange project",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

app.include_router(users_router)
app.include_router(books_router)

@app.get("/")
def read_root():
    return {"message": "Hello World from BookExchange Api"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
