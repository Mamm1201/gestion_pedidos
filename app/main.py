from fastapi import FastAPI
from fastapi import APIRouter


app = FastAPI(title="SISTEMA DE GESTIÓN PEDIDOS")

@app.get("/")
def read_root():
    return {"message": "FastAPI + MongoDB funcionando"}

