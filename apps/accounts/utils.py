import random
import string

from django.conf import settings


def random_str(N):
    return ''.join(
        random.SystemRandom().choice(
            string.ascii_uppercase + string.ascii_lowercase + string.digits)
        for _ in range(N))


def captcha():
    x = random_str(settings.CAPTCHA_LENGTH)
    if settings.CAPTCHA_STRING_CASESENSITIVE:
        return x, x
    return x, x.lower()


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
