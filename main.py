from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
async def hello_page():
    return {"msg": "Hello world!"}

