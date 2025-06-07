from bson import ObjectId
from datetime import datetime

def pedidoEntity(pedido) -> dict:
    """
    Versión corregida que maneja campos faltantes y tipos de datos consistentes
    con el modelo Pydantic.
    """
    return {
        "id": str(pedido["_id"]),
        "pedidos_enviados": int(pedido.get("pedidos_enviados", 0)),  # Conversión explícita a int
        "pedidos_cancelados": int(pedido.get("pedidos_cancelados", 0)),
        "pedidos_pagados": int(pedido.get("pedidos_pagados", 0)),
        "pedidos_reenviados": int(pedido.get("pedidos_reenviados", 0)),
        "fecha": pedido.get("fecha", datetime.now()).isoformat() if pedido.get("fecha") else None
    }

def pedidosEntity(pedidos) -> list:
    """Versión segura para listados"""
    return [pedidoEntity(pedido) for pedido in pedidos]

def pedidoEntityCreate(pedido) -> dict:
    """Versión para creación con manejo de campos faltantes"""
    return {
        "id": str(pedido.inserted_id),
        "pedidos_enviados": int(pedido.get("pedidos_enviados", 0)),
        "pedidos_cancelados": int(pedido.get("pedidos_cancelados", 0)),
        "pedidos_pagados": int(pedido.get("pedidos_pagados", 0)),
        "pedidos_reenviados": int(pedido.get("pedidos_reenviados", 0)),
        "fecha": pedido.get("fecha", datetime.now()).isoformat()
    }
    