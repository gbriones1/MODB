from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.cache import never_cache
from database.models import Product, Tool, Input, Output, Lending, Input_Product, Output_Product, Lending_Product, Lending_Tool, Provider, Appliance, Brand, Order, Configuration, Order_Product, BackupManager, Percentage, Organization
from database.forms import ProductForm, ToolForm, ProductInputForm, ProductOutputForm, ProductLendingForm, ToolLendingForm, ProviderForm, ApplianceForm, BrandForm, UpdateProviderForm, UpdateBrandForm, UpdateApplianceForm, ConfigurationForm, OrderInputForm, BackupForm, PercentageForm, UpdatePercentageForm, OrganizationForm, UpdateOrganizationForm
from lib.email_client import send_email
from datetime import datetime
import calendar
import json, operator
import os
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
            order = Order(provider=provider)
            order.save()
            for product in products:
                organization_id = request.POST.get("organization"+product.code, "")
                organization = Organization.objects.get(id=organization_id) if organization_id else None
                storage = request.POST.get("storage"+product.code, None)
                product_order = Order_Product(product=product, amount=int(request.POST.get(product.code, "0")), order=order, organization=organization, storage=storage, status=Order.STATUS_ASKED)
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
    appliances = Appliance.objects.all()
    if request.method == "POST":
        action = request.POST.get('action', '')
        if action == "CREATE":
            data = request.POST.copy()
            query_brand = Brand.objects.filter(name=data["brand"])
            query_provider = Provider.objects.filter(name=data["provider"])
            if query_brand:
                data["brand"] = query_brand[0].id
            else:
                brand = Brand(name=data["brand"])
                brand.save()
                data["brand"] = brand.id
            if query_provider:
                data["provider"] = query_provider[0].id
            else:
                provider = Provider(name=data["provider"])
                provider.save()
                data["provider"] = provider.id
            form = ProductForm(data)
            if form.is_valid():
                form.save()
            else:
                set_messages(request, [("Producto no creado, los datos no fueron validos", "danger")])
        elif action == "UPDATE":
            product = Product.objects.get(code=request.POST['code'])
            data = request.POST.copy()
            query_brand = Brand.objects.filter(name=data["brand"])
            query_provider = Provider.objects.filter(name=data["provider"])
            if query_brand:
                data["brand"] = query_brand[0].id
            else:
                brand = Brand(name=data["brand"])
                brand.save()
                data["brand"] = brand.id
            if query_provider:
                data["provider"] = query_provider[0].id
            else:
                provider = Provider(name=data["provider"])
                provider.save()
                data["provider"] = provider.id
            form = ProductForm(data, instance=product)
            if form.is_valid():
                form.save()
            else:
                set_messages(request, [("Producto no actualizado, los nuevos datos no son validos", "danger")])
        elif action == "DELETE":
            for product in Product.objects.filter(code__in=json.loads(str(request.POST.get('code',"[]")))):
                product.delete()
        redirect_url = "/"
        storage = request.POST.get('storage', '')
        if storage:
            redirect_url = "/?storage="+storage
        return HttpResponseRedirect(redirect_url)
    form = ProductForm()
    storage = request.GET.get("storage", '')
    if storage == "C":
        products = products.filter(consignment_tobe__gt=0) | products.filter(in_consignment__gt=0)
        filter_active["C"] = "active"
    elif storage == "S":
        products = products.filter(stock_tobe__gt=0) | products.filter(in_stock__gt=0)
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
    for product in products:
        product.real_price = float("%.2f" % float(product.price-product.price*product.discount/100))
        product.percentage_1 = product.percentage_2 = product.percentage_3 = product.real_price
        percentage = Percentage.objects.filter(max_price_limit__gt=product.real_price).order_by("max_price_limit")
        if percentage:
            product.percentage_1 = product.real_price+product.real_price*float(percentage[0].percentage_1)/100
            product.percentage_2 = product.real_price+product.real_price*float(percentage[0].percentage_2)/100
            product.percentage_3 = product.real_price+product.real_price*float(percentage[0].percentage_3)/100
    scripts = ["product"]
    messages = get_messages(request)
    return render_to_response('pages/dashboard.html', locals(), context_instance=RequestContext(request))

@login_required
def tools(request):
    dashboard_active = "active"
    tools_active = "active"
    tools = Tool.objects.all()
    if request.method == "POST":
        action = request.POST.get('action', '')
        if action == "CREATE":
            form = ToolForm(request.POST)
            if form.is_valid():
                form.save()
            else:
                set_messages(request, [("Herramienta no creada, los datos no fueron validos", "danger")])
        elif action == "UPDATE":
            tool = Tool.objects.get(code=request.POST['code'])
            form = ToolForm(request.POST, instance=tool)
            if form.is_valid():
                form.save()
            else:
                set_messages(request, [("Herramienta no actualizada, los nuevos datos no son validos", "danger")])
        elif action == "DELETE":
            for tool in Tool.objects.filter(code__in=json.loads(str(request.POST.get('code',"[]")))):
                tool.delete()
        return HttpResponseRedirect("/tools/")
    form = ToolForm()
    sort = request.GET.get("sort", '')
    order = request.GET.get("order", '')
    if sort:
        if order == 'desc':
            sort = "-"+sort
        tools = tools.order_by(sort)
    scripts = ["tool"]
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
    if calendar.monthrange(end_date.year, end_date.month)[1] == end_date.day:
        if end_date.month == 12:
            end_date = end_date.replace(year=end_date.year+1, month=1, day=1)
        else:
            end_date = end_date.replace(month=end_date.month+1, day=1)
    else:
        end_date = end_date.replace(day=end_date.day+1)
    lendings = Lending.objects.filter(date__gte=start_date, date__lte=end_date).order_by('-date')
    if request.method == "POST":
        action = request.POST.get('action', '')
        if action == "CREATE":
            product_amount = json.loads(request.POST.get("lendingProducts", "{}"))
            tool_amount = json.loads(request.POST.get("lendingTools", "{}"))
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
            elif tool_amount and employee and destination:
                lending = Lending(storage=storage, employee=employee, destination=destination, date=date)
                lending.save()
                for toolCode, amount in tool_amount.iteritems():
                    tool = Tool.objects.get(code=toolCode)
                    tool_lending = Lending_Tool(tool=tool, amount=amount, lending=lending, returned_amount=0)
                    tool.amount -= int(amount)
                    tool_lending.save()
                    tool.save()
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
                for tool_lending in delete_lending.lending_tool_set.all():
                    if rollback == "true":
                        tool = tool_lending.tool
                        tool.amount += tool_lending.amount-tool_lending.returned_amount
                        tool.save()
                    tool_lending.delete()
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
                for tool_lending in return_lending.lending_tool_set.all():
                    tool = tool_lending.tool
                    tool_lending.returned_amount = int(request.POST["amount"+tool.code])
                    tool.amount += tool_lending.returned_amount
                    tool_lending.save()
                    tool.save()
                return_lending.returned = True
                return_lending.returned_date = now
                return_lending.save()
        elif action == "EMAIL":
            messages = []
            for lending in Lending.objects.filter(id__in=json.loads(str(request.POST.get('lending_id', "[]")))):
                message = "Registro de Prestamo\n\n"
                message += "Fecha: "+lending.date.strftime("%Y-%m-%d")+"\n"
                message += "Empleado: "+lending.employee+"\n"
                message += "Destino: "+lending.destination+"\n"
                if lending.storage:
                    message += "Salido de: "+lending.get_storage_display()+"\n"
                message += "\nLista de productos:\n"
                for product_lending in lending.lending_product_set.all():
                    product = product_lending.product
                    message += product.code+" - "+product.name+" - "+product.description+". Cantidad: x"+str(product_lending.amount)+"\n"
                for tool_lending in lending.lending_tool_set.all():
                    tool = tool_lending.tool
                    message += tool.code+" - "+tool.name+" - "+tool.description+". Cantidad: x"+str(tool_lending.amount)+"\n"
                conf = Configuration.objects.all()[0]
                if not conf.receiver_email or not send_email(conf.receiver_email, "Registro de prestamo", message):
                    messages.append(("Correo de registro de prestamo no enviado, correo no valido", "warning"))
            set_messages(request, messages)
        elif action == "OUTPUT":
            messages = []
            for output_lending in Lending.objects.filter(id__in=json.loads(str(request.POST.get('lending_id', "[]")))):
                product_amount = {}
                for product_lending in output_lending.lending_product_set.all():
                    product = product_lending.product
                    output_amount = int(request.POST["amount"+product.code])
                    if output_amount:
                        product_amount[product.code] = output_amount
                storage = output_lending.storage
                date = output_lending.date
                if product_amount and storage:
                    new_output = Output(storage=storage, date=date, employee=output_lending.employee, destination=output_lending.destination)
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
        return HttpResponseRedirect('/lendings/?start_date='+formatted_start_date+"&end_date="+formatted_end_date)
    form = ProductLendingForm()
    toolForm = ToolLendingForm()
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
    if calendar.monthrange(end_date.year, end_date.month)[1] == end_date.day:
        if end_date.month == 12:
            end_date = end_date.replace(year=end_date.year+1, month=1, day=1)
        else:
            end_date = end_date.replace(month=end_date.month+1, day=1)
    else:
        end_date = end_date.replace(day=end_date.day+1)
    inputs = Input.objects.filter(date__gte=start_date, date__lte=end_date).order_by('-date')
    if request.method == "POST":
        action = request.POST.get('action', '')
        if action == "CREATE":
            product_amount = json.loads(request.POST.get("inputProducts", "{}"))
            storage = request.POST.get("storage", "")
            invoice_number = request.POST.get("invoice_number", None)
            date = datetime.strptime(request.POST.get("date", now.strftime("%Y-%m-%d")), "%Y-%m-%d").date()
            if product_amount and storage:
                updated_products = []
                messages = []
                for productId, definition in product_amount.iteritems():
                    price = float(definition["price"])
                    discount = float(definition["discount"])
                    product = Product.objects.get(code=productId)
                    if float(product.price) != price or float(product.discount) != discount:
                        product.price = price
                        product.discount = discount
                        product.save()
                        updated_products.append(product.code+"-"+product.name+"-"+product.description+" a: $"+str(price)+" con "+str(discount)+"%")
                        messages.append(("El producto "+product.code+" - "+product.name+" cambio su precio a: $"+str(price)+" y descuento del "+str(discount)+"%", "success"))
                new_input = Input(storage=storage, date=date, invoice_number=invoice_number)
                new_input.save()
                for productId, definition in product_amount.iteritems():
                    amount = definition["amount"]
                    product = Product.objects.get(code=productId)
                    product_input = Input_Product(product=product, amount=amount, price=float(product.price-product.price*product.discount/100), input_reg=new_input)
                    if storage == "C":
                        product.in_consignment += int(amount)
                    elif storage == "S":
                        product.in_stock += int(amount)
                    elif storage == "U":
                        product.in_used += int(amount)
                    product_input.save()
                    product.save()
                if updated_products:
                    conf = Configuration.objects.all()[0]
                    if conf.mailOnPriceChange:
                        if not conf.receiver_email or not send_email(conf.receiver_email, "BDMO Entrada con precios cambiados", "Entrada autorizada del "+str(now)+" cambio los precios de los siguientes productos:\n"+"\n".join([x for x in updated_products])):
                            messages.append(("Correo de notificacion de precio cambiado no enviado, correo no valido", "warning"))
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
        elif action == "MULTIEMAIL":
            messages = []
            product_input_ids = json.loads(str(request.POST.get('product_input_id', "[]")))
            destination = request.POST.get("destination", "")
            if not product_input_ids:
                messages.append(("Ninguna salida seleccionada.", "warning"))
            if not destination:
                messages.append(("Ningun email seleccionado.", "warning"))
            if not messages:
                product_inputs = Input_Product.objects.filter(id__in=product_input_ids)
                email_text = ""
                total_sum = 0
                for product_input in product_inputs:
                    if request.POST.get("dateColumn", ""):
                        email_text += product_input.input_reg.date.strftime("%Y-%m-%d")+"\t"
                    if request.POST.get("codeColumn"):
                        email_text += product_input.product.code+"\t"
                    if request.POST.get("brandColumn"):
                        email_text += product_input.product.brand.name+"\t"
                    if request.POST.get("providerColumn"):
                        email_text += product_input.product.provider.name+"\t"
                    if request.POST.get("nameColumn"):
                        email_text += product_input.product.name+"\t"
                    if request.POST.get("amountColumn"):
                        email_text += str(product_input.amount)+"\t"
                    if request.POST.get("silglePriceColumn"):
                        email_text += "$"+str(product_input.product.price)+"\t"
                    if request.POST.get("totalPriceColumn"):
                        total_sum += float(product_input.product.price*product_input.amount)
                        email_text += "$"+str(product_input.product.price*product_input.amount)+"\t"
                    if request.POST.get("storageColumn"):
                        email_text += product_input.input_reg.get_storage_display()+"\t"
                    email_text += "\n"
                email_text += "\n"
                if request.POST.get("totalPriceColumn"):
                    email_text += "Total:\t$"+str(total_sum)
                if not send_email(destination, "Reporte de entrada", email_text):
                    messages.append(("Correo de registro de entrada no enviado, correo no valido", "warning"))
            else:
                messages.append(("Seleccion de entradas no enviada.", "error"))
            set_messages(request, messages)
        return HttpResponseRedirect('/inputs/?start_date='+formatted_start_date+"&end_date="+formatted_end_date)
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
    if calendar.monthrange(end_date.year, end_date.month)[1] == end_date.day:
        if end_date.month == 12:
            end_date = end_date.replace(year=end_date.year+1, month=1, day=1)
        else:
            end_date = end_date.replace(month=end_date.month+1, day=1)
    else:
        end_date = end_date.replace(day=end_date.day+1)
    outputs = Output.objects.filter(date__gte=start_date, date__lte=end_date).order_by('-date')
    if request.method == "POST":
        action = request.POST.get('action', '')
        if action == "CREATE":
            messages = []
            product_amount = json.loads(request.POST.get("outputProducts", "{}"))
            storage = request.POST.get("storage", "")
            date = datetime.strptime(request.POST.get("date", now.strftime("%Y-%m-%d")), "%Y-%m-%d").date()
            if product_amount and storage:
                organization = None
                if request.POST.get("organization", ""):
                    organization = Organization.objects.get(id=request.POST.get("organization", ""))
                new_output = Output(storage=storage, date=date, employee=request.POST.get("employee", ""), destination=request.POST.get("destination", ""), organization=organization)
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
        elif action == "EMAIL":
            messages = []
            for output in Output.objects.filter(id__in=json.loads(str(request.POST.get('output_id', "[]")))):
                message = "Registro de Salida\n\n"
                message += "Fecha: "+output.date.strftime("%Y-%m-%d")+"\n"
                message += "Salido de: "+output.get_storage_display()+"\n"
                message += "\nLista de productos:\n"
                for product_output in output.output_product_set.all():
                    product = product_output.product
                    message += product.code+" - "+product.name+" - "+product.description+". Cantidad: x"+str(product_output.amount)+"\n"
                conf = Configuration.objects.all()[0]
                if not conf.receiver_email or not send_email(conf.receiver_email, "Registro de salida", message):
                    messages.append(("Correo de registro de salida no enviado, correo no valido", "warning"))
            set_messages(request, messages)
        elif action == "MULTIEMAIL":
            messages = []
            product_output_ids = json.loads(str(request.POST.get('product_output_id', "[]")))
            destination = request.POST.get("destination", "")
            if not product_output_ids:
                messages.append(("Ninguna salida seleccionada.", "warning"))
            if not destination:
                messages.append(("Ningun email seleccionado.", "warning"))
            if not messages:
                product_outputs = Output_Product.objects.filter(id__in=product_output_ids)
                email_text = ""
                total_sum = 0
                for product_output in product_outputs:
                    this_price = float(product_output.product.price)-(float(product_output.product.price)*float(product_output.product.discount)/100)
                    if request.POST.get("dateColumn", ""):
                        email_text += product_output.output_reg.date.strftime("%Y-%m-%d")+"\t"
                    if request.POST.get("employeeColumn"):
                        email_text += product_output.output_reg.employee+"\t"
                    if request.POST.get("destinationColumn"):
                        email_text += product_output.output_reg.destination+"\t"
                    if request.POST.get("codeColumn"):
                        email_text += product_output.product.code+"\t"
                    if request.POST.get("brandColumn"):
                        email_text += product_output.product.brand.name+"\t"
                    if request.POST.get("providerColumn"):
                        email_text += product_output.product.provider.name+"\t"
                    if request.POST.get("nameColumn"):
                        email_text += product_output.product.name+"\t"
                    if request.POST.get("amountColumn"):
                        email_text += str(product_output.amount)+"\t"
                    if request.POST.get("silglePriceColumn"):
                        email_text += "$"+str(this_price)+"\t"
                    if request.POST.get("totalPriceColumn"):
                        total_sum += this_price*product_output.amount
                        email_text += "$"+str(this_price*product_output.amount)+"\t"
                    if request.POST.get("storageColumn"):
                        email_text += product_output.output_reg.get_storage_display()+"\t"
                    email_text += "\n"
                email_text += "\n"
                if request.POST.get("totalPriceColumn"):
                    email_text += "Total:\t$"+str(total_sum)
                if not send_email(destination, "Reporte de salida", email_text):
                    messages.append(("Correo de registro de salida no enviado, correo no valido", "warning"))
            else:
                messages.append(("Seleccion de salidas no enviada.", "error"))
            set_messages(request, messages)
        return HttpResponseRedirect('/outputs/?start_date='+formatted_start_date+"&end_date="+formatted_end_date)
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
def percentages(request):
    dashboard_active = "active"
    percentages_active = "active"
    percentages = Percentage.objects.all().order_by("max_price_limit")
    if request.method == "POST":
        action = request.POST.get('action', '')
        if action == "CREATE":
            form = PercentageForm(request.POST)
            if form.is_valid():
                form.save()
            else:
                set_messages(request, [("Porcentaje no agregada, los datos no fueron validos", "danger")])
        elif action == "UPDATE":
            percentage = Percentage.objects.get(id=request.POST['id'])
            form = PercentageForm(request.POST, instance=percentage)
            if form.is_valid():
                form.save()
            else:
                set_messages(request, [("Porcentaje no actualizada, los nuevos datos no son validos", "danger")])
        elif action == "DELETE":
            for percentage in Percentage.objects.filter(id__in=json.loads(str(request.POST.get('percentage_id',"[]")))):
                percentage.delete()
        return HttpResponseRedirect('/percentages/')
    form = PercentageForm()
    percentage_forms = {p.id:UpdatePercentageForm(instance=p) for p in percentages}
    scripts = ["percentage"]
    messages = get_messages(request)
    return render_to_response('pages/dashboard.html', locals(), context_instance=RequestContext(request))

@login_required
def organizations(request):
    dashboard_active = "active"
    organizations_active = "active"
    organizations = Organization.objects.all().order_by("name")
    if request.method == "POST":
        action = request.POST.get('action', '')
        if action == "CREATE":
            form = OrganizationForm(request.POST)
            if form.is_valid():
                form.save()
            else:
                set_messages(request, [("Organizacion no agregada, los datos no fueron validos", "danger")])
        elif action == "UPDATE":
            organization = Organization.objects.get(id=request.POST['id'])
            form = OrganizationForm(request.POST, instance=organization)
            if form.is_valid():
                form.save()
            else:
                set_messages(request, [("Organizacion no actualizada, los nuevos datos no son validos", "danger")])
        elif action == "DELETE":
            for organization in Organization.objects.filter(id__in=json.loads(str(request.POST.get('brand_id',"[]")))):
                organization.delete()
        return HttpResponseRedirect('/organizations/')
    form = OrganizationForm()
    organization_forms = {o.id:UpdateOrganizationForm(instance=o) for o in organizations}
    scripts = ["organization"]
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
    object_type = "Product"
    return render_to_response('pages/dialog.html', locals(), context_instance=RequestContext(request))

@login_required
def tool(request, id):
    form = ToolForm(instance=Tool.objects.get(code=id))
    object_type = "Tool"
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
    for product in Product.objects.all().order_by("code"):
        if product.in_consignment < product.consignment_tobe:
            consignment_storage["products"].append(product)
        if product.in_stock < product.stock_tobe:
            stock_storage["products"].append(product)
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
    if calendar.monthrange(end_date.year, end_date.month)[1] == end_date.day:
        if end_date.month == 12:
            end_date = end_date.replace(year=end_date.year+1, month=1, day=1)
        else:
            end_date = end_date.replace(month=end_date.month+1, day=1)
    else:
        end_date = end_date.replace(day=end_date.day+1)
    orders = Order.objects.filter(date__gte=start_date, date__lte=end_date).order_by('-date')
    if request.method == "POST":
        action = request.POST.get('action', '')
        if action == "CREATE":
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
        if action == "INPUT":
            for order_product in Order_Product.objects.filter(id__in=json.loads(str(request.POST.get('order_product_id', "[]")))):
                storage = request.POST.get("storage", "")
                invoice_number = request.POST.get("invoice_number", None)
                price = float(request.POST.get("price", "0"))
                discount = float(request.POST.get("discount", "0"))
                amount = int(request.POST.get("amount", "0"))
                product = order_product.product
                product.price = price
                product.discount = discount
                product.save()
                if storage and amount:
                    new_input = Input(storage=storage, date=now, invoice_number=invoice_number)
                    new_input.save()
                    product_input = Input_Product(product=product, amount=amount, price=float(product.price-product.price*product.discount/100), input_reg=new_input)
                    if storage == "C":
                        product.in_consignment += int(amount)
                    elif storage == "S":
                        product.in_stock += int(amount)
                    elif storage == "U":
                        product.in_used += int(amount)
                    product_input.save()
                    product.save()
                    order_product.status = Order.STATUS_RECEIVED
                    order_product.received_date = now
                    order_product.save()
                else:
                    set_messages(request, [("Entrada no autorizada, los datos no fueron validos", "danger")])
        if action == "RESEND":
            for order in Order.objects.filter(id__in=json.loads(str(request.POST.get('order_id', "[]")))):
                if order.provider.email:
                    message = request.POST.get("text", "")
                    for order_product in order.order_product_set.all():
                        product = order_product.product
                        if product.code in request.POST.keys():
                            order_product.amount = request.POST[product.code]
                            order_product.save()
                            message += "\n"+product.code+" - "+product.name+" "+product.description+". Cantidad: "+order_product.amount
                        else:
                            order_product.delete()
                    if send_email(order.provider.email, request.POST.get("subject", ""), message):
                        for order_product in order.order_product_set.all():
                            order_product.status = Order.STATUS_ASKED
                            order_product.save()
                    else:
                        for order_product in order.order_product_set.all():
                            order_product.status = Order.STATUS_PENDING
                            order_product.save()
                        add_message(request, ("Email no valido. Orden no enviada", "warning"))
                else:
                    add_message(request, ("Proveedor: "+provider.name+" sin email. Orden no enviada", "warning"))
        if action == "RECEIVED":
            for order in Order.objects.filter(id__in=json.loads(str(request.POST.get('order_id', "[]")))):
                for order_product in order.order_product_set.all():
                    order_product.status = Order.STATUS_RECEIVED
                    order_product.received_date = now
                    order_product.save()
        if action == "CANCEL":
            for order in Order.objects.filter(id__in=json.loads(str(request.POST.get('order_id', "[]")))):
                if order.provider.email:
                    message = request.POST.get("text", "")
                    for order_product in order.order_product_set.all():
                        product = order_product.product
                        message += "\n"+product.code+" - "+product.name+" "+product.description+". Cantidad: "+str(order_product.amount)
                    if send_email(order.provider.email, request.POST.get("subject", ""), message):
                        for order_product in order.order_product_set.all():
                            order_product.status = Order.STATUS_CANCELED
                            order_product.save()
                    else:
                        add_message(request, ("Email no valido. Email no enviado", "warning"))
                else:
                    add_message(request, ("Proveedor: "+order.provider.name+" sin email. Email no enviado", "warning"))
        if action == "DELETE":
            for order in Order.objects.filter(id__in=json.loads(str(request.POST.get('order_id', "[]")))):
                for order_product in order.order_product_set.all():
                    order_product.delete()
                order.delete()
        return HttpResponseRedirect('/reports/shopping/?start_date='+formatted_start_date+"&end_date="+formatted_end_date)
    dashboard_active = "active"
    shopping_active = "active"
    order_inputs_forms = {}
    for i in Order_Product.objects.filter(order__in=orders):
        form = OrderInputForm(instance=i)
        if request.user.is_superuser:
            form.fields['price'].initial = float(i.product.price)
            form.fields['discount'].initial = float(i.product.discount)
        form.fields['hidden_price'].initial = float(i.product.price)
        form.fields['hidden_discount'].initial = float(i.product.discount)
        order_inputs_forms[i.id] = form
    scripts = ["shopping"]
    messages = get_messages(request)
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

@login_required
def settings(request):
    settings_active = "active"
    conf = Configuration.objects.all()[0]
    form = ConfigurationForm(instance=conf)
    backupform = BackupForm()
    if request.method == "POST":
        form = ConfigurationForm(request.POST, instance=conf)
        if form.is_valid():
            form.save()
        else:
            set_messages(request, [("Configuracion no guardada, los datos no fueron validos", "danger")])
        return HttpResponseRedirect("/settings/")
    messages = get_messages(request)
    scripts = ["settings"]
    return render_to_response('pages/settings.html', locals(), context_instance=RequestContext(request))

def backup(request):
    if request.method == "POST":
        action = request.POST.get('action', '')
        if action == "CREATE":
            BackupManager().create_backup()
            add_message(request, ("Respaldo de la base de datos generado exitosamente", "success"))
        elif action == "UPLOAD":
            pass
        elif action == "SEND":
            backup = request.POST["backups"]
            if backup:
                conf = Configuration.objects.all()[0]
                backup_file = os.path.join(BackupManager.DIRECTORY, backup)
                if conf.receiver_email and send_email(conf.receiver_email, "Respaldo de la Base de Datos", "", files=[backup_file]):
                    add_message(request, ("Respaldo de la base de datos enviado exitosamente", "success"))
                else:
                    add_message(request, ("Respaldo no enviado, correo no valido", "danger"))
            else:
                add_message(request, ("Respaldo no enviado, seleccione un respaldo", "danger"))
        elif action == "RESTORE":
            backup = request.POST["backup"]
            if backup:
                BackupManager().restore_backup(backup)
                add_message(request, ("Respaldo de la base de datos restaurado exitosamente", "success"))
            else:
                add_message(request, ("Respaldo no realizado, seleccione un respaldo", "danger"))
        elif action == "DELETE":
            backup = request.POST["backup"]
            if backup:
                BackupManager().delete_backup(backup)
                add_message(request, ("Respaldo de la base de datos eliminado exitosamente", "success"))
            else:
                add_message(request, ("Eliminacion no realizada, seleccione un respaldo", "danger"))
    return HttpResponseRedirect("/settings/")

"""
Editar en consignacion redirecciona a Refacciones.
Eliminar temporizador en notificaciones.
Agregar precio con descuento al email de salidas.
Agregar codigo a lista de productos por pedir.

Agregar solicitante en pedidos.
Nuevos pedidos en pedidos.
Notificacion para cuando pedido se pasa de stock.
agregar a salidas cuantos hay en el almacen de la salida del producto
boton de devoluciones en salidas
boton de editar entradas, salidas, prestamos.
presupuestador
envio de arachivos csv.
"""