from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.routes.user import usuario
from app.routes.pedido import pedido 

# Crear la instancia principal de la aplicación
app = FastAPI(
    title="GESTIÓN DE PEDIDOS FASTAPI Y MONGODB",
    description="ELIGE UNO DE LOS SIGUIENTES ROLES: admin, gerente, cliente, vendedor",
    version="1.0.0",
)

# -----------------------------
#   PERSONALIZACIÓN DEL OPENAPI (Swagger con soporte JWT Bearer)
# -----------------------------
def custom_openapi():
    """
    Esta función personaliza el esquema de OpenAPI para incluir
    la autenticación Bearer en la documentación (Swagger UI).
    """
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    # Añadir esquema JWT Bearer a los componentes de seguridad
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",  # Este formato indica que el token es un JWT
        }
    }

    # Aca estoy empujando para que todos los endpoints requieran token por defecto
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", []).append({"BearerAuth": []})

    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Asignar el nuevo esquema personalizado al OpenAPI de la app
app.openapi = custom_openapi

# -----------------------------
#   INCLUSIÓN DE RUTAS
# -----------------------------
# Importamos el router que contiene las rutas de autenticación y CRUD de usuarios
app.include_router(usuario, tags=["Usuarios"])
app.include_router(pedido, tags=["Ventas"])

# -----------------------------
#   RUTA INICIAL
# -----------------------------
@app.get("/")
async def root():
    """
    Ruta raíz de prueba.
    """
    return {"mensaje": "Bienvenido al sistema de perfilamiento"}




