from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routers import productos

app = FastAPI(
    title="API de Gestión de Inventarios",
    description="Sistema para gestionar productos, categorías y stock",
    version="1.0.0"
)

# Montar archivos estáticos (CSS, JS, imágenes)
app.mount("/css", StaticFiles(directory="static/css"), name="css")
app.mount("/js", StaticFiles(directory="static/js"), name="js")

# Configurar motor de templates Jinja2
templates = Jinja2Templates(directory="templates")

# Incluir routers de la API
app.include_router(productos.router, prefix="/api/v1", tags=["Productos"])


@app.get("/", tags=["Inicio"])
async def home(request: Request):
    """
    Página de inicio del sistema con estadísticas en tiempo real
    """
    # Importar base de datos de productos
    from app.routers.productos import productos_db
   
    # Calcular estadísticas
    total = len(productos_db)
    disponibles = len([p for p in productos_db if p.get("stock", 0) > 0])
   
    # Calcular valor total del inventario
    if total > 0:
        valor_total = sum([p.get("precio", 0) * p.get("stock", 0) for p in productos_db])
    else:
        valor_total = 0
   
    # Datos que se pasan al template
    context = {
        "request": request,  # Obligatorio para Jinja2
        "titulo": "Sistema de Gestión de Inventarios",
        "descripcion": "API REST desarrollada con FastAPI",
        "total_productos": total,
        "productos_disponibles": disponibles,
        "valor_inventario": f"${valor_total:,.2f}",
        "features": [
            {
                "icono": "📦",
                "titulo": "Productos",
                "descripcion": "Gestión completa de productos con validaciones de datos"
            },
            {
                "icono": "📊",
                "titulo": "Categorías",
                "descripcion": "Control y administración de categorías del inventario"
            },
            {
                "icono": "📈",
                "titulo": "Stock",
                "descripcion": "Administración de existencias y alertas de inventario"
            },
            {
                "icono": "📋",
                "titulo": "Reportes",
                "descripcion": "Métricas y reportes del inventario en tiempo real"
            }
        ]
    }
   
    # Renderizar template con los datos
    return templates.TemplateResponse("home.html", context)