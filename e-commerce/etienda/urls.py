from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .api import api

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("buscar", views.busqueda, name="busqueda"),
    path('buscar_categoria/<str:categoria>', views.categoria, name='categoria'),
    path('addproduct', views.addproduct, name='addproduct'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

