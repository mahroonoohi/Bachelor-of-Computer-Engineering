from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from hashids import Hashids
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.cache import cache

from Internet_Engineering.celery import app
from users.models import BaseUser


@app.task(name='verify_email', queue='email')
def send_email_confirmation_link(user_email, user_id, username):
    email_verify_token = cache.get(f"email_verification__{username}")
    if email_verify_token:
        token = email_verify_token
    else:
        hashids_verify_email = Hashids(salt=settings.EMAIL_VERIFY_SALT, min_length=10)
        token = hashids_verify_email.encode(user_id, timezone.now().microsecond)
        cache.set(
            f"email_verification__{username}",
            (token, 0),
            settings.EMAIL_VERIFY_EXPIRE_MINUTES * 60
        )


    email_detail = {
        'username': username,
        'url': f"{settings.EMAIL_VERIFY_URL}{username}/{token}"
    }
    email_content = render_to_string("email/email_confirmation.html", context=email_detail)


    email = EmailMultiAlternatives(subject="Activate your account", from_email=settings.EMAIL_HOST_USER,
                                   to=[user_email])

    email.attach_alternative(email_content, "text/html")
    email.send()


@app.task(name='change-password', queue='email')
def send_email_password_confirmation(user_id, username, validation_code):

    email_subject = "Change Password"
    email_detail = {
        'username': username,
        'validation_code': validation_code
    }
    email_content = render_to_string("email/change_password.html", context=email_detail)



    email = EmailMultiAlternatives(subject="Chang Your Password", from_email=settings.EMAIL_HOST_USER,
                                   to=[BaseUser.objects.get(id=user_id).email])

    email.attach_alternative(email_content, "text/html")
    email.send()

