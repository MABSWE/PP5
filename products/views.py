from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.db.models import Q
from .models import Product
from .cart import Cart
from django.contrib import messages
import stripe
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django import forms
from django.contrib.auth.models import User


# Show all products
def all_products(request):
    """Show products and searching and sorting queries"""
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'products/products.html', context)

# Category-specific views


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
    """Add a product to the cart without showing a message."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product=product, quantity=quantity)

    if request.headers.get(
            'x-requested-with') == 'XMLHttpRequest':  # Check if AJAX
        return JsonResponse({'cart_total': cart.get_total_price()})

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


def checkout(request):
    """Show the checkout-site with a summary"""
    cart = Cart(request)
    context = {
        'cart': cart,
        'total_price': cart.get_total_price(),
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
    }
    return render(request, 'products/checkout.html', context)


def create_payment_intent(request):
    """Create a payment intent for Stripe checkout."""
    cart = Cart(request)
    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        intent = stripe.PaymentIntent.create(
            amount=int(cart.get_total_price() * 100),
            currency='usd',
            payment_method_types=['card'],
        )
        return JsonResponse({'client_secret': intent['client_secret']})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def order_success(request):
    """Show thank you message"""
    cart = Cart(request)
    cart.clear()
    messages.success(request, "Thank you for your purchase!")
    return render(request, 'products/order_success.html')


def cart_update(request, product_id):
    """Update the quantity of a product in the cart."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    try:
        quantity = int(request.POST.get('quantity'))
        if quantity > 0:
            cart.add(product=product, quantity=quantity, update_quantity=True)
        else:
            cart.remove(product)
    except ValueError:
        messages.error(request, "Invalid quantity value.")
    return redirect('cart_detail')


# Custom form for profile
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'username': '',
        }
# User profile


@login_required
def my_profile(request):
    """Display and allow updates to user profile"""
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was updated successfully.')
            return redirect('my_profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileForm(instance=user)

    context = {'form': form}
    return render(request, 'products/my_profile.html', context)
