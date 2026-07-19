from fastapi import FastAPI
from PhotoShare.routes import auth
from PhotoShare.routes import photos

app = FastAPI(title="PhotoShare API")

app.include_router(auth.router)
app.include_router(photos.router)

@app.get("/")
def root():
    return {"message": "PhotoShare API is running"}

