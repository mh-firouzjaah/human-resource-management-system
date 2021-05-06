from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BasicInformationsConfig(AppConfig):
    name = 'apps.BasicInformations'

    verbose_name = _('اطلاعات پایه')
    verbose_name_plural = _('اطلاعات پایه') 
