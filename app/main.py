from fastapi import FastAPI
from .routers import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allowing reqs from local client
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Quais origens são permitidas
    allow_credentials=True,
    allow_methods=["*"],              # Quais métodos (GET, POST, etc)
    allow_headers=["*"],              # Quais headers
)

app.include_router(router)