from fastapi import FastAPI
from app.routes import categories, products, orders

app=FastAPI(title = "stockFlow API")
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(orders.router)

@app.get("/")
def home():
    return {"message" : "Welcome to StockFlow API"}

