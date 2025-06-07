# -----------------------------
#         SCHEMAS USER
# -----------------------------


# Función para que reciba un objeto y entregue un diccionario con dict
def userEntity(usuario) -> dict:
    return {
        "id": str(usuario["_id"]),
        "nombre": usuario["nombre"],
        "email": usuario["email"],
        "rol": usuario["rol"],
    }


# Función para retornar una lista
def usersEntity(usuarios) -> dict:
    return [
        userEntity(usuario) for usuario in usuarios
    ]  # Iterar la lista de usuarios y genera un nuevo usuario