from fastapi import FastAPI
from contextlib import asynccontextmanager
from db import create_table
from routes.reviews import router


@asynccontextmanager
async def lifespan(app:FastAPI):
    create_table()
    print("Database table has been created")
    yield
    #shutdown
    print("Database has been shut down")




app = FastAPI(
    title="Ravindramanch API",
    description="This is the api for ravindramanch",
    lifespan=lifespan
)

app.include_router(router)


@app.get("/")
def root():
    return {"message":"Hello this is Ravindramanch Api"}