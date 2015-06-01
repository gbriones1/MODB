from django.contrib import admin
from django.db import models

class Appliance(models.Model):
    name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name

class Provider(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    def __unicode__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name

class Classification(models.Model):
    name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name

class Tool(models.Model):
    code = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=255, null=True, blank=True)
    condition = models.CharField(max_length=255, null=True, blank=True)
    amount = models.IntegerField()

    def __unicode__(self):
        return self.code+" - "+self.name+" - "+self.description

class Product(models.Model):
    STORAGE_CHOICES = (
        ('C', 'Consignacion'),
        ('S', 'Propias'),
        ('U', 'Obsoletas'),
    )
    code = models.CharField(max_length=30, primary_key=True)
    brand = models.ForeignKey(Brand, null=True, blank=True)
    provider = models.ForeignKey(Provider, null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=255, null=True, blank=True)
    appliance = models.ManyToManyField(Appliance, null=True, blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    discount = models.DecimalField(max_digits=9, decimal_places=2)
    classification = models.ForeignKey(Classification, null=True, blank=True)
    in_used = models.IntegerField()
    in_stock = models.IntegerField()
    in_consignment = models.IntegerField()
    stock_tobe =models.IntegerField()
    consignment_tobe =models.IntegerField()

    def __unicode__(self):
        return self.code+" - "+self.name+" - "+self.description

class Input(models.Model):
    date = models.DateTimeField()
    storage = models.CharField(max_length=1, choices=Product.STORAGE_CHOICES)

    def __init__(self, *args, **kwargs):
        super(Input, self).__init__(*args, **kwargs)
        self.type = "Input"

class Output(models.Model):
    date = models.DateTimeField()
    employee = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    storage = models.CharField(max_length=1, choices=Product.STORAGE_CHOICES)

    def __init__(self, *args, **kwargs):
        super(Output, self).__init__(*args, **kwargs)
        self.type = "Output"

class Input_Product(models.Model):
    input_reg = models.ForeignKey(Input)
    product = models.ForeignKey(Product)
    amount = models.IntegerField()
    price = models.DecimalField(max_digits=9, decimal_places=2)

class Output_Product(models.Model):
    output_reg = models.ForeignKey(Output)
    product = models.ForeignKey(Product)
    amount = models.IntegerField()
    price = models.DecimalField(max_digits=9, decimal_places=2)

class Lending(models.Model):
    date = models.DateTimeField()
    employee = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    storage = models.CharField(max_length=1, choices=Product.STORAGE_CHOICES)
    returned = models.BooleanField(default=False)
    returned_date = models.DateTimeField(null=True)

    def __init__(self, *args, **kwargs):
        super(Lending, self).__init__(*args, **kwargs)
        self.type = "Lending"

class Lending_Product(models.Model):
    lending = models.ForeignKey(Lending)
    product = models.ForeignKey(Product)
    amount = models.IntegerField()
    returned_amount = models.IntegerField()

class Lending_Tool(models.Model):
    lending = models.ForeignKey(Lending)
    tool = models.ForeignKey(Tool)
    amount = models.IntegerField()
    returned_amount = models.IntegerField()

class Order(models.Model):
    STATUS_PENDING = 'P'
    STATUS_ASKED = 'A'
    STATUS_CANCELED = 'C'
    STATUS_RECEIVED = 'R'
    STATUS_CHOICES = (
        (STATUS_PENDING, 'Por pedir'),
        (STATUS_ASKED, 'Pedido'),
        (STATUS_CANCELED, 'Cancelado'),
        (STATUS_RECEIVED, 'Recibido'),
    )
    date = models.DateTimeField(auto_now_add=True)
    provider = models.ForeignKey(Provider)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    received_date = models.DateTimeField(null=True)

class Order_Product(models.Model):
    order = models.ForeignKey(Order)
    product = models.ForeignKey(Product)
    amount = models.IntegerField()

class Configuration(models.Model):
    sender_email = models.EmailField(null=True)
    password = models.CharField(max_length=30, null=True)
    receiver_email = models.EmailField(null=True)
    mailOnPriceChange = models.BooleanField(default=True)
    mailOnNegativeValues = models.BooleanField(default=True)
    # destination del sistema para enviar un correo de adgoritmo para mi hermoso amorcito te amo te amo :*
    # la longitud de mi inteligencia va a ayudar a mi papito clo voy a ayudar siempre 
    
class ProductAdmin(admin.ModelAdmin):
    pass

class InputProductAdmin(admin.ModelAdmin):
    pass

class InputAdmin(admin.ModelAdmin):
    pass

admin.site.register(Product, ProductAdmin)
admin.site.register(Input_Product, InputProductAdmin)
admin.site.register(Input, InputAdmin)