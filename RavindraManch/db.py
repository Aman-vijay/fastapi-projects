from sqlmodel import SQLModel,Session,create_engine

DB_URL = "sqlite:///ravindramanch.db"

engine = create_engine(DB_URL,echo=True)

def create_table():
    """To create all tables in sqllite"""
    SQLModel.metadata.create_all(engine)

def get_session():
    """To get per db session """
    with Session(engine) as session:
        yield session    