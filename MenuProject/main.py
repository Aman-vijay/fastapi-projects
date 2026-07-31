from fastapi import FastAPI,Query,HTTPException
from data import menu_Items
import uvicorn
from typing import Optional
from models import MenuItem,MenuResponse
app = FastAPI(
    title="Menu File",
    description="Read only menu API"
)


@app.get("/")
def root():
    return {"message":"API working fine"}





@app.get("/menu",response_model=MenuResponse)
def get_menu(category: Optional[str] = Query(None, description="This is the filtered item query")):
    if category:
        # compare case-insensitively
        filtered = [item for item in menu_Items if str(item.get("category","")).lower() == category.lower()]
        if not filtered:
            raise HTTPException(status_code=404,detail=f"No item found of this category:{category}")
        return MenuResponse(count=len(filtered),items = filtered)

    return MenuResponse(count=len(menu_Items),items=menu_Items)



@app.get("/menu/{item_id}",response_model=MenuItem) 
def get_particular_item(item_id:int):
    for item in menu_Items: 
        if item["id"]==item_id:
            return item 
    raise HTTPException(status_code=404,detail=f"Item not found")
            




if __name__ == "__main__":
    uvicorn.run("main:app",host="127.0.0.1",port=8001,reload=True)
