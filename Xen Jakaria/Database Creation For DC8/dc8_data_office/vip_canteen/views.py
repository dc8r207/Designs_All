
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the vip canteen index.")

from django.shortcuts import render

def menu(request):
	context = {}
	return render(request, 'vip_canteen/menu.html', context)

def cart(request):
	context = {}
	return render(request, 'vip_canteen/cart.html', context)

def checkout(request):
	context = {}
	return render(request, 'vip_canteen/checkout.html', context)