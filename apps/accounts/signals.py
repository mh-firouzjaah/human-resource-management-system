from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.models import DELETION, LogEntry
from django.contrib.auth.signals import (user_logged_in, user_logged_out,
                                         user_login_failed)
from django.contrib.messages.api import error
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from jalali_date import datetime2jalali

from .models import LOGINLOGOUT, CustomLogger, LoginFailedIP, User
from .utils import get_client_ip


@receiver(user_logged_in)
def _concurrent_logins(sender, **kwargs):
    user = kwargs.get('user')
    user.is_logged_in = True
    request = kwargs.get('request')

    ip = get_client_ip(request)

    # delete previous login failed for this user
    if LoginFailedIP.objects.filter(ip=ip).exists():
        offender = LoginFailedIP.objects.get(ip=ip)
        offender.delete()

    # convert last last_logout to jalali_date
    last_logout = ''
    if user.last_logout is not None:
        last_logout = datetime2jalali(user.last_logout).strftime('%Y/%m/%d - %H:%M:%S')

    current_ip = get_client_ip(request)
    last_ip = user.last_ip
    login_message_string = _(
        "Welcome, last time you were logged out at {last_logout} and "
        "last IP was {last_ip}.<br/>"
        "your current ip is {current_ip}.<br/>"
        "You're being Watched and <strong>Responsible</strong> for whatever you've done.")

    login_message = mark_safe(
        login_message_string.format(
            last_logout=last_logout, last_ip=last_ip, current_ip=current_ip))

    user.last_ip = current_ip
    messages.info(request, login_message, fail_silently=True)

    # kick out all the other users logged in, with this credentials
    if user is not None and request is not None:
        user.set_session_key(request.session.session_key)

    # create log-entry for user login
    CustomLogger.objects.create(user=user, action=_("logged in"), action_flag=LOGINLOGOUT)


@receiver(user_logged_out)
def _user_logged_out(sender, user, request, **kwargs):
    user = user
    user.last_logout = timezone.now()
    user.is_logged_in = False
    user.save()

    # check if users password is not expired
    if timezone.now() > user.last_password_change + \
            timedelta(days=settings.PASSWORD_RESET_TIMEOUT_DAYS):
        user.has_valid_password = False

    # create log-entry for user log out
    CustomLogger.objects.create(
        user=user, action=_("logged out"),
        action_flag=LOGINLOGOUT)


@receiver(user_login_failed)
def _user_login_failed_callback(sender, credentials, **kwargs):
    request = kwargs.get('request')
    req_ip = ''
    # create or update LoginFailedIP object incase of login failed.
    if request is not None:
        req_ip = get_client_ip(request)
        if LoginFailedIP.objects.filter(ip=req_ip).exists():
            offender = LoginFailedIP.objects.get(ip=req_ip)
            offender.tries += 1
            offender.save()
            if offender.tries > settings.LOGIN_FAILED_LIMIT:
                messages.error(
                    request,
                    mark_safe(_("Too many attempts please try again after "
                                "<span id=\"cooldown-error\">{cooldown}</span>"
                                "<script>window.onload = function () {{var minute = {cooldown};var sec = 60;setInterval(function () {{document.getElementById('cooldown-error').innerHTML = minute-1 + ':' + sec;sec--;if (sec == 00) {{minute--;if(minute==00){{ window.location = window.location.href; }}sec = 60;}}}}, 1000);}};</script>").format(
                        cooldown=settings.LOGIN_FAILED_COOLDOWN // 60)))
        else:
            LoginFailedIP.objects.create(ip=req_ip, tries=1)

    # create log-entry for login failed
    message = _("ip: {req_ip} tries to log in.")
    user = _("Anonymous user")
    CustomLogger.objects.create(action=message.format(req_ip=req_ip),
                                user=user, action_flag=LOGINLOGOUT)


@receiver(post_save, sender=LogEntry)
def _logentry_capture(sender, instance, **kwargs):
    '''Create a log entry based on Django default LogEntry events'''

    action_dict = {1: _("Addition"), 2: _("Change"), 3: _("Deletion")}
    user = User.objects.get(id=instance.user_id)
    action = action_dict[instance.action_flag]
    object_name = ""

    if instance.action_flag != DELETION:
        ct = instance.content_type
        object_name = ct.name

    def object_link(obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = f'<a href="{obj.get_admin_url()}">{ct.name}</a>'
        return mark_safe(link)

    CustomLogger.objects.create(action_flag=instance.action_flag, user=user,
                                action=action, object_type=object_name,
                                object_link=object_link(instance))
