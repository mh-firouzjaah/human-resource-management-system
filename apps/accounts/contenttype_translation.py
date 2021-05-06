from django.apps import apps
from django.contrib.contenttypes.models import ContentType


def new_app_labeled_name(self):
    model = self.model_class()
    if not model:
        return self.model
    return '%s | %s' % (
        apps.get_app_config(model._meta.app_label).verbose_name, model._meta.verbose_name)


def class_decorator(cls):
    cls.app_labeled_name = property(new_app_labeled_name)
    return cls


class_decorator(ContentType)
