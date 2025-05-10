from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def Main():
    return 'hello'