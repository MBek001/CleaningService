import random
import string

def generate_unique_code(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

from django.core.mail import send_mail

def send_test_email():
    subject = 'Test Email'
    message = 'This is a test email sent using Mailtrap.'
    from_email = 'your_email@example.com'
    recipient_list = ['recipient@example.com']

    send_mail(subject, message, from_email, recipient_list)


