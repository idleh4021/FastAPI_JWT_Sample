from fastapi import FastAPI
from api.routes import user
app = FastAPI()


app.include_router(user.router, prefix="/users", tags=["Users"])
'''
@app.get("/")
def Main():
    return 'hello'
'''