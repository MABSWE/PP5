from django.contrib import admin
from .models import NewsletterSubscription, Testimonial, ContactMessage


# Register your models here.
admin.site.register(NewsletterSubscription)
admin.site.register(Testimonial)
admin.site.register(ContactMessage)