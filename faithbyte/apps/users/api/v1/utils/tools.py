import base64
import random
import string

from django.conf import settings
from django.core.mail import send_mail

def confirmation_code_generator(size=6, chars=string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def encode_email(email):
    encoded_email = base64.b64encode(email.encode('utf-8')).decode('utf-8')
    return encoded_email


def decode_email(email):
    decoded_email = base64.b64decode(email.encode('utf-8')).decode('utf-8')
    return decoded_email


def send_verification_code_to_email__second(email):
    code = confirmation_code_generator()
    subject = "Thank you for signing up for FaithByte!"
    html_message = f"""<html>
                       <body>
                            <h4>We're excited to see your selfies!</h4>
                            <h4>To complete your registration, please enter the code to the previous site</h4>
                            <h4>Activation code: {code}</h4>
                       </body>
                       </html>"""
    message = ""

    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject=subject, html_message=html_message, message=message, from_email=email_from,
                                recipient_list=recipient_list)
    return code