from fastapi import FastAPI
import uvicorn

my_app = FastAPI()

@my_app.get("/")
def read_root():
    return {"message": "hello everyone!"}

@my_app.get("/item/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "query": q}


@my_app.put("/products")
# PUT requests can be sent from the OpenAPI docs or any HTTP client
def update_product(product_name: str | None = None, product_type: str | None = None):
    return {"product_name": product_name, "product_type": product_type}

if __name__ == "__main__":
    uvicorn.run(my_app, host="0.0.0.0", port=8000)