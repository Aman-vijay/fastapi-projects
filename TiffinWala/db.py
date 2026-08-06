from sqlmodel import create_engine, Session, SQLModel
from model import Order, StatusList


DATABASE_URL = "sqlite:///tiffinwala.db"
#Create Database Engine
engine = create_engine(DATABASE_URL,echo=True)


def create_table():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


