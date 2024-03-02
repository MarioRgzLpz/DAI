from django.db import models
from pymongo import MongoClient
from pydantic import BaseModel, FilePath, Field
from bson.objectid import ObjectId
from typing import Any
from ninja import Schema

# Create your models here.

client = MongoClient('mongo', 27017)

tienda_db = client.tienda                   # Base de Datos
productos_collection = tienda_db.productos  # Colección productos
compras_collection = tienda_db.compras      # Colección compras

class Rating(BaseModel):
	rate: float = Field(ge=0., lt=5.)
	count: int = Field(ge=1)

class Producto(Schema):
    id: Any
    title: str
    price: float
    description: str
    category: str
    image: FilePath | None

    #@field_validator('title')
    @classmethod
    def title_mayuscula(cls,v):
        if v[0].islower():
            raise ValueError('El título debe empezar por mayúscula')
        return v.title()

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

def getProduct(idproducto):
    consulta = { 'id': idproducto }
    resultado = productos_collection.find_one(consulta)
    return resultado

def ObtenerOfertas():
    resultado = productos_collection.find()
    return resultado    
        
def ObtenerCategorias():
    categorias = []
    for record in productos_collection.find():     
        cat = record.get("category")
        if cat not in categorias:
            categorias.append(cat)
    return categorias

def ObtenerBusqueda(busqueda):
    consulta = { 'title': {"$regex" : busqueda, '$options': 'i'}}
    resultado = productos_collection.find(consulta)
    resultado = list(resultado)
    for r in resultado:
        r["id"] = str(r.get("_id"))
        del r["_id"]
    return resultado

def ObtenerProductosCategoria(categoria):
    consulta = { 'category': categoria}
    resultado = productos_collection.find(consulta)
    resultado = list(resultado)
    for r in resultado:
        r["id"] = str(r.get("_id"))
        del r["_id"]
    return resultado

def ObtenerProductos():
    resultado = productos_collection.find()
    resultado = list(resultado)
    for r in resultado:
        r["id"] = str(r.get("_id"))
        del r["_id"]
    return resultado

def ObtenerProductosId(id):
    resultado = productos_collection.find({"_id": ObjectId(id)})
    resultado = list(resultado)
    for r in resultado:
        r["id"] = str(r.get("_id"))
        del r["_id"]
    return resultado


def handle_uploaded_file(f):
    directorio_destino = "static/imagenes/" 
    directorio_imagenes = "imagenes/"
    nombre_archivo = f.name.split('/')[-1]
    nombre_archivo_destino = directorio_imagenes+nombre_archivo
    ruta_archivo_destino = directorio_destino+nombre_archivo
    with open(ruta_archivo_destino,"wb") as archivo:
        archivo.write(f.read())
    with open(nombre_archivo_destino,"wb") as archivo:
        archivo.write(f.read())
    return nombre_archivo_destino
    
def CrearProducto(title, price, description, category, image):
    image = handle_uploaded_file(image)
    producto = {"title": title, "price": price, "description": description, "category": category, "image": image, "rating": {"count": 0, "rate": 0}}
    insertado = productos_collection.insert_one(producto)
    resultado = productos_collection.find({"_id": insertado.inserted_id})
    resultado = list(resultado)
    for r in resultado:
        r["id"] = str(r.get("_id"))
        del r["_id"]
    return resultado

def ModificarProducto(idproducto, atributo, valor):
    productos_collection.update_one({"_id": ObjectId(idproducto)}, {'$set': {atributo: valor}})

def EliminarProducto(idproducto):
    productos_collection.delete_one({"_id": ObjectId(id)})

def ModificarRating(id, rate):
    product = productos_collection.find_one({"_id": ObjectId(id)})
    if product:
        new_rating = Rating(**product["rating"])
        new_count = new_rating.count + 1
        new_rate = ((new_rating.rate * new_rating.count) + (rate * 1.0)) / new_count
        productos_collection.update_one({"_id": ObjectId(id)}, {"$set": {"rating": {"count": new_count, "rate": new_rate}}})
        return ObtenerProductosId(id)


def consulta2():
    consulta = { 'description': {"$regex" : "pocket"}}
    resultado1 = productos_collection.find(consulta)
    resultado = " ".join([str(x) for x in resultado1])
    return resultado

def consulta3():
    consulta = { 'rating.rate': {"$gt" : 4} }
    resultado1 = productos_collection.find(consulta)
    resultado = " ".join([str(x) for x in resultado1])
    return resultado

def consulta4():
    consulta = { 'category': "men's clothing"}
    resultado1 = productos_collection.find(consulta).sort('rating.rate')
    resultado = " ".join([str(x) for x in resultado1])
    return resultado

def consulta5():

    facturacion_total= 0

    for compra in compras_collection.find():
        productoscompra = compra.get("products")
        for producto in productoscompra:
            facturacion_total += getPrice(producto.get("productId")) * producto.get("quantity")

    return str(facturacion_total)

def consulta6():
    categorias = []
    facturaciones = []
    resultado= []

    for record in productos_collection.find():
         cat=record.get("category")
         if cat not in categorias:
             categorias.append(cat)

    for categoria in categorias:
         facturacion_categoria = 0
         for compra in compras_collection.find():
             productoscompra = compra.get("products")
             for producto in productoscompra:
                 if categoria == getCategoria(producto.get("productId")):
                     facturacion_categoria += getPrice(producto.get("productId")) * producto.get("quantity")
         facturaciones.append([categoria,facturacion_categoria])

    resultado = " ".join([str(x) for x in facturaciones])
    return resultado
