from fastapi import FastAPI, HTTPException
from api.routes import transactions
from utils.logging import setup_logging

setup_logging()

app = FastAPI(
    title="Transaction Categorizer API",
    description="API for categorizing financial transactions using machine learning",
    version="1.0.0"
)


app.include_router(transactions.router, prefix="/api/v1", tags=["transactions"])

@app.get("/")
async def root():
    return {"message": "Transaction Categorizer API is running"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
