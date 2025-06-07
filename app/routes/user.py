from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from datetime import datetime, timedelta
from app.config.db import usuarios_collection
from app.models.user import User
from app.schemas.user import userEntity, usersEntity
from bson import ObjectId

# Clave secreta y algoritmo JWT
SECRET_KEY = "secretito123"
ALGORITHM = "HS256"

# Crear el enrutador FastAPI
usuario = APIRouter()

# Seguridad basada en encabezado Authorization: Bearer <token>
security = HTTPBearer()

# -----------------------------
#       FUNCIONES JWT
# -----------------------------

def crear_token(user: dict):
    """
    Crea un JWT con email, rol y expiración de 1 hora.
    """
    payload = {
        "sub": user["email"],
        "rol": user["rol"],
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def obtener_usuario_actual(token: HTTPAuthorizationCredentials = Depends(security)):
    """
    Decodifica el JWT y retorna el payload.
    Lanza 401 si el token es inválido o ha expirado.
    """
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Payload decodificado: {payload}")
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado")

def permitir_roles(*roles_permitidos):
    """
    Decorador para permitir acceso solo a ciertos roles.
    Se usa con Security().
    """
    def verificar(user=Depends(obtener_usuario_actual)):
        print(f"Rol del usuario: {user.get('rol')}, roles permitidos: {roles_permitidos}")
        if user["rol"] not in roles_permitidos:
            raise HTTPException(
                status_code=403,
                detail=f"No tienes permiso para acceder. Roles permitidos: {roles_permitidos}"
            )
        return user
    return verificar

# -----------------------------
#         RUTAS JWT
# -----------------------------

@usuario.post("/login")
def login(email: str):
    """
    Login: genera token si el usuario existe.
    """
    user = usuarios_collection.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    token = crear_token(user)
    print(token)
    return {"access_token": token}

@usuario.get("/admin")
def acceso_admin(user=Security(permitir_roles("admin"))):
    """
    Acceso exclusivo para usuarios con rol 'admin'.
    """
    return {"mensaje": "Bienvenido, administrador", "usuario": user}

@usuario.get("/user")
def acceso_usuario(user=Security(permitir_roles("usuario"))):
    """
    Acceso exclusivo para usuarios con rol 'usuario'.
    """
    return {"mensaje": f"Bienvenido, usuario con rol {user['rol']}", "usuario": user}

@usuario.get("/ventas")
def ver_ventas(user=Security(permitir_roles("admin", "gerente", "vendedor"))):
    """
    Acceso permitido a roles: admin, gerente, vendedor.
    """
    return {"mensaje": f"Bienvenido a ventas, rol: {user['rol']}"}

@usuario.get("/perfil")
def ver_perfil(user=Depends(obtener_usuario_actual)):
    """
    Retorna información del usuario autenticado.
    """
    return {"email": user['sub'], "rol": user['rol']}

# -----------------------------
#         CRUD USUARIOS
# -----------------------------

@usuario.get("/users")
def find_all_users():
    """
    Devuelve todos los usuarios.
    """
    return usersEntity(usuarios_collection.find())

@usuario.post("/users")
def create_user(user: User):
    """
    Crea un nuevo usuario.
    """
    new_user = dict(user)
    if "id" in new_user:
        del new_user["id"]
    id = usuarios_collection.insert_one(new_user).inserted_id
    user = usuarios_collection.find_one({"_id": id})
    return userEntity(user)

@usuario.get("/users/{id}")
def find_user(id: str):
    """
    Busca un usuario por ID.
    """
    user = usuarios_collection.find_one({"_id": ObjectId(id)})
    return userEntity(user)

@usuario.put("/users/{id}")
def update_user(id: str, user: User):
    """
    Actualiza un usuario por ID.
    """
    usuarios_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": dict(user)}
    )
    user = usuarios_collection.find_one({"_id": ObjectId(id)})
    return userEntity(user)

@usuario.delete("/users/{id}")
def delete_user(id: str):
    """
    Elimina un usuario por ID.
    """
    deleted_user = usuarios_collection.find_one_and_delete({"_id": ObjectId(id)})
    if not deleted_user:
        return {"error": "Usuario no encontrado"}
    return {"mensaje": "Usuario eliminado correctamente"}





