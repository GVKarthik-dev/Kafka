from fastapi import FastAPI
from app import orders, transactions, analytics, email

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Kafka FastAPI is running!"}

# Include routes from other modules
app.include_router(orders.router)
app.include_router(transactions.router)
app.include_router(analytics.router)
app.include_router(email.router)
