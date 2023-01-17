from django.core.mail import send_mail
from jellyfish.celery import app

@app.task
def send_confirmation_email(email, code):
    full_link = f'http://localhost:8000/api/v1/account/activate/{code}'
    send_mail(
        'User activation',
        f'Please, click the link to acitvate profile:  {full_link}',
        'sabyrkulov.nurmuhammed@gmail.com',
        [email]
    )


@app.task
def send_confirmation_code(email, code):
    send_mail(
        'Password recovery',
        f'Please, enter code to recover profile password: {code}',
        'sabyrkulov.nurmuhammed@gmail.com',
        [email]
    )