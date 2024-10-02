from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.endpoints import cat, root

app = FastAPI()

app.title = 'Cat FastAPI'
app.description = 'Light Weight API For Cat Data'


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


app.include_router(cat.router, tags=['cats'], prefix='/api/v1')
app.include_router(root.router, tags=['health'], prefix='/api/v1')
