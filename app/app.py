from fastapi import FastAPI
from routes.s3 import s3_router

app = FastAPI()
app.include_router(s3_router)

@app.get("/")
def index():
    return {"message": "Hello, Docker with FastAPI! 🚀"}

