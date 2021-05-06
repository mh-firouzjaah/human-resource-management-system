import re
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import resolve, reverse
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import gettext_lazy as _

from .models import LoginFailedIP
from .utils import get_client_ip

IGNORE_PATHS = [re.compile(settings.LOGIN_URL)]

IGNORE_PATHS += [
    re.compile(url) for url in getattr(settings, 'LOGIN_REQUIRED_IGNORE_PATHS', [])
]

IGNORE_VIEW_NAMES = [
    name for name in getattr(settings, 'LOGIN_REQUIRED_IGNORE_VIEW_NAMES', [])
]


class LoginRequiredMiddleware(AuthenticationMiddleware):
    def process_view(self, request, view_func, view_args, view_kwargs):
        path = request.path
        if request.user.is_authenticated:
            return

        resolver = resolve(path)
        views = ((name == resolver.view_name) for name in IGNORE_VIEW_NAMES)

        if not any(views) and not any(url.match(path) for url in IGNORE_PATHS):
            return redirect('{}?next={}'.format(
                reverse('admin:login'),
                request.path))


class PasswordValidationMiddleware(AuthenticationMiddleware):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated:
            if '/admin/password_change/' not in request.path:
                user = request.user
                if not user.has_valid_password:
                    return redirect('{}?next={}'.format(
                        reverse('admin:password_change'),
                        request.path))


class SessionExpiry(MiddlewareMixin):
    """ Set the session expiry according to settings """

    def process_request(self, request):
        if getattr(settings, 'SESSION_EXPIRY', None):
            request.session.set_expiry(settings.SESSION_EXPIRY)
        return None


class LoginFailedMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ip = get_client_ip(request)
        if LoginFailedIP.objects.filter(ip=ip).exists():
            offender = LoginFailedIP.objects.get(ip=ip)

            if offender.tries > settings.LOGIN_FAILED_LIMIT:
                mul = offender.tries - settings.LOGIN_FAILED_LIMIT
                base_cooldown = settings.LOGIN_FAILED_COOLDOWN
                stop = mul * base_cooldown
                cooldown = offender.last_try + timedelta(seconds=stop)
                cl, now = cooldown.timestamp(), timezone.now().timestamp()
                if timezone.now() <= cooldown:
                    # TODO: This response should be translated
                    return HttpResponse(
                        _('<center dir="rtl" style="margin-top: 30px;">'
                          "Too many attempts please try again after "
                          "<span id=\"cooldown-error\">{cooldown}</span>"
                          '</center>'
                          "<script>window.onload = function () {{var minute = {cooldown};var sec = 60;setInterval(function () {{document.getElementById('cooldown-error').innerHTML = minute-1 + ':' + sec;sec--;if (sec == 00) {{minute--;if(minute==00){{ window.location = window.location.href; }}sec = 60;}}}}, 1000);}};</script>").format(
                            cooldown=settings.LOGIN_FAILED_COOLDOWN // 60))
                else:
                    offender.tries -= 1
                    offender.save()
                    return redirect(reverse('admin:login'))

        return None
