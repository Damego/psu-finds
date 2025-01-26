import os
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


sys.path.insert(1, os.path.join(sys.path[0], ".."))

from .api.routers import routers


app = FastAPI()


@app.get("/")
def index():
    return {"Hello": "World"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Origin"],
)

for router in routers:
    app.include_router(router)
