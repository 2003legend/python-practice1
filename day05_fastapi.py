from fastapi import FastAPI
app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "Hello, 李剑东"}
@app.get("/hello/{name}")
def say_hello(name: str):
    return {"msg": f"Hello, {name}"}