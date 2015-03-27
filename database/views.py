from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from database.models import Product, Input, Output, Lending, Input_Product, Output_Product, Lending_Product, Provider, Appliance, Classification, Brand, Order, Configuration, Order_Product
from database.forms import ProductForm, ProductInputForm, ProductOutputForm, ProductLendingForm, ProviderForm, ApplianceForm, BrandForm, ClassificationForm, UpdateProviderForm, UpdateBrandForm, UpdateApplianceForm, UpdateClassificationForm, ConfigurationForm
from lib.email_client import send_email
from datetime import datetime
import json, operator
import pdb

def get_messages(request):
    clean_messages = request.session.get('clean_messages', False)
    if clean_messages:
        request.session['messages'] = []
        request.session['clean_messages'] = False
    messages = request.session.get('messages', [])
    if messages:
        request.session["clean_messages"] = True
    return messages

def set_messages(request, messages):
    request.session['clean_messages'] = False
    request.session["messages"] = messages

def add_message(request, message):
    clean_messages = request.session.get('clean_messages', False)
    if clean_messages:
        request.session['messages'] = []
        request.session['clean_messages'] = False
    messages = request.session.get('messages', [])
    if messages:
        request.session['messages'].append(message)
    else:
        request.session['messages'] = [message]

def createOrder(provider, products, subject, message, request):
    if provider.email:
        for product in products:
            message += "\n"+product.code+" - "+product.name+" "+product.description+". Cantidad: "+request.POST.get(product.code, "0")
        if send_email(provider.email, subject, message):
            order = Order(provider=provider, status=Order.STATUS_ASKED)
            order.save()
            for product in products:
                product_order = Order_Product(product=product, amount=int(request.POST.get(product.code, "0")), order=order)
                product_order.save()
        else:
            add_message(request, ("Email no valido. Orden no enviada", "warning"))
    else:
        add_message(request, ("Proveedor: "+provider.name+" sin email. Orden no enviada", "warning"))

### DASHBOARD VIEW ###

@login_required
def dashboard(request):
    dashboard_active = "active"
    filter_active = {}
    products = Product.objects.all()
    providers = Provider.objects.all()
    brands = Brand.objects.all()
    classifications = Classification.objects.all()
    if request.method == "POST":
        redirect_url = "/"
        action = request.POST.get('action', '')
        if action == "CREATE":
            form = ProductForm(request.POST)
            if form.is_valid():
                form.save()
            else:
                set_messages(request, [("Producto no creado, los datos no fueron validos", "danger")])
        elif action == "UPDATE":
            product = Product.objects.get(code=request.POST['code'])
            form = ProductForm(request.POST, instance=product)
            if form.is_valid():
                form.save()
            else:
                set_messages(request, [("Producto no actualizado, los nuevos datos no son validos", "danger")])
        elif action == "DELETE":
            for product in Product.objects.filter(code__in=json.loads(str(request.POST.get('code',"[]")))):
                product.delete()
        # elif action == "INPUT":
        #     product_amount = json.loads(request.POST.get("inputProducts", "{}"))
        #     storage = request.POST.get("storage", "")
        #     if product_amount and storage:
        #         new_input = Input(storage=storage)
        #         new_input.save()
        #         for productId, amount in product_amount.iteritems():
        #             product = Product.objects.get(code=productId)
        #             product_input = Input_Product(product=product, amount=amount, input_reg=new_input)
        #             if storage == "C":
        #                 product.in_consignment += int(amount)
        #             elif storage == "S":
        #                 product.in_stock += int(amount)
        #             elif storage == "U":
        #                 product.in_used += int(amount)
        #             product_input.save()
        #             product.save()
        #     else:
        #         set_messages(request, [("Entrada no autorizada, los datos no fueron validos", "danger")])
        # elif action == "OUTPUT":
        #     product_amount = json.loads(request.POST.get("outputProducts", "{}"))
        #     storage = request.POST.get("storage", "")
        #     if product_amount and storage:
        #         new_output = Output(storage=storage)
        #         new_output.save()
        #         for productId, amount in product_amount.iteritems():
        #             product = Product.objects.get(code=productId)
        #             product_output = Output_Product(product=product, amount=amount, output_reg=new_output)
        #             if storage == "C":
        #                 product.in_consignment -= int(amount)
        #             elif storage == "S":
        #                 product.in_stock -= int(amount)
        #             elif storage == "U":
        #                 product.in_used -= int(amount)
        #             product_output.save()
        #             product.save()
        #     else:
        #         set_messages(request, [("Salida no autorizada, los datos no fueron validos", "danger")])
        # elif action == "LENDING":
        #     product_amount = json.loads(request.POST.get("lendingProducts", "{}"))
        #     storage = request.POST.get("storage", "")
        #     employee = request.POST.get("employee", "")
        #     destination = request.POST.get("destination", "")
        #     if product_amount and storage and employee and destination:
        #         lending = Lending(storage=storage, employee=employee, destination=destination)
        #         lending.save()
        #         for productId, amount in product_amount.iteritems():
        #             product = Product.objects.get(code=productId)
        #             product_lending = Lending_Product(product=product, amount=amount, lending=lending)
        #             if storage == "C":
        #                 product.in_consignment -= int(amount)
        #             elif storage == "S":
        #                 product.in_stock -= int(amount)
        #             elif storage == "U":
        #                 product.in_used -= int(amount)
        #             product_lending.save()
        #             product.save()
        #     else:
        #         set_messages(request, [("Prestamo no autorizado, los datos no fueron validos", "danger")])
        return HttpResponseRedirect("/?storage="+request.POST.get('storage', ''))
    form = ProductForm()
    storage = request.GET.get("storage", '')
    if storage == "C":
        products = products.filter(in_consignment__gt=0)
        filter_active["C"] = "active"
    elif storage == "S":
        products = products.filter(in_stock__gt=0)
        filter_active["S"] = "active"
    elif storage == "U":
        products = products.filter(in_used__gt=0)
        filter_active["U"] = "active"
    else:
        filter_active["all"] = "active"
    sort = request.GET.get("sort", '')
    order = request.GET.get("order", '')
    if sort:
        if order == 'desc':
            sort = "-"+sort
        products = products.order_by(sort)
    # product_forms = {p.code:ProductForm(instance=p) for p in products}
    scripts = ["product"]
    messages = get_messages(request)
    return render_to_response('pages/dashboard.html', locals(), context_instance=RequestContext(request))

@login_required
def lendings(request):
    dashboard_active = "active"
    lendings_active = "active"
    now = datetime.now()
    start_date = datetime.strptime(request.GET.get("start_date", now.replace(day=1).strftime("%Y-%m-%d")), "%Y-%m-%d").date()
    end_date = datetime.strptime(request.GET.get("end_date", now.strftime("%Y-%m-%d")), "%Y-%m-%d").date()
    formatted_start_date = start_date.strftime("%Y-%m-%d")
    formatted_end_date = end_date.strftime("%Y-%m-%d")
    lendings = Lending.objects.filter(date__gte=start_date, date__lte=end_date.replace(day=end_date.day+1)).order_by('-date')
    if request.method == "POST":
        action = request.POST.get('action', '')
        if action == "CREATE":
            product_amount = json.loads(request.POST.get("lendingProducts", "{}"))
            storage = request.POST.get("storage", "")
            employee = request.POST.get("employee", "")
            destination = request.POST.get("destination", "")
            date = datetime.strptime(request.POST.get("date", now.strftime("%Y-%m-%d")), "%Y-%m-%d").date()
            if product_amount and storage and employee and destination:
                lending = Lending(storage=storage, employee=employee, destination=destination, date=date)
                lending.save()
                for productId, amount in product_amount.iteritems():
                    product = Product.objects.get(code=productId)
                    product_lending = Lending_Product(product=product, amount=amount, lending=lending, returned_amount=0)
                    if storage == "C":
                        product.in_consignment -= int(amount)
                    elif storage == "S":
                        product.in_stock -= int(amount)
                    elif storage == "U":
                        product.in_used -= int(amount)
                    product_lending.save()
                    product.save()
            else:
                set_messages(request, [("Prestamo no autorizado, los datos no fueron validos", "danger")])
        elif action == "DELETE":
            rollback = request.POST.get('rollback', 'false')
            for delete_lending in Lending.objects.filter(id__in=json.loads(str(request.POST.get('lending_id', "[]")))):
                for product_lending in delete_lending.lending_product_set.all():
                    if rollback == "true":
                        product = product_lending.product
                        if delete_lending.storage == "C":
                            product.in_consignment += product_lending.amount-product_lending.returned_amount
                        elif delete_lending.storage == "S":
                            product.in_stock += product_lending.amount-product_lending.returned_amount
                        elif delete_lending.storage == "U":
                            product.in_used += product_lending.amount-product_lending.returned_amount
                        product.save()
                    product_lending.delete()
                delete_lending.delete()
        elif action == "RETURN":
            for return_lending in Lending.objects.filter(id__in=json.loads(str(request.POST.get('lending_id', "[]")))):
                for product_lending in return_lending.lending_product_set.all():
                    product = product_lending.product
                    product_lending.returned_amount = int(request.POST["amount"+product.code])
                    if return_lending.storage == "C":
                        product.in_consignment += product_lending.returned_amount
                    elif return_lending.storage == "S":
                        product.in_stock += product_lending.returned_amount
                    elif return_lending.storage == "U":
                        product.in_used += product_lending.returned_amount
                    product_lending.save()
                    product.save()
                return_lending.returned = True
                return_lending.returned_date = now
                return_lending.save()
        return HttpResponseRedirect('/lendings/')
    form = ProductLendingForm()
    scripts = ['productLending']
    messages = get_messages(request)
    return render_to_response('pages/dashboard.html', locals(), context_instance=RequestContext(request))

@login_required
def inputs(request):
    dashboard_active = "active"
    inputs_active = "active"
    now = datetime.now()
    start_date = datetime.strptime(request.GET.get("start_date", now.replace(day=1).strftime("%Y-%m-%d")), "%Y-%m-%d").date()
    end_date = datetime.strptime(request.GET.get("end_date", now.strftime("%Y-%m-%d")), "%Y-%m-%d").date()
    formatted_start_date = start_date.strftime("%Y-%m-%d")
    formatted_end_date = end_date.strftime("%Y-%m-%d")
    inputs = Input.objects.filter(date__gte=start_date, date__lte=end_date.replace(day=end_date.day+1)).order_by('-date')
    if request.method == "POST":
        action = request.POST.get('action', '')
        if action == "CREATE":
            product_amount = json.loads(request.POST.get("inputProducts", "{}"))
            storage = request.POST.get("storage", "")
            date = datetime.strptime(request.POST.get("date", now.strftime("%Y-%m-%d")), "%Y-%m-%d").date()
            if product_amount and storage:
                is_valid = True
                messages = []
                for productId, definition in product_amount.iteritems():
                    amount = definition["amount"]
                    price = float(definition["price"])
                    product = Product.objects.get(code=productId)
                    if product.price != price:
                        is_valid = False
                        messages.append(("El producto "+product.code+" - "+product.name+" a: $"+str(product.price)+" no coincide con el precio ingresado: $"+str(price), "danger"))
                if is_valid:
                    new_input = Input(storage=storage, date=date)
                    new_input.save()
                    for productId, definition in product_amount.iteritems():
                        product = Product.objects.get(code=productId)
                        product_input = Input_Product(product=product, amount=amount, price=product.price, input_reg=new_input)
                        if storage == "C":
                            product.in_consignment += int(amount)
                        elif storage == "S":
                            product.in_stock += int(amount)
                        elif storage == "U":
                            product.in_used += int(amount)
                        product_input.save()
                        product.save()
                else:
                    conf = Configuration.objects.all()[0]
                    if conf.mailOnPriceChange:
                        if not conf.receiver_email or not send_email(conf.receiver_email, "BDMO Entrada con precios erroneos", "Entrada no autorizada del "+str(now)+" por las siguientes razones:\n"+"\n".join([x[0] for x in messages])):
                            messages.append(("Correo de notificacion de precio diferente no enviado, correo no valido", "warning"))
                set_messages(request, messages)
            else:
                set_messages(request, [("Entrada no autorizada, los datos no fueron validos", "danger")])
        elif action == "DELETE":
            rollback = request.POST.get('rollback', 'false')
            for delete_input in Input.objects.filter(id__in=json.loads(str(request.POST.get('input_id', "[]")))):
                for product_input in delete_input.input_product_set.all():
                    if rollback == "true":
                        product = product_input.product
                        if delete_input.storage == "C":
                            product.in_consignment -= product_input.amount
                        elif delete_input.storage == "S":
                            product.in_stock -= product_input.amount
                        elif delete_input.storage == "U":
                            product.in_used -= product_input.amount
                        product.save()
                    product_input.delete()
                delete_input.delete()
        return HttpResponseRedirect('/inputs/')
    form = ProductInputForm()
    scripts = ['productInput']
    messages = get_messages(request)
    return render_to_response('pages/dashboard.html', locals(), context_instance=RequestContext(request))

@login_required
def outputs(request):
    dashboard_active = "active"
    outputs_active = "active"
    now = datetime.now()
    start_date = datetime.strptime(request.GET.get("start_date", now.replace(day=1).strftime("%Y-%m-%d")), "%Y-%m-%d").date()
    end_date = datetime.strptime(request.GET.get("end_date", now.strftime("%Y-%m-%d")), "%Y-%m-%d").date()
    formatted_start_date = start_date.strftime("%Y-%m-%d")
    formatted_end_date = end_date.strftime("%Y-%m-%d")
    outputs = Output.objects.filter(date__gte=start_date, date__lte=end_date.replace(day=end_date.day+1)).order_by('-date')
    if request.method == "POST":
        action = request.POST.get('action', '')
        if action == "CREATE":
            messages = []
            product_amount = json.loads(request.POST.get("outputProducts", "{}"))
            storage = request.POST.get("storage", "")
            date = datetime.strptime(request.POST.get("date", now.strftime("%Y-%m-%d")), "%Y-%m-%d").date()
            if product_amount and storage:
                new_output = Output(storage=storage, date=date)
                new_output.save()
                for productId, amount in product_amount.iteritems():
                    product = Product.objects.get(code=productId)
                    product_output = Output_Product(product=product, amount=amount, price=product.price, output_reg=new_output)
                    if storage == "C":
                        product.in_consignment -= int(amount)
                        if product.in_consignment < 0:
                            messages.append(("El producto "+product.code+" - "+product.name+" en Consignacion ha alcanzado valores negativos, favor de corregir inconsistencias.", "warning"))
                    elif storage == "S":
                        product.in_stock -= int(amount)
                        if product.in_stock < 0:
                            messages.append(("El producto "+product.code+" - "+product.name+" en Propias ha alcanzado valores negativos, favor de corregir inconsistencias.", "warning"))
                    elif storage == "U":
                        product.in_used -= int(amount)
                        if product.in_used < 0:
                            messages.append(("El producto "+product.code+" - "+product.name+" en Obsoletas ha alcanzado valores negativos, favor de corregir inconsistencias.", "warning"))
                    product_output.save()
                    product.save()
                if messages:
                    conf = Configuration.objects.all()[0]
                    if conf.mailOnNegativeValues:
                        if not conf.receiver_email or not send_email(conf.receiver_email, "BDMO Salida con valores negativos", "Salida del "+str(now)+" con inconsistencias en la base de datos:\n"+"\n".join([x[0] for x in messages])):
                            messages.append(("Correo de notificacion de valores negativos no enviado, correo no valido", "warning"))
            else:
                messages.append(("Salida no autorizada, los datos no fueron validos", "danger"))
            set_messages(request, messages)
        elif action == "DELETE":
            rollback = request.POST.get('rollback', 'false')
            for delete_output in Output.objects.filter(id__in=json.loads(str(request.POST.get('output_id', "[]")))):
                for product_output in delete_output.output_product_set.all():
                    if rollback == "true":
                        product = product_output.product
                        if delete_output.storage == "C":
                            product.in_consignment += product_output.amount
                        elif delete_output.storage == "S":
                            product.in_stock += product_output.amount
                        elif delete_output.storage == "U":
                            product.in_used += product_output.amount
                        product.save()
                    product_output.delete()
                delete_output.delete()
        return HttpResponseRedirect('/outputs/')
    form = ProductOutputForm()
    scripts = ['productOutput']
    messages = get_messages(request)
    return render_to_response('pages/dashboard.html', locals(), context_instance=RequestContext(request))

@login_required
def providers(request):
    dashboard_active = "active"
    providers_active = "active"
    providers = Provider.objects.all().order_by("name")
    if request.method == "POST":
        action = request.POST.get('action', '')
        if action == "CREATE":
            form = ProviderForm(request.POST)
            if form.is_valid():
                form.save()
            else:
                set_messages(request, [("Proveedor no agregado, los datos no fueron validos", "danger")])
        elif action == "UPDATE":
            provider = Provider.objects.get(id=request.POST['id'])
            form = ProviderForm(request.POST, instance=provider)
            if form.is_valid():
                form.save()
            else:
                set_messages(request, [("Proveedor no actualizado, los nuevos datos no son validos", "danger")])
        elif action == "DELETE":
            for provider in Provider.objects.filter(id__in=json.loads(str(request.POST.get('provider_id',"[]")))):
                provider.delete()
        return HttpResponseRedirect('/providers/')
    form = ProviderForm()
    provider_forms = {p.id:UpdateProviderForm(instance=p) for p in providers}
    scripts = ["provider"]
    messages = get_messages(request)
    return render_to_response('pages/dashboard.html', locals(), context_instance=RequestContext(request))

@login_required
def brands(request):
    dashboard_active = "active"
    brands_active = "active"
    brands = Brand.objects.all().order_by("name")
    if request.method == "POST":
        action = request.POST.get('action', '')
        if action == "CREATE":
            form = BrandForm(request.POST)
            if form.is_valid():
                form.save()
            else:
                set_messages(request, [("Marca no agregada, los datos no fueron validos", "danger")])
        elif action == "UPDATE":
            brand = Brand.objects.get(id=request.POST['id'])
            form = BrandForm(request.POST, instance=brand)
            if form.is_valid():
                form.save()
            else:
                set_messages(request, [("Marca no actualizada, los nuevos datos no son validos", "danger")])
        elif action == "DELETE":
            for brand in Brand.objects.filter(id__in=json.loads(str(request.POST.get('brand_id',"[]")))):
                brand.delete()
        return HttpResponseRedirect('/brands/')
    form = BrandForm()
    brand_forms = {b.id:UpdateBrandForm(instance=b) for b in brands}
    scripts = ["brand"]
    messages = get_messages(request)
    return render_to_response('pages/dashboard.html', locals(), context_instance=RequestContext(request))

@login_required
def appliances(request):
    dashboard_active = "active"
    appliances_active = "active"
    appliances = Appliance.objects.all().order_by("name")
    if request.method == "POST":
        action = request.POST.get('action', '')
        if action == "CREATE":
            form = ApplianceForm(request.POST)
            if form.is_valid():
                form.save()
            else:
                set_messages(request, [("Aplicacion no agregada, los datos no fueron validos", "danger")])
        elif action == "UPDATE":
            appliance = Appliance.objects.get(id=request.POST['id'])
            form = ApplianceForm(request.POST, instance=appliance)
            if form.is_valid():
                form.save()
            else:
                set_messages(request, [("Aplicacion no actualizada, los nuevos datos no son validos", "danger")])
        elif action == "DELETE":
            for appliance in Appliance.objects.filter(id__in=json.loads(str(request.POST.get('appliance_id',"[]")))):
                appliance.delete()
        return HttpResponseRedirect('/appliances/')
    form = ApplianceForm()
    appliance_forms = {a.id:UpdateApplianceForm(instance=a) for a in appliances}
    scripts = ["appliance"]
    messages = get_messages(request)
    return render_to_response('pages/dashboard.html', locals(), context_instance=RequestContext(request))

@login_required
def classifications(request):
    dashboard_active = "active"
    classifications_active = "active"
    classifications = Classification.objects.all().order_by("name")
    if request.method == "POST":
        action = request.POST.get('action', '')
        if action == "CREATE":
            form = ClassificationForm(request.POST)
            if form.is_valid():
                form.save()
            else:
                set_messages(request, [("Clasificacion no agregada, los datos no fueron validos", "danger")])
        elif action == "UPDATE":
            classification = Classification.objects.get(id=request.POST['id'])
            form = ClassificationForm(request.POST, instance=classification)
            if form.is_valid():
                form.save()
            else:
                set_messages(request, [("Clasificacion no actualizada, los nuevos datos no son validos", "danger")])
        elif action == "DELETE":
            for classification in Classification.objects.filter(id__in=json.loads(str(request.POST.get('classification_id',"[]")))):
                classification.delete()
        return HttpResponseRedirect('/classifications/')
    form = ClassificationForm()
    classification_forms = {c.id:UpdateClassificationForm(instance=c) for c in classifications}
    scripts = ["classification"]
    messages = get_messages(request)
    return render_to_response('pages/dashboard.html', locals(), context_instance=RequestContext(request))

@login_required
def registry(request):
    dashboard_active = "active"
    registry_active = "active"
    now = datetime.now()
    start_date = datetime.strptime(request.GET.get("start_date", now.replace(day=1).strftime("%Y-%m-%d")), "%Y-%m-%d").date()
    end_date = datetime.strptime(request.GET.get("end_date", now.strftime("%Y-%m-%d")), "%Y-%m-%d").date()
    formatted_start_date = start_date.strftime("%Y-%m-%d")
    formatted_end_date = end_date.strftime("%Y-%m-%d")
    outputs = list(Output.objects.filter(date__gte=start_date, date__lte=end_date))
    inputs = list(Input.objects.filter(date__gte=start_date, date__lte=end_date))
    lendings = list(Lending.objects.filter(date__gte=start_date, date__lte=end_date))
    registry = inputs+outputs+lendings
    registry.sort(key=lambda r: r.date)
    registry.reverse()
    return render_to_response('pages/dashboard.html', locals(), context_instance=RequestContext(request))

@login_required
def product(request, id):
    form = ProductForm(instance=Product.objects.get(code=id))
    storage = request.GET.get("storage", '')
    return render_to_response('pages/dialog.html', locals(), context_instance=RequestContext(request))

### REPORTS VIEW ###

@login_required
def reports(request):
    reports_active = "active"
    statistics_active = "active"
    scripts = ['Chart.min','statistics']
    year = int(request.GET.get("year", datetime.now().year))
    #adgoritmo de productos para mi papito hermoso te amo mucho y le entiendo muy bien html brand_forms end_date lendings.
    product_sales_dataset = {}
    product_earnings_dataset = {}
    for output in Output.objects.filter(date__gte=datetime(day=1, month=1, year=year), date__lte=datetime(day=31, month=12, year=year)):
        for product_output in output.output_product_set.all():
            if product_output.product.code in product_sales_dataset.keys():
                product_sales_dataset[product_output.product.code] += product_output.amount
            else:
                product_sales_dataset[product_output.product.code] = product_output.amount
            if product_output.product.code in product_earnings_dataset.keys():
                product_earnings_dataset[product_output.product.code] += product_output.amount * product_output.price
            else:
                product_earnings_dataset[product_output.product.code] = product_output.amount * product_output.price
    product_sales_labels = []
    product_sales_data = []
    for dataset_data in sorted(product_sales_dataset.items(), key=operator.itemgetter(1), reverse=True)[:10]:
        product = Product.objects.get(code=dataset_data[0])
        product_sales_labels.append(product.code + "-" + product.name)
        product_sales_data.append(dataset_data[1])
    product_earnings_labels = []
    product_earnings_data = []
    for dataset_data in sorted(product_earnings_dataset.items(), key=operator.itemgetter(1), reverse=True)[:10]:
        product = Product.objects.get(code=dataset_data[0])
        product_earnings_labels.append(product.code + "-" + product.name)
        product_earnings_data.append(dataset_data[1])
    ProductSalesData = json.dumps({'labels':product_sales_labels, 'datasets':[{"label":"Productos mas vendidos", "data":product_sales_data}]})
    ProductEarningsData = json.dumps({'labels':product_earnings_labels, 'datasets':[{"label":"Productos mas rentables", "data":product_earnings_data}]}, cls=DjangoJSONEncoder)
    return render_to_response('pages/dashboard.html', locals(), context_instance=RequestContext(request))

@login_required
def storage_diff(request):
    if request.method == "POST":
        codes = request.POST.keys()
        codes.remove('csrfmiddlewaretoken')
        codes.remove('subject')
        codes.remove('text')
        products = Product.objects.filter(code__in=codes)
        if len(products):
            provider_products = {}
            for product in products:
                if product.provider.id in provider_products.keys():
                    provider_products[product.provider.id].append(product)
                else:
                    provider_products[product.provider.id] = [product]
            for provider_id in provider_products.keys():
                provider = Provider.objects.get(id=provider_id)
                createOrder(provider, provider_products[provider_id], request.POST.get("subject", ""), request.POST.get("text", ""), request)
        else:
            set_messages(request, [("Ningun producto pedido. Orden no enviada", "warning")])
        return HttpResponseRedirect('/reports/differences/storage/')
    reports_active = "active"
    storage_diff_active = "active"
    stock_storage = {
        "name": "stock",
        "title": "Propias",
        "products": [],
        "active": "active"
    }
    consignment_storage = {
        "name": "consignment",
        "title": "Consignacion",
        "products": []
    }
    used_storage = {
        "name": "used",
        "title": "Obsoletas",
        "products": []
    }
    for product in Product.objects.all().order_by("code"):
        if product.in_consignment < product.consignment_tobe:
            consignment_storage["products"].append(product)
        if product.in_stock < product.stock_tobe:
            stock_storage["products"].append(product)
        if product.in_used < product.used_tobe:
            used_storage["products"].append(product)
    storages = [stock_storage, consignment_storage]
    scripts = ["orderStorage"]
    messages = get_messages(request)
    return render_to_response('pages/dashboard.html', locals(), context_instance=RequestContext(request))

@login_required
def product_diff(request):
    if request.method == "POST":
        codes = request.POST.keys()
        codes.remove('csrfmiddlewaretoken')
        codes.remove('subject')
        codes.remove('text')
        products = Product.objects.filter(code__in=codes)
        if len(products):
            provider = products[0].provider
            createOrder(provider, products, request.POST.get("subject", ""), request.POST.get("text", ""), request)
        else:
            set_messages(request, [("Ningun producto pedido. Orden no enviada", "warning")])
        return HttpResponseRedirect('/reports/differences/products/')
    reports_active = "active"
    product_diff_active = "active"
    products = []
    for product in Product.objects.all():
        if product.in_consignment < product.consignment_tobe or product.in_stock < product.stock_tobe:
            products.append(product)
    messages = get_messages(request)
    return render_to_response('pages/dashboard.html', locals(), context_instance=RequestContext(request))

@login_required
def provider_diff(request):
    if request.method == "POST":
        codes = request.POST.keys()
        codes.remove('csrfmiddlewaretoken')
        codes.remove('subject')
        codes.remove('text')
        products = Product.objects.filter(code__in=codes)
        if len(products):
            provider = products[0].provider
            createOrder(provider, products, request.POST.get("subject", ""), request.POST.get("text", ""), request)
        else:
            set_messages(request, [("Ningun producto pedido. Orden no enviada", "warning")])
        return HttpResponseRedirect('/reports/differences/providers/')
    reports_active = "active"
    provider_diff_active = "active"
    providers = []
    provider_products = {}
    for product in Product.objects.all():
        if product.in_consignment < product.consignment_tobe or product.in_stock < product.stock_tobe:
            if product.provider:
                if not product.provider.id in provider_products:
                    provider_products[product.provider.id] = [product]
                else:
                    provider_products[product.provider.id].append(product)
    providers = Provider.objects.filter(pk__in=provider_products.keys())
    for index in range(len(providers)):
        provider = providers[index]
        provider.products = provider_products[provider.pk]
        if index == 0:
            provider.active = "active"
    scripts = ["orderProvider"]
    messages = get_messages(request)
    return render_to_response('pages/dashboard.html', locals(), context_instance=RequestContext(request))

@login_required
def shopping(request):
    now = datetime.now()
    start_date = datetime.strptime(request.GET.get("start_date", now.replace(day=1).strftime("%Y-%m-%d")), "%Y-%m-%d").date()
    end_date = datetime.strptime(request.GET.get("end_date", now.strftime("%Y-%m-%d")), "%Y-%m-%d").date()
    formatted_start_date = start_date.strftime("%Y-%m-%d")
    formatted_end_date = end_date.strftime("%Y-%m-%d")
    orders = Order.objects.filter(date__gte=start_date, date__lte=end_date.replace(day=end_date.day+1)).order_by('-date')
    if request.method == "POST":
        action = request.POST.get('action', '')
        if action == "INPUT":
            pass
        if action == "RESEND":
            pass
        if action == "RECEIVED":
            for order in Order.objects.filter(id__in=json.loads(str(request.POST.get('order_id', "[]")))):
                order.status = Order.STATUS_RECEIVED
                order.received_date = now
                order.save()
        if action == "CANCEL":
            for order in Order.objects.filter(id__in=json.loads(str(request.POST.get('order_id', "[]")))):
                order.status = Order.STATUS_CANCELED
                order.save()
        if action == "DELETE":
            for order in Order.objects.filter(id__in=json.loads(str(request.POST.get('order_id', "[]")))):
                for order_product in order.order_product_set.all():
                    order_product.delete()
                order.delete()
    reports_active = "active"
    shopping_active = "active"
    return render_to_response('pages/dashboard.html', locals(), context_instance=RequestContext(request))

@login_required
def expenses(request):
    reports_active = "active"
    time = request.GET.get("time", 'W')
    expenses_active = {time: "active"}
    start_date = end_date = now = datetime.now()
    week = "%02d" % (int(request.GET.get("week", now.isocalendar()[1]-1)), )
    month = int(request.GET.get("month", now.month))
    year = int(request.GET.get("year", now.year))
    if time == 'W':
        start_date = datetime.strptime(str(year)+week+"1", '%Y%W%w')
        end_date = datetime.strptime(str(year)+"%02d" % (int(week)+1, )+"1", '%Y%W%w')
    elif time == 'M':
        start_date = datetime(year, month, 1)
        end_date = datetime(year, month+1, 1)
    elif time == 'A':
        start_date = datetime(year, 1, 1)
        end_date = datetime(year+1, 1, 1)
    inputs = Input.objects.filter(date__gte=start_date, date__lte=end_date)
    return render_to_response('pages/dashboard.html', locals(), context_instance=RequestContext(request))

### SETTINGS VIEW ###

def settings(request):
    settings_active = "active"
    conf = Configuration.objects.all()[0]
    form = ConfigurationForm(instance=conf)
    if request.method == "POST":
        form = ConfigurationForm(request.POST, instance=conf)
        if form.is_valid():
            form.save()
        else:
            set_messages(request, [("Configuracion no guardada, los datos no fueron validos", "danger")])
        return HttpResponseRedirect("/settings/")
    messages = get_messages(request)
    return render_to_response('pages/settings.html', locals(), context_instance=RequestContext(request))