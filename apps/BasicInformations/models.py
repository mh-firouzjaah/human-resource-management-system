# -*- coding: utf-8 -*-
from django.db import models
from jalali_date import datetime2jalali


class State(models.Model):
    name = models.CharField(max_length=60, null=False, blank=False,
                            verbose_name='نام', unique=True,)
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان درج')
    updated = models.DateTimeField(
        auto_now=True, null=True, verbose_name='تاریخ و ز مان بروز رسانی')

    class Meta:
        verbose_name = 'استان'
        verbose_name_plural = 'استان ها'

    def __str__(self):
        return 'استان {0}'.format(self.name)


class City(models.Model):
    name = models.CharField(max_length=60, null=False, blank=False,
                            verbose_name='نام', unique=False)
    state = models.ForeignKey(
        'State', on_delete=models.SET_NULL, null=True, blank=False,
        verbose_name='استان مربوطه')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان درج')
    updated = models.DateTimeField(
        auto_now=True, null=True, verbose_name='تاریخ و ز مان بروز رسانی')

    class Meta:
        verbose_name = 'شهر'
        verbose_name_plural = 'شهر ها'

    def __str__(self):
        return 'شهر {0} در {1}'.format(self.name, self.state)


class Chevron(models.Model):
    title = models.CharField(max_length=60, null=False, blank=False,
                             verbose_name='عنوان', unique=True)
    code = models.IntegerField(null=True, blank=True,
                               verbose_name='کد درجه', unique=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان درج')
    updated = models.DateTimeField(
        auto_now=True, null=True, verbose_name='تاریخ و ز مان بروز رسانی')

    class Meta:
        verbose_name = 'درجه نظامی'
        verbose_name_plural = 'درجات نظامی'

    def __str__(self):
        return '{0}'.format(self.title)


class StatusEquipment(models.Model):
    title = models.CharField(max_length=60, null=False, blank=False,
                             verbose_name='عنوان', unique=True)
    code = models.IntegerField(null=True, blank=True,
                               verbose_name='کد وضعیت', unique=True)
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات تکمیلی')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان درج')
    updated = models.DateTimeField(
        auto_now=True, null=True, verbose_name='تاریخ و ز مان بروز رسانی')

    class Meta:
        verbose_name = 'وضعیت تجهیزات'
        verbose_name_plural = 'وضعیت های تجهیزات'

    def __str__(self):
        return 'وضعیت {0}'.format(self.title)


class Skill(models.Model):
    title = models.CharField(max_length=60, null=False, blank=False,
                             verbose_name='عنوان', unique=True)
    code = models.IntegerField(null=True, blank=True,
                               verbose_name='کد تخصص', unique=True)
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات تکمیلی')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان درج')
    updated = models.DateTimeField(
        auto_now=True, null=True, verbose_name='تاریخ و ز مان بروز رسانی')

    class Meta:
        verbose_name = 'تخصص و رسته'
        verbose_name_plural = 'تخصص ها و رسته ها'

    def __str__(self):
        return '{0}'.format(self.title)


class ZonetHreat(models.Model):
    title = models.CharField(max_length=60, null=False, blank=False,
                             verbose_name='عنوان', unique=True)
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات تکمیلی')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان درج')
    updated = models.DateTimeField(
        auto_now=True, null=True, verbose_name='تاریخ و ز مان بروز رسانی')
    pass

    class Meta:
        verbose_name = 'تهدید منطقه ای'
        verbose_name_plural = 'تهدیدات منطقه ای'

    def __str__(self):
        return '{0}'.format(self.title)


class Card(models.Model):
    title = models.CharField(max_length=60, null=False, blank=False,
                             verbose_name='عنوان', unique=True)
    code = models.IntegerField(null=True, blank=True,
                               verbose_name='کد کارت', unique=True)
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات تکمیلی')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان درج')
    updated = models.DateTimeField(verbose_name='تاریخ و ز مان بروز رسانی',
                                   auto_now=True,)

    class Meta:
        verbose_name = 'کارت حفاظتی'
        verbose_name_plural = 'کارت های حفاظتی'

    def __str__(self):
        return '{0}'.format(self.title)


class AcademicField(models.Model):
    name = models.CharField(verbose_name='رشته تحصیلی', max_length=50,
                            null=False, blank=False, unique=True)

    class Meta:
        verbose_name = 'رشته دانشگاهی'
        verbose_name_plural = 'رشته های دانشگاهی'

    def __str__(self):
        return f'{self.name}'


class ToolsCategory(models.Model):
    name = models.CharField(verbose_name='عنوان دسته بندی',
                            max_length=50, null=False, blank=False, unique=True)

    class Meta:
        verbose_name = 'دسته بندی تجهیزات'
        verbose_name_plural = 'دسته بندی های تجهیزات'

    def __str__(self):
        return '{0}'.format(self.name)


class EventCategory(models.Model):
    name = models.CharField(verbose_name='عنوان دسته بندی',
                            max_length=50, null=False, blank=False, unique=True)

    class Meta:
        verbose_name = 'دسته بندی رویداد'
        verbose_name_plural = 'دسته بندی های رویداد ها'

    def __str__(self):
        return '{0}'.format(self.name)
