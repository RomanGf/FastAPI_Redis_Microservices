import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

redis = get_redis_connection(
    host="redis-15269.c250.eu-central-1-1.ec2.cloud.redislabs.com",
    port=15269,
    password="mB4CDWACSS3SZuG6ADA5xDQvhDuKdyD2",
    decode_responses=True
)

class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis

def format(pk: str):
    product = Product.get(pk)
    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity
    }

@app.get('/products')
async def get_all_products():
    return [format(pk) for pk in Product.all_pks()]

@app.post('/products')
async def create_product(product: Product):
    return product.save()

@app.get('/products/{pk}')
async def get_product(pk: str):
    return Product.get(pk)

@app.delete('/products/{pk}')
async def delete_product(pk: str):
    return Product.delete(pk)


if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8080, reload=True)