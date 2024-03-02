from html.entities import html5
from multiprocessing import context
from re import search
from django.shortcuts import render
from . import forms
import logging
import os
from django.contrib import messages
from django.contrib.auth.decorators import login_required
logger = logging.getLogger(__name__)

# Create your views here.

from django.http import HttpResponse

from . import models


def index(request):
    context = {'productos' : models.ObtenerProductos(), 'categorias' : models.ObtenerCategorias()}
    return render(request, 'etienda/index.html', context)

def busqueda(request):
    context = {'productos' : models.ObtenerBusqueda(request.GET.get('input_busqueda', '')), 'categorias' : models.ObtenerCategorias()}
    return render(request, 'etienda/busqueda.html', context)

def categoria(request, categoria):
    context = {'productos' : models.ObtenerProductosCategoria(categoria), 'categorias' : models.ObtenerCategorias()}
    return render(request, 'etienda/categorias.html', context)

@login_required
def addproduct(request):
    form = forms.ProductForm()
    if request.method == "POST":
    # Rellena automáticamente todos los campos
        form = forms.ProductForm(request.POST, request.FILES)
    # valida o si no añade errores a form
        if form.is_valid():
            producto = { 'title' : form.cleaned_data['title'], 'price' : form.cleaned_data['price'], 'category' : form.cleaned_data['category'], 'description' : form.cleaned_data['description'], 'image' : form.cleaned_data['image']}
            # Copiamos el archivo a la carpeta de imagenes
            image_path = form.cleaned_data['image'].name
            destination1 = os.path.join('imagenes', image_path)
            with open(destination1, 'wb') as destination_file:
                for chunk in form.cleaned_data['image'].chunks():
                    destination_file.write(chunk)
            destination2 = os.path.join('static/imagenes', image_path)
            with open(destination2, 'wb') as destination_file:
                for chunk in form.cleaned_data['image'].chunks():
                    destination_file.write(chunk)
            producto['image'] = destination1
            logger.info("Añadiendo producto: %s", producto)

            models.AnadirProducto(producto)
            logger.info("Producto añadido: %s", producto)
            messages.success(request, 'Producto añadido correctamente')

            context = {'form' : forms.ProductForm(), 'categorias' : models.ObtenerCategorias()}
            return render (request, 'etienda/addproduct.html', context)
        else:
            logger.error('Error añadiendo producto')
            messages.error(request, 'Error añadiendo producto')
            context = {'form' : form, 'categorias' : models.ObtenerCategorias()}
            return render(request, 'etienda/addproduct.html', context)
    # cuando GET o cuando no valida y rellena errores
    context = {'form' : forms.ProductForm(), 'categorias' : models.ObtenerCategorias()}
    return render(request, 'etienda/addproduct.html', context)