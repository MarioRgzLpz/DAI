from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import logging

logger = logging.getLogger(__name__)

def title_in_mayus_validator(value):
    if value[0].islower():
        logger.error('El título de un producto a insertar debe empezar por mayúscula')
        raise ValidationError(
            _("%(value)s debe empezar con mayúscula"),
            params={"value": value},
        )
    
class ProductForm(forms.Form):
	title = forms.CharField(label='Title', max_length=100, validators=[title_in_mayus_validator]) 
	category = forms.CharField(label='Category', max_length=100)
	description = forms.CharField(label='Description', max_length=1000)
	price = forms.FloatField(label='Price')   
	image = forms.FileField(label='Image')
