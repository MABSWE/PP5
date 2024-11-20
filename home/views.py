from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .forms import NewsletterForm
from .models import NewsletterSubscription
from django.contrib import messages

# Existing View
def index(request):
    """ A view to return the index page """
    return render(request, 'home/index.html')

# View robots.txt
def robots_txt(request):
    """ A view to return the robots.txt file """
    template = loader.get_template('robots.txt')
    return HttpResponse(template.render(), content_type='text/plain')

# Forms
def subscribe_to_newsletter(request):
    """Handle newsletter subscription through a form"""
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if not NewsletterSubscription.objects.filter(email=email).exists():
                form.save()
                messages.success(request, "You've successfully subscribed to our newsletter!")
            else:
                messages.info(request, "You're already subscribed.")
        else:
            messages.error(request, "Please enter a valid email address.")
        return redirect('home')  # Redirect to the homepage, can change later
    else:
        form = NewsletterForm()
    return render(request, 'home/subscribe_form.html', {'form': form})
    
# Subscription
def subscribe(request):
    """AJAX-based newsletter subscription"""
    if request.method == "POST":
        email = request.POST.get("email")
        if email:
            # Check if email is already subscribed
            if not NewsletterSubscription.objects.filter(email=email).exists():
                NewsletterSubscription.objects.create(email=email)
                return JsonResponse({"message": "Subscription successful"}, status=200)
            return JsonResponse({"message": "Email already subscribed"}, status=400)
        return JsonResponse({"message": "Invalid email"}, status=400)
    return JsonResponse({"message": "Method not allowed"}, status=405)