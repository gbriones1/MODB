from django import forms
from django.utils.encoding import (
    force_str, force_text, python_2_unicode_compatible,
)
from django.utils.html import conditional_escape, format_html
from models import Product, Tool, Provider, Appliance, Classification, Brand, Lending, Input_Product, Output_Product, Lending_Product, Configuration

from datetime import datetime

class DateInput(forms.DateInput):
    input_type = 'date'

class ProductSelect(forms.widgets.Select):
    def render_option(self, selected_choices, option_value, option_label):
        if option_value is None:
            option_value = ''
        option_value = force_text(option_value)
        if option_value in selected_choices:
            selected_html = mark_safe(' selected="selected"')
            if not self.allow_multiple_selected:
                # Only allow for a single selection.
                selected_choices.remove(option_value)
        else:
            selected_html = ''
        return format_html('<option value="{}" provider="{}" {}>{}</option>',
                           option_value,
                           self.choices.queryset.get(code=option_value).provider.id,
                           selected_html,
                           force_text(option_label))


class ProductForm(forms.ModelForm):
    code = forms.CharField(max_length=30, label='Codigo')
    brand = forms.ModelChoiceField(queryset=Brand.objects.all(), required=False, label="Marca")
    provider = forms.ModelChoiceField(queryset=Provider.objects.all(), required=False, label="Proveedor")
    name = forms.CharField(max_length=200, label='Nombre')
    description = forms.CharField(max_length=255, label='Descripcion', required=False)
    appliance = forms.ModelMultipleChoiceField(queryset=Appliance.objects.all(), required=False, label="Aplicacion")
    price = forms.DecimalField(max_digits=9, decimal_places=2, label='Precio de lista', required=True, min_value=0, initial=0)
    discount = forms.IntegerField(label='Descuento', initial=0, min_value=0, max_value=100)
    real_price = forms.DecimalField(max_digits=9, decimal_places=2, label='Precio real', required=False, initial=0, min_value=0, widget=forms.widgets.NumberInput(attrs={'disabled':'disabled'}))
    classification = forms.ModelChoiceField(queryset=Classification.objects.all(), required=False, label="Porcentaje")
    in_used = forms.IntegerField(label='Obsoletas', initial=0, min_value=0)
    used_tobe = forms.IntegerField(label='Stock obsoletas', initial=0, min_value=0)
    in_stock = forms.IntegerField(label='Propias', initial=0, min_value=0)
    stock_tobe = forms.IntegerField(label='Stock propias', initial=0, min_value=0)
    in_consignment = forms.IntegerField(label='Consignacion', initial=0, min_value=0)
    consignment_tobe = forms.IntegerField(label='Stock consignacion', initial=0, min_value=0)

    class Meta:
        model = Product
        # fields = "__all__"
        fields = [
            "code",
            "brand",
            "provider",
            "name",
            "description",
            "appliance",
            "price",
            "discount",
            "real_price",
            "classification",
            "in_used",
            "used_tobe",
            "in_stock",
            "stock_tobe",
            "in_consignment",
            "consignment_tobe",
            ] 

class ToolForm(forms.ModelForm):
    code = forms.CharField(max_length=30, label='Codigo')
    name = forms.CharField(max_length=200, label='Nombre')
    description = forms.CharField(max_length=255, label='Descripcion', required=False)
    condition = forms.CharField(max_length=255, label='Condicion', required=False)
    amount = forms.IntegerField(initial=0, label='Cantidad', required=True)

    class Meta:
        model = Tool
        fields = "__all__" 

class ProductInputForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput(), label='Fecha', initial=datetime.now())
    filter_search = forms.CharField(max_length=100, label='Buscar producto')
    product = forms.ModelMultipleChoiceField(queryset=Product.objects.all(), required=False, label="Seleccionar productos", widget=ProductSelect(attrs={"size":"10"}))
    amount = forms.IntegerField(label='Cantidad', initial=1)
    price = forms.DecimalField(max_digits=9, decimal_places=2, label='Precio de lista', initial=0)
    storage = forms.ChoiceField(label='Almacen', choices=Product.STORAGE_CHOICES)
    provider = forms.ModelChoiceField(queryset=Provider.objects.all(), required=False, label="Proveedor")

    class Meta:
        model = Input_Product
        fields = ['date', 'storage', 'provider', 'filter_search', 'product', 'amount', 'price']

class ProductOutputForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput(), label='Fecha', initial=datetime.now())
    filter_search = forms.CharField(max_length=100, label='Buscar producto')
    product_consignment = forms.ModelMultipleChoiceField(queryset=Product.objects.filter(in_consignment__gt=0), required=False, label="Seleccionar productos", widget=ProductSelect(attrs={"size":"10"}))
    product_stock = forms.ModelMultipleChoiceField(queryset=Product.objects.filter(in_stock__gt=0), required=False, label="Seleccionar productos", widget=ProductSelect(attrs={"size":"10"}))
    product_used = forms.ModelMultipleChoiceField(queryset=Product.objects.filter(in_used__gt=0), required=False, label="Seleccionar productos", widget=ProductSelect(attrs={"size":"10"}))
    amount = forms.IntegerField(label='Cantidad', initial=1)
    storage = forms.ChoiceField(label='Almacen', choices=Product.STORAGE_CHOICES)
    provider = forms.ModelChoiceField(queryset=Provider.objects.all(), required=False, label="Proveedor")

    class Meta:
        model = Output_Product
        fields = ['date', 'storage', 'provider', 'filter_search', 'product_consignment', 'product_stock', 'product_used', 'amount']

class ProductLendingForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput(), label='Fecha', initial=datetime.now())
    employee = forms.CharField(max_length=100, label='Empleado')
    destination = forms.CharField(max_length=100, label='Destino')
    filter_search = forms.CharField(max_length=100, label='Buscar producto')
    product_consignment = forms.ModelMultipleChoiceField(queryset=Product.objects.filter(in_consignment__gt=0), required=False, label="Seleccionar productos", widget=ProductSelect(attrs={"size":"10"}))
    product_stock = forms.ModelMultipleChoiceField(queryset=Product.objects.filter(in_stock__gt=0), required=False, label="Seleccionar productos", widget=ProductSelect(attrs={"size":"10"}))
    product_used = forms.ModelMultipleChoiceField(queryset=Product.objects.filter(in_used__gt=0), required=False, label="Seleccionar productos", widget=ProductSelect(attrs={"size":"10"}))
    amount = forms.IntegerField(label='Cantidad', initial=1)
    storage = forms.ChoiceField(label='Almacen', choices=Product.STORAGE_CHOICES)
    provider = forms.ModelChoiceField(queryset=Provider.objects.all(), required=False, label="Proveedor")

    class Meta:
        model = Lending
        fields = ['date', 'employee', 'destination', 'storage', 'provider', 'filter_search', 'product_consignment', 'product_stock', 'product_used', 'amount']

class ToolLendingForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput(), label='Fecha', initial=datetime.now())
    employee = forms.CharField(max_length=100, label='Empleado')
    destination = forms.CharField(max_length=100, label='Destino')
    tool_filter_search = forms.CharField(max_length=100, label='Buscar herramienta')
    tool = forms.ModelMultipleChoiceField(queryset=Tool.objects.all(), required=False, label="Seleccionar herramienta", widget=forms.widgets.Select(attrs={"size":"10"}))
    amount = forms.IntegerField(label='Cantidad', initial=1)

    class Meta:
        model = Lending
        fields = ['date', 'employee', 'destination', 'tool_filter_search', 'tool', 'amount']

class ProviderForm(forms.ModelForm):
    name = forms.CharField(max_length=100, label='Nombre')

    class Meta:
        model = Provider
        fields = "__all__"

class UpdateProviderForm(forms.ModelForm):
    id = forms.IntegerField(widget = forms.HiddenInput)
    name = forms.CharField(max_length=100, label='Nombre')

    class Meta:
        model = Provider
        fields = "__all__"

class BrandForm(forms.ModelForm):
    name = forms.CharField(max_length=100, label='Nombre')

    class Meta:
        model = Brand
        fields = "__all__"

class UpdateBrandForm(forms.ModelForm):
    id = forms.IntegerField(widget = forms.HiddenInput)
    name = forms.CharField(max_length=100, label='Nombre')

    class Meta:
        model = Brand
        fields = "__all__" 

class ApplianceForm(forms.ModelForm):
    name = forms.CharField(max_length=100, label='Nombre')

    class Meta:
        model = Appliance
        fields = "__all__"

class UpdateApplianceForm(forms.ModelForm):
    id = forms.IntegerField(widget = forms.HiddenInput)
    name = forms.CharField(max_length=100, label='Nombre')

    class Meta:
        model = Appliance
        fields = "__all__"

class ClassificationForm(forms.ModelForm):
    name = forms.CharField(max_length=100, label='Nombre')

    class Meta:
        model = Classification
        fields = "__all__"

class UpdateClassificationForm(forms.ModelForm):
    id = forms.IntegerField(widget = forms.HiddenInput)
    name = forms.CharField(max_length=100, label='Nombre')

    class Meta:
        model = Classification
        fields = "__all__" 

class ConfigurationForm(forms.ModelForm):
    sender_email = forms.EmailField(label="Email para ordenes", required=False)
    password = forms.CharField(widget=forms.PasswordInput(render_value=True), required=False, label="Password")
    receiver_email = forms.EmailField(label="Email para notificaciones", required=False)
    mailOnPriceChange = forms.BooleanField(label="Enviar correo al cambiar el precio de un producto", required=False)
    mailOnNegativeValues = forms.BooleanField(label="Enviar correo por llegar a valores negativos", required=False)

    class Meta:
        model = Configuration
        fields = "__all__" 

class OrderInputForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput(), label='Fecha', initial=datetime.now())
    storage = forms.ChoiceField(label='Almacen', choices=Product.STORAGE_CHOICES)

    class Meta:
        model = Input_Product
        fields = ['date', 'storage']