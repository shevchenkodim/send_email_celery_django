from django.core.mail import send_mail
from send_email_celery_django.celery import app

from .service import send
from .models import Contact


@app.task
def send_spam_email(user_email):
    send(user_email)


@app.task
def send_beat_email():
    for contact in Contact.objects.all():
        send_mail(
            'Вы подписались на рассылку',
            'Мы будем присылать Вам много спама каждые 1 мин !',
            'djangos99@gmail.com',
            [contact.email],
            fail_silently=False,
        )
