from captcha.fields import CaptchaField
from django.contrib.auth.forms import AuthenticationForm


class CustomLoginForm(AuthenticationForm):
    captcha = CaptchaField()
