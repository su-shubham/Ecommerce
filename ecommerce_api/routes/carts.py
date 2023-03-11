from fastapi import APIRouter, Depends, HTTPException
from routes.auth import get_token
import json

router = APIRouter()

# Load products from the products.json file
with open("./json/products.json") as f:
    products_db = json.load(f)

# This would be your JSON file that stores cart data
# We will assume the file name is "carts.json"
carts_db = {}

# API for adding a new product to the cart
@router.post("/cart/add_product/{user_id}/{product_id}/{quantity}",tags=["carts"])
async def add_to_cart(user_id: str, product_id: str, quantity: int,token: str = Depends(get_token)):
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    if quantity < 1:
        raise HTTPException(status_code=400, detail="Invalid quantity")

    if user_id not in carts_db:
        carts_db[user_id] = {}

    if product_id not in carts_db[user_id]:
        carts_db[user_id][product_id] = {"quantity": quantity}
    else:
        carts_db[user_id][product_id]["quantity"] += quantity

    return {"message": "Product added to cart successfully"}

# API for updating the quantity of a product in the cart
@router.put("/cart/update_product/{user_id}/{product_id}/{quantity}",tags=["carts"])
async def update_cart_product(user_id: str, product_id: str, quantity: int,token: str = Depends(get_token)):
    if user_id not in carts_db or product_id not in carts_db[user_id]:
        raise HTTPException(status_code=404, detail="Product not found in cart")
    if quantity < 1:
        raise HTTPException(status_code=400, detail="Invalid quantity")

    carts_db[user_id][product_id]["quantity"] = quantity

    return {"message": "Product quantity updated successfully"}

# API for deleting a product from the cart
@router.delete("/cart/remove_product/{user_id}/{product_id}",tags=["carts"])
async def remove_from_cart(user_id: str, product_id: str,token: str = Depends(get_token)):
    if user_id not in carts_db or product_id not in carts_db[user_id]:
        raise HTTPException(status_code=404, detail="Product not found in cart")

    del carts_db[user_id][product_id]

# API for getting the aggregated cart information
@router.get("/cart/{user_id}",tags=["carts"])
async def get_cart_info(user_id: str,token: str = Depends(get_token)):
    if user_id not in carts_db:
        raise HTTPException(status_code=404, detail="Cart not found")

    total_price = 0.0
    total_quantity = 0
    cart_items = []

    for product_id, item in carts_db[user_id].items():
        if product_id not in products_db:
            continue

        product = products_db[product_id]
        item_price = product["price"] * item["quantity"]
        total_price += item_price
        total_quantity += item["quantity"]
        cart_items.append({
            "id": product_id,
            "name": product["name"],
            "quantity": item["quantity"],
            "price": product["price"],
            "item_price": item_price,
            "image": product["image"]
        })

    return {
        "total_price": total_price,
        "total_quantity": total_quantity,
        "items": cart_items
    }
