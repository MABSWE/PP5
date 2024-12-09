from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Product(models.Model):
    updated_at = models.DateTimeField(default=timezone.now)

@receiver(pre_save, sender=Product)
def update_timestamp(sender, instance, **kwargs):
    if not instance.updated_at:
        instance.updated_at = timezone.now()

class Testimonial(models.Model):
    user_name = models.CharField(max_length=100)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_name

class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    sent_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"
