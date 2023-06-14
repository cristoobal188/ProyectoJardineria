from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column,Div
from django.forms import ModelForm
from .models import *

class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = ('nombre', 'stock', 'precio', 'tipo', 'fechagregado', 'fechamodificado', 'foto')
        widgets = {'fechagregado': forms.SelectDateWidget(years=range(2023, 2040))}
        widgets = {'fechamodificado': forms.SelectDateWidget(years=range(2023, 2040))}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Div(
                Row(
                    Div('nombre', css_class='form-group col-md-6 mb-10 mt-10'),
                    Div('stock', css_class='form-group col-md-6 mb-10 mt-10'),
                    css_class='form-row'
                ),
                Row(
                    Div('precio', css_class='form-group col-md-6 mb-10 mt-10'),
                    Div('tipo', css_class='form-group col-md-6 mb-10 mt-10'),
                    css_class='form-row'
                ),
                Row(
                    Div('fechagregado', css_class='form-group col-md-6 mb-10 mt-10'),
                    Div('fechamodificado', css_class='form-group col-md-6 mb-10 mt-10'),
                    css_class='form-row'
                ),
                css_class='form-group'
            ),
            Submit('submit', 'Guardar')
        )


class SuscriptorForm(ModelForm):
    class Meta:
        model = Suscriptores
        fields = ('nombrecompleto', 'apellidos', 'correo', 'numerotelefono', 'contraseña', 'confirmarcontraseña')

        widgets = {'fechavencimiento': forms.SelectDateWidget(years=range(2023, 2027))}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('nombrecompleto', css_class='form-group col-md-4 mb-0'),
                Column('apellidos', css_class='form-group col-md-4 mb-0'),
                Column('correo', css_class='form-group col-md-4 mb-0'),
                Column('numerotelefono', css_class='form-group col-md-4 mb-0'),
                Column('contraseña', css_class='form-group col-md-4 mb-0'),
                Column('confirmarcontraseña', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Guardar')
        )
