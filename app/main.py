from fastapi import FastAPI
from app.database import engine
from app import models
from app.routers import notes, analytics

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI-Enhanced Notes Management System")

app.include_router(notes.router, prefix="/api", tags=["notes"])
app.include_router(analytics.router, prefix="/api", tags=["analytics"])

@app.get("/")
def read_root():
    return {"message": "Welcome to AI-Enhanced Notes Management System"}