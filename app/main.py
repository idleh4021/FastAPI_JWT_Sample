from fastapi import FastAPI
from api.routes import user,todo
app = FastAPI()


app.include_router(user.router, prefix='/users', tags=['Users'])
#app.include_router(todo.router, prefix='/todos', tags=['Todo'])
'''
@app.get('/')
def Main():
    return 'hello'
'''