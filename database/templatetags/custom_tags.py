from django import template
import pdb

register = template.Library()

import calendar

@register.filter(name='month_name')
def month_name(month_number):
    return calendar.month_name[month_number]


@register.filter(name='substract')
def substract(value, arg):
    return value - arg

@register.filter(name='multiply')
def multiply(value, arg):
    return value * arg

@register.filter(name='real_price')
def real_price(product):
    return product.price-product.price*product.discount/100

@register.filter(name='real_price_amount')
def real_price_amount(product, amount):
    return amount*(product.price-product.price*product.discount/100)

@register.filter(name='total_sum')
def total_sum(movements):
    acc = 0
    for movement in movements:
    	if movement.type == "Input":
    		for input_product in movement.input_product_set.all():
    			acc += input_product.amount*float(input_product.price)
    return acc

@register.filter(name='total_required')
def total_required(product):
    return product.consignment_tobe-product.in_consignment+product.stock_tobe-product.in_stock