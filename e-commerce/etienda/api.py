from ninja_extra import NinjaExtraAPI, api_controller, http_get
from ninja.security import django_auth,HttpBearer
import logging
from . import models
from ninja import Schema, Query, Form, File
from ninja.files import UploadedFile

		
class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        if token == "supersecret":
            return token

#api = NinjaExtraAPI(auth=GlobalAuth())
	
api = NinjaExtraAPI()
logger = logging.getLogger(__name__)

class Rate(Schema):
	rate: float
	count: int
	
class ProductSchema(Schema):  # sirve para validar y para documentación
	id:    str
	title: str
	price: float
	description: str
	category: str
	image: str = None
	rating: Rate
	
	
class ProductSchemaIn(Schema):
	title: str
	price: float
	description: str
	category: str
	rating: Rate
	
	
class ErrorSchema(Schema):
	message: str
	

@api.get("/products", tags=['TIENDA DAI'], response = {202: list[ProductSchema], 404: ErrorSchema})
def Lista_producto(request, desde: int , hasta: int):
	try:
		data = models.ObtenerProductos()[desde:hasta]
		return 202, data
	except:
		return 404, {'message': 'productos no encontrados'}
	
@api.post("/products", tags=['TIENDA DAI'], response = {202: list[ProductSchema], 404: ErrorSchema})
def Añade_producto(request, title: str = Form(...), price: float = Form(...), description: str = Form(...), category: str = Form(...), image: UploadedFile = File(...)):
	try:
		data = models.CrearProducto(title, price, description, category, image)
		return 202, list(data)
	except:
		return 404, {'message': 'error añadiendo producto'}
	
@api.get("/products/{id}", tags=['TIENDA DAI'], response = {202: list[ProductSchema], 404: ErrorSchema})
def Lista_producto_id(request, id: str):
	try:
		data = models.ObtenerProductosId(id)
		return 202, list(data)
	except:
		return 404, {'message': 'producto no encontrado'}

@api.put("/products/{id}", tags=['TIENDA DAI'], response = {202: list[ProductSchema], 404: ErrorSchema})
def Modifica_producto(request, id: str, payload: ProductSchemaIn ):
	try:
		for attr, value in payload.dict().items():
			logger.debug(f'{attr} -> {value}')
			models.ModificarProducto(id, attr, value)
		resultado = models.ObtenerProductosId(id)
		logger.debug(f'{payload}')
		return 202, list(resultado)
	except:
		return 404, {'message': 'error modificando producto'}
	
@api.delete("/products/{id}", tags=['TIENDA DAI'], response = {204: None, 404: ErrorSchema})
def Elimina_producto(request, id: str):
	try:
		models.EliminarProducto(id)
		return 204, {'message': 'producto eliminado'}
	except:
		return 404, {'message': 'error eliminando producto'}
	
@api.put('/products/{id}/{rating}', tags=['TIENDA DAI'], response={202 : list[ProductSchema], 404 : ErrorSchema})
def ModificarRating(request, id : str, rating : int):
	try:
		resultado = models.ModificarRating(id, rating)
		return 202, list(resultado)
	except:
		return 404, {"message": "No se ha encontrado el producto"}
	

@api.get("/bearer",tags=['TIENDA DAI'], auth=GlobalAuth())
def bearer(request):
    return {"token": request.auth}