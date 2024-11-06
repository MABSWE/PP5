from django.shortcuts import render, get_object_or_404
from .models import Product
from django.db.models import Q

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
    lashes_products = Product.objects.filter(category__name='lashes')
    context = {
        'lashes': lashes_products,
    }
    return render(request, 'products/lashes.html', context)

def glue(request):
    """ Visa endast limprodukter """
    glue_products = Product.objects.filter(category__name='glue')
    context = {
        'glue': glue_products,
    }
    return render(request, 'products/glue.html', context)

def other(request):
    """ Visa övriga produkter """
    other_products = Product.objects.filter(category__name='other')
    context = {
        'other': other_products,
    }
    return render(request, 'products/other.html', context)

def contact(request):
    """ Visa kontaktsidan med Google Maps och kontaktinformation """
    return render(request, 'products/contact.html')

# Ny vy för produktdetaljer
def product_detail(request, product_id):
    """ Visa detaljer för en specifik produkt """
    product = get_object_or_404(Product, id=product_id)
    context = {
        'product': product,
    }
    return render(request, 'products/product_detail.html', context)

# Ny vy för limproduktdetaljer
def glue_detail(request, product_id):
    """ Visa detaljer för en specifik limprodukt """
    product = get_object_or_404(Product, id=product_id, category__name='Glue')
    context = {
        'product': product,
    }
    return render(request, 'products/product_detail.html', context)

# Ny vy för övriga produktdetaljer
def other_detail(request, product_id):
    """ Visa detaljer för en specifik produkt i kategorin Other """
    product = get_object_or_404(Product, id=product_id, category__name='Other')
    context = {
        'product': product,
    }
    return render(request, 'products/product_detail.html', context)

# Sökfunktion för produkter
def product_search(request):
    """ Hanterar sökningar efter produkter """
    query = request.GET.get('q')
    products = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    ) if query else Product.objects.none()
    
    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'products/search_results.html', context)
