import datetime
from itertools import chain

from django.core.exceptions import ValidationError
from django.db import models

from apps.Garrisons.models import Garrison, Location, Personal, Soldier

HOURS = [(datetime.time(hour=x, minute=0), '{:02d}:00'.format(x)) for x in range(0, 24)]
HOURS_WITH_HALF = [(datetime.time(hour=x, minute=30),
                    '{:02d}:30'.format(x)) for x in range(0, 24)]
HOUR_CHOICES = list(chain(*zip(HOURS, HOURS_WITH_HALF)))
# HOUR_CHOICES = (None, None) + HOUR_CHOICES


class Position(models.Model):
    GUN_CHOICES = (
        ('فاقد اسلحه', 'فاقد اسلحه'),
        ('MP4 - 20 تیر', 'MP4 - 20 تیر'),
        ('ژ 3 - 20 تیر', 'ژ 3 - 20 تیر'),
        ('کلت برونینگ - 12 تیر', 'کلت برونینگ - 12 تیر'),
        ('کلاشینکف - 20 تیر', 'کلاشینکف - 20 تیر'),
        ('باتوم', 'باتوم'),
        ('شوکر', 'شوکر'),
        ('باتوم و شوکر', 'باتوم و شوکر'),
        ('دیگر', 'دیگر'),
    )
    title = models.CharField(max_length=128, null=False, verbose_name='عنوان پست نگهبانی')
    location = models.ForeignKey(Location,
                                 on_delete=models.SET_NULL,
                                 verbose_name='مکان',
                                 null=True, blank=False, )
    weapon = models.CharField(verbose_name='سلاح',
                              max_length=50, choices=GUN_CHOICES, default='A',)
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات تکمیلی')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان درج')
    updated = models.DateTimeField(verbose_name='تاریخ و زمان بروز رسانی',
                                   auto_now=True)

    class Meta:
        verbose_name = 'پست نگهبانی'
        verbose_name_plural = 'پست های نگهبانی'

    def __str__(self):
        return 'پست {0} در {1}'.format(self.title, self.location)


class PersonalMilitaryPolice(models.Model):
    personal = models.ForeignKey(Personal,
                                 on_delete=models.SET_NULL,
                                 verbose_name='پایور',
                                 null=True, blank=False)
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات تکمیلی')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان درج')
    updated = models.DateTimeField(verbose_name='تاریخ و زمان بروز رسانی',
                                   auto_now=True, null=True)

    class Meta:
        verbose_name = 'پایور پلیس هوایی'
        verbose_name_plural = 'پایوران پلیس هوایی'

    def __str__(self):
        return f'{self.personal}'


class SoldierMilitaryPolice(models.Model):
    soldier = models.ForeignKey(Soldier, on_delete=models.SET_NULL,
                                null=True, blank=False, verbose_name='وظیفه')
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات تکمیلی')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان درج')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ و زمان بروز رسانی')

    class Meta:
        verbose_name = 'وظیفه پلیس هوایی'
        verbose_name_plural = 'وظیفه های پلیس هوایی'

    def __str__(self):
        return f'{self.soldier}'


class GuardTablet(models.Model):
    title = models.CharField(
        verbose_name="عنوان لوحه", max_length=550,
        default='لوحه نگهبانی کادر و وظیفه گروه دژبان'
    )
    garrison = models.ForeignKey(
        'Garrisons.Garrison', on_delete=models.SET_NULL, null=True, blank=False,
        verbose_name='پایگاه')
    apply_date = models.DateField(verbose_name='تاریخ لوحه', unique=True)
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات تکمیلی')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان درج')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ و زمان بروز رسانی')

    class Meta:
        verbose_name = 'لوحه نگهبانی'
        verbose_name_plural = 'لوحه های نگهبانی'

    def __str__(self):
        return 'لوحه نگهبانی {0}'.format(self.apply_date)


class PersonalGuard(models.Model):
    guard_tablet = models.ForeignKey(GuardTablet,
                                     on_delete=models.SET_NULL,
                                     related_name='personals_on_guard',
                                     verbose_name='لوحه نگهبانی',
                                     null=True, blank=False,)
    personal = models.ForeignKey(PersonalMilitaryPolice,
                                 on_delete=models.SET_NULL,
                                 verbose_name='پایور',
                                 null=True, blank=False, )
    position = models.ForeignKey(Position,
                                 on_delete=models.SET_NULL,
                                 verbose_name='پست',
                                 null=True, blank=False)
    shift_start = models.TimeField(verbose_name='ساعت شروع پست',
                                   choices=HOUR_CHOICES, null=False, blank=False)
    shift_end = models.TimeField(verbose_name='ساعت پایان پست',
                                 choices=HOUR_CHOICES, null=False, blank=False)
    shift_ends_next_day = models.BooleanField(verbose_name="روز بعد",
                                              default=False, choices=[
                                                  (True, 'بله'), (False, 'خیر')])
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات تکمیلی')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان درج')
    updated = models.DateTimeField(verbose_name='تاریخ و زمان بروز رسانی',
                                   auto_now=True, null=True)

    class Meta:
        verbose_name = 'پایور پلیس هوایی'
        verbose_name_plural = 'پایوران پلیس هوایی'

    def __str__(self):
        return 'پلیس هوایی {0}، پایور در {1}'.format(self.personal, self.position)


class SoldierGuard(models.Model):
    guard_tablet = models.ForeignKey(GuardTablet,
                                     on_delete=models.SET_NULL,
                                     related_name='soldiers_on_guard',
                                     verbose_name='لوحه نگهبانی',
                                     null=True, blank=False,)
    soldier = models.ForeignKey(SoldierMilitaryPolice,
                                on_delete=models.SET_NULL,
                                verbose_name='وظیفه',
                                null=True, blank=False, )
    position = models.ForeignKey(Position,
                                 on_delete=models.SET_NULL,
                                 verbose_name='پست',
                                 related_name='soldiers_on_this_postion',
                                 null=True, blank=False)
    shift_start = models.TimeField(verbose_name='ساعت شروع پست',
                                   choices=HOUR_CHOICES, null=False, blank=False)
    shift_end = models.TimeField(verbose_name='ساعت پایان پست',
                                 choices=HOUR_CHOICES, null=False, blank=False)
    shift_ends_next_day = models.BooleanField(verbose_name="روز بعد", default=False,
                                              # choices=[(True, 'بله'), (False, 'خیر')]
                                              )
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات تکمیلی')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان درج')
    updated = models.DateTimeField(verbose_name='تاریخ و زمان بروز رسانی',
                                   auto_now=True, null=True)

    class Meta:
        verbose_name = 'وظیفه پلیس هوایی'
        verbose_name_plural = 'وظیفه های پلیس هوایی'

    def __str__(self):
        return '{0}، پلیس هوایی در {1}'.format(self.soldier, self.position)

    def clean(self):
        '''Ensure that dates are regular'''
        super().clean()
        if self.shift_start >= self.shift_end and not self.shift_ends_next_day:
            raise ValidationError(
                "ساعت شروع شیفت نمی‌تواند همزمان یا متعاقب ساعت پایان شیفت باشد.")
