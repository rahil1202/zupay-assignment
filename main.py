from fastapi import FastAPI

from routers import users, blogs

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(users.router, tags=["users"], prefix="/users")
app.include_router(blogs.router, tags=["blogs"], prefix="/blogs")
