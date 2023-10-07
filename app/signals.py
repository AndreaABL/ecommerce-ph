from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from django.db.models.signals import post_save
from .models import Order
from django.core.mail import send_mail

order_status_changed = Signal()

@receiver(post_save, sender=Order)
def order_created_alert(sender, instance, created, **kwargs):
    if created:
        # Send an alert to the Django administration
        # You can customize the message and handling here
        from django.core.mail import mail_admins
        mail_admins(
            'Nueva orden creada',
            f'Order ID: {instance.id} has been created by {instance.user}.',
        )

