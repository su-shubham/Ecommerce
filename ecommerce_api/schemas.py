from pydantic import BaseModel


class Product(BaseModel):
    productId: str
    image: str
    name: str
    price: float
    quantity: int
