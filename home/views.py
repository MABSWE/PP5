from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .forms import NewsletterForm

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
        return redirect('home')