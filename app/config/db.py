# --------------------------------------
# CONEXIÓN A LA BASE DE DATOS MONGODB #
# --------------------------------------
from pymongo import MongoClient

conn = (
    MongoClient()
)  # Con la variable conn estoy conectandome a una base de datos de Mongo