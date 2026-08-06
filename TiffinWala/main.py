from fastapi import FastAPI
import uvicorn
from routes.orders import router as orders_router
from routes.stats import router as stats_router
from db import create_table
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_table()  # Create tables
    print("Tables created")
    yield  # Wait for the application to start
    print("Tables dropped")

app = FastAPI(
    title="TiffinWala API Documentation",
    description="TiffinWala is a web application for managing tiffin services",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(orders_router)
app.include_router(stats_router)
@app.get("/")
def read_root():
    return {"message": "Welcome to TiffinWala API Documentation"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
