from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel

from app.modules.users.router import router as user_router


app = FastAPI()

app.include_router(user_router)

# -------------------------- #
# Using Enum
# -------------------------- #
class ModelName(str, Enum):
  alexnet = "alexnet"
  resnet = "resnet"
  lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
  if model_name is ModelName.alexnet:
    return {"model_name": model_name, "message": "Deep Learning FTW!"}
  if model_name.value == "lenet":
    return {"model_name": model_name, "message": "LeCNN all the images"}
  return {"model_name": model_name, "message": "Have some residuals"}

# -------------------------- #
# Using :path
# /files/home/johndoe/myfile.txt -> file_path = /home/johndoe/myfile.txt
# It will response not found error if not using :path
# -------------------------- #
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

# -------------------------- #
# Query Parameter
# When you declare other function parameters that are not part of the path parameters, they are automatically interpreted as "query" parameters.
# -------------------------- #
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

# Default parameters
@app.get("/items")
async def read_itmes(skip: int = 0, limit: int = 10):
  return fake_items_db[skip : skip + limit]

# Optional parameters
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None):
  if q:
    return {"item_id": item_id, "q": q}
  return {"item_id": item_id}

# Query parameter type conversion
# - http://127.0.0.1:8000/items2/foo?short=1
# - http://127.0.0.1:8000/items2/foo?short=True
# - http://127.0.0.1:8000/items2/foo?short=true
# - http://127.0.0.1:8000/items2/foo?short=on
# - http://127.0.0.1:8000/items2/foo?short=yes
# or any other case variation (uppercase, first letter in uppercase, etc), your function will see the parameter short with a bool value of True. Otherwise as False.
@app.get("/items2/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
  item = {"item_id": item_id}
  if q:
    item.update({"q": q})
  if not short:
    item.update(
      {"description": "This is an amazing item that has a long description"}
    )
  return item

# Required query parameters
@app.get("/user-items/{item_id}")
async def read_user_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item

# ============================================================== #
# Request Body
# ============================================================== #

# Create your data model that inherits from pydantic BaseModel
class Item(BaseModel):
  name: str
  description: str | None = None
  price: float
  tax: float | None = None

@app.post("/items")
async def create_item(item: Item):
  item_dict = item.model_dump()
  if item.tax is not None:
    price_with_tax = item.price + item.tax
    item_dict.update({"price_with_tax": price_with_tax})
  return item_dict


# ============================================================== #
# Query Parameters and String Validations
# ============================================================== #


