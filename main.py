import uvicorn
from fastapi import FastAPI

from src.routes import fornecedores

app = FastAPI()
app.include_router(fornecedores.router)

@app.get('/')
def index():
    return {'message': 'Hello World!'}


if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="0.0.0.0", log_level="debug", port=8000, reload=True
    )
