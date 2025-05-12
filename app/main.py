from fastapi import FastAPI
from app.api.routes import user,todo
#import uvicorn
app = FastAPI()

#if __name__ == "__main__":
#    uvicorn.run(app, host="127.0.0.1", port=8000)
    
app.include_router(user.router, prefix='/users', tags=['Users'])
app.include_router(todo.router, prefix='/todos', tags=['Todo'])
'''
@app.get('/')
def Main():
    return 'hello'
'''