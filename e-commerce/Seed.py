# Seed.py
from pydantic import BaseModel, FilePath, Field, EmailStr #field_validator
from pymongo import MongoClient
from pprint import pprint
from datetime import datetime
from typing import Any
import requests
import os

		
# https://requests.readthedocs.io/en/latest/
def getProductos(api):
	response = requests.get(api)
	return response.json()

# Funcion que pasando como argumento el id de un producto obtiene su precio
def getPrice(idproducto):
	consulta = { 'id': idproducto }
	proyeccion = {"price": 1}
	resultado = productos_collection.find_one(consulta, proyeccion)
	precio = resultado.get("price")
	return precio

def getCategoria(idproducto):
	consulta = { 'id': idproducto }
	proyeccion = {"category": 1}
	resultado = productos_collection.find_one(consulta, proyeccion)
	categoria = resultado.get("category")
	return categoria
				
# Esquema de la BD
# https://docs.pydantic.dev/latest/
# con anotaciones de tipo https://docs.python.org/3/library/typing.html
# https://docs.pydantic.dev/latest/usage/fields/

class Rating(BaseModel):
    rate: float = Field(ge=0., lt=5.)
    count: int = Field(ge=1)
                
class Producto(BaseModel):
    #_id: Any
    title: str
    price: float
    description: str
    category: str
    image: FilePath | None
    rating: Rating

    #@field_validator('title')
    @classmethod
    def title_mayuscula(cls,v):
        if v[0].islower():
            raise ValueError('El título debe empezar por mayúscula')
        return v.title()

class Compra(BaseModel):
    _id: Any
    userId: int
    date: datetime
    products: list




# Conexión con la BD				
# https://pymongo.readthedocs.io/en/stable/tutorial.html
client = MongoClient('mongo', 27017)

tienda_db = client.tienda                   # Base de Datos
productos_collection = tienda_db.productos  # Colección  
	

# añade a BD
compras_collection = tienda_db.compras  # Colección
	


productos = getProductos('https://fakestoreapi.com/products')
productos_collection.drop()

for p in productos:
	url = p.get("image")
	directorio_destino = "imagenes/"
	nombre_archivo = os.path.basename(url)
	path = os.path.join(directorio_destino, nombre_archivo)
	response = requests.get(url)
	with open(path, "wb") as archivo:
		archivo.write(response.content)
	p['image'] = path
	p.pop('id')

	Producto(**p)

	productos_collection.insert_one(p)


compras = getProductos('https://fakestoreapi.com/carts')
compras_collection.drop()

for c in compras:
	Compra(**c)
compras_collection.insert_many(compras)

print("------------------------------------------------------------------------------")

consulta = { 'category': 'electronics' , 'price' : {"$lte" : 200, "$gte" : 100 }}
resultado = productos_collection.find(consulta).sort('price',1)
for p in resultado:
	pprint(p)

print("------------------------------------------------------------------------------")

consulta = { 'description': {"$regex" : "pocket"}}
resultado = productos_collection.find(consulta)
for p in resultado:
	pprint(p)

print("------------------------------------------------------------------------------")

consulta = { 'rating.rate': {"$gt" : 4} }
resultado = productos_collection.find(consulta)
for p in resultado:
	pprint(p)

print("------------------------------------------------------------------------------")

consulta = { 'category': "men's clothing"}
resultado = productos_collection.find(consulta).sort('rating.rate')
for p in resultado:
	pprint(p)


print("------------------------------------------------------------------------------")

""" facturacion_total= 0

for compra in compras_collection.find():
	productoscompra = compra.get("products")
	for producto in productoscompra:
		facturacion_total += getPrice(producto.get("productId")) * producto.get("quantity")

print(facturacion_total) """

print("------------------------------------------------------------------------------")


""" categorias= []

for record in productos_collection.find():
	cat=record.get("category")
	if cat not in categorias:
		categorias.append(cat)

for categoria in categorias:
	print('\n  ' + categoria)
	facturacion_categoria = 0
	for compra in compras_collection.find():
		productoscompra = compra.get("products")
		for producto in productoscompra:
			if categoria == getCategoria(producto.get("productId")):
				facturacion_categoria += getPrice(producto.get("productId")) * producto.get("quantity")
	print( facturacion_categoria) """
