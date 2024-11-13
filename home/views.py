from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Existing View
def index(request):
    """ A view to return the index page """
    return render(request, 'home/index.html')

# View robots.txt
def robots_txt(request):
    """ A view to return the robots.txt file """
    template = loader.get_template('robots.txt')
    return HttpResponse(template.render(), content_type='text/plain')
