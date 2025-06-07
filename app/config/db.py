# --------------------------------------
# CONEXIÓN A LA BASE DE DATOS MONGODB #
# --------------------------------------
from pymongo import MongoClient

# Conexión a MongoDB (se conecta a localhost:27017 por defecto)
conn = MongoClient(
    "mongodb://localhost:27017/",
    serverSelectionTimeoutMS=5000
)

# Conexión a la base de datos
db = conn["pedidosdb"]

# Definición de colecciones
usuarios_collection = db["usuarios"]
pedidos_collection = db["pedidos"]  # Colección para pedidos