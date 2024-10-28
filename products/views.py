from django.shortcuts import render
from .models import Product

# Skapa dina vyer här.

def all_products(request):
    """ Show products and searching and sorting queries """
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'products/products.html', context)

def lashes(request):
    """ Visa endast fransar """
    lashes_products = Product.objects.filter(category__name='Lashes')
    context = {
        'lashes': lashes_products,
    }
    return render(request, 'products/lashes.html', context)

def glue(request):
    """ Visa endast limprodukter """
    glue_products = Product.objects.filter(category__name='Glue')
    context = {
        'glue': glue_products,
    }
    return render(request, 'products/glue.html', context)

def other(request):
    """ Visa övriga produkter """
    other_products = Product.objects.filter(category__name='Other')
    context = {
        'other': other_products,
    }
    return render(request, 'products/other.html', context)
