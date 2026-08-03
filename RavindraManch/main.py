from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from db import create_table

@asynccontextmanager
async def lifespan(app:FastAPI):
    create_table()
    print("Database table created")
    yield
    print("Shutting down")



app =  FastAPI(
    title="Ravindrmanch API",
    description="This is the api for ravindramanch with sql data",
    lifespan=lifespan
)


@app.get("/")
def root():
    return {"message":"Hello this is ravindramanch api"}