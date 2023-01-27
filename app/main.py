from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import localidades
from .Database import engine
from app import Models

app = FastAPI()

origins = [ settings.CLIENT_ORIGIN,  ]
Models.Base.metadata.create_all(bind=engine, checkfirst=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(localidades.router,  prefix='/api/localidades')


@app.get('/api')
def root():
    return {'message': 'ok'}