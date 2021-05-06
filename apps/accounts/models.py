from django.contrib.auth.models import AbstractUser
from django.contrib.sessions.models import Session
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from jalali_date import datetime2jalali

from apps.Garrisons.models import Soldier

ADDITION = 1
CHANGE = 2
DELETION = 3
LOGINLOGOUT = 4

ACTION_FLAG_CHOICES = (
    (ADDITION, _('Addition')),
    (CHANGE, _('Change')),
    (DELETION, _('Deletion')),
    (LOGINLOGOUT, _('Log in/Log out')),
)


class LoginFailedIP(models.Model):
    ip = models.GenericIPAddressField(_("IP"), protocol="both", unpack_ipv4=False)
    tries = models.PositiveSmallIntegerField(_("Try Count"))
    last_try = models.DateTimeField(_("Last Try"), auto_now=True)


class User(AbstractUser):
    last_session_key = models.CharField(blank=True, null=True, max_length=40)
    has_valid_password = models.BooleanField(_("Has valid password"), default=False)
    last_password_change = models.DateTimeField(_("Last password change"),
                                                null=True, blank=True)
    last_ip = models.GenericIPAddressField(_("Last IP"), null=True, blank=True,
                                           protocol="both", unpack_ipv4=False)
    is_logged_in = models.BooleanField(_("Logged in"), default=False)
    last_logout = models.DateTimeField(_("Last logout"), null=True, blank=True,)

    personal = models.ForeignKey("Garrisons.Personal", verbose_name=_("Personal"),
                                 on_delete=models.CASCADE, null=True, blank=True)
    soldier = models.ForeignKey("Garrisons.Soldier", verbose_name=_("Soldier"),
                                on_delete=models.CASCADE, null=True, blank=True)
    garrison = models.ForeignKey("Garrisons.Garrison", verbose_name=_("Garrison"),
                                 null=True, blank=True,
                                 related_name='admin_user', on_delete=models.SET_NULL)

    def set_session_key(self, key):
        if self.last_session_key and not self.last_session_key == key:
            if Session.objects.filter(session_key=self.last_session_key).exists():
                Session.objects.get(session_key=self.last_session_key).delete()
        self.last_session_key = key
        self.save()

    def get_full_name(self):
        return self.personal.__str__() if self.personal else self.username

    def __str__(self):
        return self.get_full_name()

    def clean(self, *args, **kwargs):
        if not self.personal and not self.soldier:
            raise ValidationError("یکی از فیلدهای پایور یا وظیفه باید مقداردهی شود")
        return super().save(*args, **kwargs)


class UserPassword(models.Model):

    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)
    password = models.CharField(_("Password"), max_length=100)

    def __str__(self):
        """Unicode representation of UserPassword."""
        return f'{self.user}'


class CustomLogger(models.Model):
    action = models.CharField(_("Action"), max_length=500)
    user = models.CharField(_("User"), max_length=500)
    action_flag = models.PositiveSmallIntegerField(_('action flag'),
                                                   choices=ACTION_FLAG_CHOICES)
    event_date = models.DateTimeField(_("Event Date"), default=timezone.now)
    # object_id = models.TextField(_('object id'), blank=True, null=True)
    # object_repr = models.CharField(_('object repr'), max_length=200)
    object_type = models.CharField(_("Object Type"), max_length=250, default="")
    object_link = models.CharField(_("Object URL"), max_length=250, null=True, blank=True)

    class Meta:
        verbose_name = _("Log Entry")
        verbose_name_plural = _("Log Entries")
        # ordering = ('-action_time',)

    def event_date_to_jalali(self):
        return datetime2jalali(self.event_date).strftime('%y/%m/%d _ %H:%M:%S')

    def __str__(self):
        date = self.event_date_to_jalali()
        string = _("date: {event_date}, user: {user}, action: {action}")
        return string.format(event_date=date,
                             user=self.user, action=self.action)
