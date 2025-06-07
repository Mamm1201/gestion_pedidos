from fastapi import APIRouter, HTTPException, Response, status
from app.models.pedido import Pedido
from app.config.db import pedidos_collection
from bson import ObjectId
from datetime import datetime
from typing import List

pedido = APIRouter(prefix="/pedidos")

# --------------------------
# Operaciones CRUD para Pedidos
# --------------------------

@pedido.get("/", response_model=List[dict], response_description="Lista todos los pedidos")
async def listar_pedidos():
    """
    Obtiene todos los pedidos registrados en la base de datos.
    Retorna una lista de pedidos con sus detalles.
    """
    try:
        pedidos = list(pedidos_collection.find({}))
        return [{
            "id": str(pedido.get("_id")),
            "pedidos_cancelados": pedido.get("pedidos_cancelados", 0),
            "pedidos_enviados": pedido.get("pedidos_enviados", 0),
            "pedidos_pagados": pedido.get("pedidos_pagados", 0),
            "pedidos_reenviados": pedido.get("pedidos_reenviados", 0),
            "fecha": pedido.get("fecha", datetime.now()).isoformat()
        } for pedido in pedidos]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener los pedidos: {str(e)}"
        )

@pedido.post("/", status_code=status.HTTP_201_CREATED, response_description="Crea un nuevo pedido")
async def crear_pedido(pedido_data: Pedido):
    """
    Crea un nuevo registro de pedido en la base de datos.
    La fecha se genera automáticamente si no se proporciona.
    """
    try:
        # Convertimos el modelo Pydantic a diccionario
        pedido_dict = pedido_data.dict()
        
        # Insertamos el pedido en la colección
        resultado = pedidos_collection.insert_one(pedido_dict)
        
        # Obtenemos el pedido recién creado como diccionario
        pedido_creado = pedidos_collection.find_one({"_id": resultado.inserted_id})
        
        # Convertimos el ObjectId a string y aseguramos la serialización
        pedido_creado["_id"] = str(pedido_creado["_id"])
        
        # Convertimos la fecha a ISO format si existe
        if "fecha" in pedido_creado and isinstance(pedido_creado["fecha"], datetime):
            pedido_creado["fecha"] = pedido_creado["fecha"].isoformat()
            
        return pedido_creado
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear el pedido: {str(e)}"
        )

@pedido.get("/{pedido_id}", response_description="Obtiene un pedido específico")
async def obtener_pedido(pedido_id: str):
    """
    Obtiene los detalles de un pedido específico por su ID.
    """
    if not ObjectId.is_valid(pedido_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El ID proporcionado no es válido"
        )
    
    pedido = pedidos_collection.find_one({"_id": ObjectId(pedido_id)})
    
    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido no encontrado"
        )
    
    return {
        "id": str(pedido["_id"]),
        "pedidos_cancelados": pedido.get("pedidos_cancelados", 0),
        "pedidos_enviados": pedido.get("pedidos_enviados", 0),
        "pedidos_pagados": pedido.get("pedidos_pagados", 0),
        "pedidos_reenviados": pedido.get("pedidos_reenviados", 0),
        "fecha": pedido.get("fecha", datetime.now()).isoformat()
    }

@pedido.put("/{pedido_id}", response_description="Actualiza un pedido existente")
async def actualizar_pedido(pedido_id: str, pedido_data: Pedido):
    """
    Actualiza los datos de un pedido existente.
    """
    if not ObjectId.is_valid(pedido_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El ID proporcionado no es válido"
        )
    
    pedido_dict = pedido_data.dict()
    
    resultado = pedidos_collection.update_one(
        {"_id": ObjectId(pedido_id)},
        {"$set": pedido_dict}
    )
    
    if resultado.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido no encontrado"
        )
    
    pedido_actualizado = pedidos_collection.find_one({"_id": ObjectId(pedido_id)})
    return {
        "id": str(pedido_actualizado["_id"]),
        **pedido_dict,
        "fecha": pedido_actualizado["fecha"].isoformat()
    }

@pedido.delete("/{pedido_id}", status_code=status.HTTP_204_NO_CONTENT, response_description="Elimina un pedido")
async def eliminar_pedido(pedido_id: str):
    """
    Elimina un pedido de la base de datos.
    """
    if not ObjectId.is_valid(pedido_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El ID proporcionado no es válido"
        )
    
    resultado = pedidos_collection.delete_one({"_id": ObjectId(pedido_id)})
    
    if resultado.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido no encontrado"
        )
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)