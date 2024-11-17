from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.db.models import Q
from .models import Product
from .cart import Cart

# Create views here
def all_products(request):
    """Show products and searching and sorting queries"""
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'products/products.html', context)

def lashes(request):
    """Show only lash products"""
    lashes_products = Product.objects.filter(category__name='lashes')
    context = {
        'lashes': lashes_products,
    }
    return render(request, 'products/lashes.html', context)

def glue(request):
    """Show only glue products"""
    glue_products = Product.objects.filter(category__name='glue')
    context = {
        'glue': glue_products,
    }
    return render(request, 'products/glue.html', context)

def other(request):
    """Show other products"""
    other_products = Product.objects.filter(category__name='other')
    context = {
        'other': other_products,
    }
    return render(request, 'products/other.html', context)

def special_offers(request):
    """Display a message for special offers"""
    return render(request, 'products/special_offers.html')

def contact(request):
    """Display the contact page with Google Maps and contact information"""
    return render(request, 'products/contact.html')

# Product details
def product_detail(request, product_id):
    """Show details for a specific product"""
    product = get_object_or_404(Product, id=product_id)
    context = {
        'product': product,
    }
    return render(request, 'products/product_detail.html', context)

# Glue product details
def glue_detail(request, product_id):
    """Show details for a specific glue product"""
    product = get_object_or_404(Product, id=product_id, category__name='Glue')
    context = {
        'product': product,
    }
    return render(request, 'products/product_detail.html', context)

# Other product details
def other_detail(request, product_id):
    """Show details for a specific product in the 'Other' category"""
    product = get_object_or_404(Product, id=product_id, category__name='Other')
    context = {
        'product': product,
    }
    return render(request, 'products/product_detail.html', context)

# Search functionality
def product_search(request):
    """Handle searches for products"""
    query = request.GET.get('q')
    products = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    ) if query else Product.objects.none()

    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'products/search_results.html', context)

# Staff-only view
@staff_member_required
def admin_product_view(request):
    """View for administrators only"""
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'products/admin_product_view.html', context)

# Manager-only view
def is_manager(user):
    return user.groups.filter(name='Manager').exists()

@user_passes_test(is_manager)
def manager_view(request):
    """A view accessible only to managers"""
    return render(request, 'products/manager_view.html')

# Cart functionality
@require_POST
def cart_add(request, product_id):
    """Add a product to the cart"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product=product, quantity=quantity)
    return redirect('cart_detail')

@require_POST
def cart_remove(request, product_id):
    """Remove a product from the cart"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')

def cart_detail(request):
    """Display the cart"""
    cart = Cart(request)
    context = {'cart': cart}
    return render(request, 'products/cart_detail.html', context)
