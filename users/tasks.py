from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task(queue="low_priority")
def send_activation_email(email, first_name, activation_link):
    subject = "Activate your account"
    message = f"Hi {first_name}, please click the link: {activation_link}"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

@shared_task(queue="high_priority")
def order_in_silpo(order_id):
    print(f"Processing Silpo order {order_id}")

@shared_task(queue="high_priority")
def order_in_kfc(order_id):
    print(f"Processing KFC order {order_id}")