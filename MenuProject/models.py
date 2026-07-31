from pydantic import BaseModel

class MenuItem(BaseModel):
    id:int
    name:str
    description:str
    available:bool
    category:str
    price:int



class MenuResponse(BaseModel):
    status:str = "success"
    count:int
    items: list[MenuItem]    