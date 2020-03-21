from django.core.mail import send_mail
from send_email_celery_django.celery import app
import xmlrpc.client as xmlrpclib
import time

from .service import send
from .models import Contact

@app.task
def live_journal_task():
    ljsrv = xmlrpclib.ServerProxy(r"http://www.livejournal.com/interface/xmlrpc")
    curtime = time.localtime()
    data = {'ver':1,
     'subject':'THE TEST 22222222',
     'year': curtime[0],
     'mon': curtime[1],
     'day': curtime[2],
     'hour': curtime[3] + 2,
     'min': curtime[4],
     'security': 'private',
     'event': 'TEST 22222222 message <img src="https://i.pinimg.com/originals/03/79/0a/03790a3d3d8d84bb510659c15cb42c9a.jpg" /> from xml rpc',
     'username': 'username',
     'password': 'password',
     }
    response = ljsrv.LJ.XMLRPC.postevent(data)
    print(response)
    return response

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

@app.task
def my_task(a, b):
    c = a + b
    return c

@app.task
def my_task_as(d, e):
    c = d + e
    return c

#@app.task(bind=True, default_retry_delay=5*60)
#def my_task_retry(self, x, y):
    #try:
        #return x + y
    #except Exception as exc:
        #raise self.retry(exc=exc, countdown=60)

#@shared_task()
#def my_sh_task(msg):
#    return msg + "!!!"
