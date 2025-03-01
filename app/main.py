from fastapi import FastAPI
from app.api.v1.endpoints import x, goal
from app.db.session import engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/", tags=["home"])
def read_root():
    return {"message": "Welcome to FastAPI with Selenium!"}

app.include_router(goal.router, prefix="/api/v1") 
app.include_router(x.router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
