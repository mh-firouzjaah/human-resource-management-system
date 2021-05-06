from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class GarrisonsConfig(AppConfig):
    name = 'apps.Garrisons'

    verbose_name = _('پایگاه ها و امور مرتبط به پرسنل')
    verbose_name_plural = _('پایگاه ها و امور مرتبط به پرسنل')
