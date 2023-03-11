from fastapi import FastAPI, HTTPException,APIRouter,Depends
from typing import Dict
from schemas import Product
from routes.auth import get_token
import json


router = APIRouter()

# Load the product data from the JSON file
with open("./json/products.json", "r") as product_file:
    product_db = json.load(product_file)


# Define a function to get a product by its ID
def get_product(product_id: str) -> Product:
    if product_id not in product_db:
        raise HTTPException(status_code=404, detail="Product not found")
    product_data = product_db[product_id]
    return Product(**product_data)

@router.get("/products",status_code=200,tags=["products"],summary="Read all product",
    description="Read all product with all the information")
async def read_products():
    return product_db

# Define an endpoint to get a product by its ID
@router.get("/products/{product_id}", response_model=Product,tags=["products"],summary="Read an single product",
    description="Read an product with Id")
async def read_product(product_id: str,token: str = Depends(get_token)):
    return get_product(product_id)

# Define an endpoint to create a new product
@router.post("/products", response_model=Product,tags=["products"],status_code=201,summary="Create an product",
    description="Create an product with all the information, name,price,quantity and Image")
async def create_product(product: Product,token: str = Depends(get_token)):
    product_id = product.productId
    if product_id in product_db:
        raise HTTPException(status_code=400, detail="Product already exists")
    product_db[product_id] = product.dict()
    with open("./json/products.json", "w") as product_file:
        json.dump(product_db, product_file, indent=2)
    return product

# Define an endpoint to update an existing product
@router.put("/products/{product_id}", response_model=Product,tags=["products"],status_code=200,summary="Update an product",
    description="Update poduct with Id")
async def update_product(product_id: str, product: Product,token: str = Depends(get_token)):
    if product_id not in product_db:
        raise HTTPException(status_code=404, detail="Product not found")
    if product_id != product.productId:
        raise HTTPException(status_code=400, detail="Product ID cannot be changed")
    product_dict = product.dict()
    product_db[product_id].update(product_dict)
    with open("./json/products.json", "w") as product_file:
        json.dump(product_db, product_file, indent=2)
    return Product(**product_db[product_id])

# Define an endpoint to delete an existing product
@router.delete("/products/{product_id}", response_model=Product,tags=["products"],status_code=202,summary="Delete an product",
    description="Delete product with Id")
async def delete_product(product_id: str,token: str = Depends(get_token)):
    if product_id not in product_db:
        raise HTTPException(status_code=404, detail="Product not found")
    deleted_product_data = product_db.pop(product_id)
    with open("./json/products.json", "w") as product_file:
        json.dump(product_db, product_file, indent=2)
    return Product(**deleted_product_data)
