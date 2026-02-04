from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

# Base de datos simulada
productos_db = [
    {
        "id": 1,
        "nombre": "Laptop Dell",
        "descripcion": "Laptop Dell Inspiron 15",
        "precio": 15000.00,
        "stock": 10,
        "categoria": "Electrónica"
    },
    {
        "id": 2,
        "nombre": "Mouse Logitech",
        "descripcion": "Mouse inalámbrico",
        "precio": 350.00,
        "stock": 50,
        "categoria": "Accesorios"
    }
]

# Modelo Pydantic
class Producto(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    stock: int
    categoria: str

# Endpoints
@router.get("/productos")
async def obtener_productos():
    """Obtener todos los productos"""
    return productos_db

@router.get("/productos/{producto_id}")
async def obtener_producto(producto_id: int):
    """Obtener un producto por ID"""
    producto = next((p for p in productos_db if p["id"] == producto_id), None)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.post("/productos")
async def crear_producto(producto: Producto):
    """Crear un nuevo producto"""
    nuevo_id = max([p["id"] for p in productos_db]) + 1 if productos_db else 1
    nuevo_producto = {
        "id": nuevo_id,
        **producto.dict()
    }
    productos_db.append(nuevo_producto)
    return nuevo_producto

@router.put("/productos/{producto_id}")
async def actualizar_producto(producto_id: int, producto: Producto):
    """Actualizar un producto existente"""
    for i, p in enumerate(productos_db):
        if p["id"] == producto_id:
            productos_db[i] = {"id": producto_id, **producto.dict()}
            return productos_db[i]
    raise HTTPException(status_code=404, detail="Producto no encontrado")

@router.delete("/productos/{producto_id}")
async def eliminar_producto(producto_id: int):
    """Eliminar un producto"""
    for i, p in enumerate(productos_db):
        if p["id"] == producto_id:
            productos_db.pop(i)
            return {"message": "Producto eliminado correctamente"}
    raise HTTPException(status_code=404, detail="Producto no encontrado")
