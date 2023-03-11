from fastapi import FastAPI,Depends
from routes import products,carts
from routes.auth import get_token
import uvicorn


app = FastAPI()


app.include_router(products.router,dependencies=[Depends(get_token)])
app.include_router(carts.router)


@app.get('/')
async def main():
    return "Welcome to su-shubham Ecommerce shop"

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)