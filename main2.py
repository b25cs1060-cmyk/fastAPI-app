from fastapi import FastAPI
from pydantic import BaseModel

my_app2 = FastAPI()


class Items(BaseModel):
    item_id: int
    item_name: str
    item_price: int

@my_app2.post("/items")
def insert_item_info(item: Items):
     print(item)
     return item
     

if __name__ == "__main__":
     import uvicorn
     uvicorn.run(my_app2 ,  host ="0.0.0.0" , port=8000 )
