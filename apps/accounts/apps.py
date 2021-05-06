from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AccountsConfig(AppConfig):
    name = 'apps.accounts'
    verbose_name = _("Accounts")
    # verbose_name_plural = _("Accounts")

    def ready(self):
        import apps.accounts.contenttype_translation
        import apps.accounts.signals
