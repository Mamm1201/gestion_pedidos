# -----------------------------
#     MODELO BASE PEDIDOS
# -----------------------------

# Importación de módulos necesarios
from datetime import datetime  # Para manejar fechas y horas
from pydantic import BaseModel, Field  # BaseModel para crear modelos de datos, Field para configurar campos
from typing import Optional  # Para tipos de datos opcionales (no se usa en este modelo pero es común incluirlo)
from bson import ObjectId  # Para manejar ObjectId de MongoDB

class Pedido(BaseModel):
    """
    Modelo Pydantic que representa un documento de pedido en MongoDB.
    Define la estructura de datos y validaciones para los pedidos.
    """
    
    # Campos del modelo con sus tipos de datos
    pedidos_cancelados: int  # Número de pedidos cancelados (entero requerido)
    pedidos_enviados: int    # Número de pedidos enviados (entero requerido)
    pedidos_pagados: int     # Número de pedidos pagados (entero requerido)
    pedidos_reenviados: int  # Número de pedidos reenviados (entero requerido)
    
    # Campo de fecha con valor por defecto automático
    fecha: datetime = Field(
        default_factory=datetime.now,  # Genera automáticamente la fecha/hora actual al crear un nuevo pedido
        description="Fecha y hora de registro del pedido"  # Descripción para documentación
    )

    class Config:
        """
        Clase de configuración para el modelo Pydantic.
        """
        
        # Configuración para serializar ObjectId de MongoDB a string en JSON
        json_encoders = {
            ObjectId: str  # Convierte ObjectId a string cuando se serializa a JSON
        }
        
        # Ejemplo de documento para la documentación automática (Swagger/OpenAPI)
        schema_extra = {
            "example": {
                "pedidos_cancelados": 100,
                "pedidos_enviados": 500,
                "pedidos_pagados": 180,
                "pedidos_reenviados": 2,
                "fecha": "2023-10-25T00:00:00Z"  # Ejemplo en formato ISO 8601
            }
        }