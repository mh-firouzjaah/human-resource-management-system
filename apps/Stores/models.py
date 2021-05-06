# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.db.models import Q
from django.utils import timezone
from jalali_date import datetime2jalali

from apps.Garrisons.models import Garrison, Location, Owner, Personal

numeric = RegexValidator(r'^[0-9+]', 'فقط عدد وارد کنید.')
ip_ic = RegexValidator(r'^[0-9.+]', 'فقط عدد و نقطه مجاز است.')


class Charge(models.Model):
    name = models.CharField(max_length=60, null=True, blank=True,
                            verbose_name='عنوان اعتبار')
    number = models.CharField(max_length=60, null=True, blank=False,
                              verbose_name='شماره امریه', unique=True)
    amount = models.IntegerField(verbose_name='مبلغ به ریال',
                                 validators=[MinValueValidator(1), ])
    garrison = models.ForeignKey(Garrison, verbose_name='یگان دریافت کننده',
                                 on_delete=models.CASCADE)
    receive_date = models.DateField(verbose_name='تاریخ دریافت')
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات تکمیلی')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان درج')
    updated = models.DateTimeField(verbose_name='تاریخ و ز مان بروز رسانی', auto_now=True)
    pass

    class Meta:
        verbose_name = 'اعتبار'
        verbose_name_plural = 'اعتبارات'

    def __str__(self):
        return '{0} - {1} ریال'.format(self.name, str(self.amount))


class Shop(models.Model):
    name = models.CharField(
        max_length=60, verbose_name='نام', unique=True)
    city = models.ForeignKey(
        'BasicInformations.City', on_delete=models.SET_NULL, null=True, blank=False,
        verbose_name='شهر مربوطه')
    address = models.TextField(verbose_name='آدرس دقیق')
    phone_number = models.CharField(
        max_length=11, null=True, blank=True, verbose_name='شماره تلفن',
        validators=[numeric])
    manager_full_name = models.CharField(
        max_length=11, null=True, blank=True, verbose_name='نام و نشان مدیر')
    manager_mobile_number = models.CharField(
        max_length=11, null=True, blank=True, verbose_name='تلفن همراه مدیر',
        validators=[numeric])
    information_security_license = models.CharField(
        max_length=30, null=True, blank=True, verbose_name='مجوز حفاظت اطلاعات',
        help_text='شماره امریه یا نامه حفاظت اطلاعات، که مبنی بر تایید فروشگاه می باشد.')
    samta_license = models.CharField(
        max_length=30, null=True, blank=True, verbose_name='مجوز سمتا')
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات تکمیلی')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان درج')
    updated = models.DateTimeField(
        auto_now=True, null=True, blank=True, verbose_name='تاریخ و ز مان بروز رسانی')

    class Meta:
        verbose_name = 'فروشگاه'
        verbose_name_plural = 'فروشگاه ها'

    def __str__(self):
        return 'فروشگاه {0}'.format(self.name)


class Depot(models.Model):
    name = models.CharField(
        max_length=60, verbose_name='نام', unique=True)
    garrison = models.ForeignKey(
        Garrison, on_delete=models.SET_NULL, null=True, blank=False,
        verbose_name='پایگاه مربوطه')
    zonet_hreats = models.ManyToManyField(
        'BasicInformations.ZonetHreat', verbose_name='تهدیدات منطقه ای', blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان درج')
    updated = models.DateTimeField(
        auto_now=True, null=True, blank=True, verbose_name='تاریخ و ز مان بروز رسانی')

    class Meta:
        verbose_name = 'انبار'
        verbose_name_plural = 'انبار ها'

    def __str__(self):
        return 'انبار {0}'.format(self.name)


class Equipment(models.Model):
    name = models.CharField(max_length=60, verbose_name='نام')
    category = models.ForeignKey(
        'BasicInformations.ToolsCategory', on_delete=models.CASCADE,
        verbose_name='دسته بندی', null=False, blank=False)
    description_equipment = models.TextField(
        null=True, blank=True, verbose_name='شرح کالا')
    brand = models.CharField(max_length=60, null=True, blank=True, verbose_name='برند')
    model = models.CharField(max_length=60, null=True, blank=True, verbose_name='مدل')
    serial_number = models.CharField(
        max_length=60, null=True, blank=True, verbose_name='شماره سریال', unique=True)
    image = models.ImageField(
        null=True, blank=True, verbose_name='تصویر',
        upload_to='UploadFiles\Images\Equipments')
    files = models.FileField(
        null=True, blank=True, verbose_name='فایل',
        upload_to='UploadFiles\EquipmentFiles')
    buy_date = models.DateField(verbose_name='تاریخ خرید')
    # buy_expert = models.ForeignKey(Personal, on_delete = models.SET_NULL, null = True, blank = False, verbose_name = 'کارشناس خرید')
    buyer = models.ForeignKey(Personal,
                              on_delete=models.CASCADE,
                              # limit_choices_to={'is_buyer': True},
                              related_name='bought_equipments',
                              verbose_name='عامل خرید')
    buy_expert = models.ForeignKey(Personal,
                                   on_delete=models.CASCADE,
                                   limit_choices_to={'is_buy_expert': True},
                                   related_name='expert_bought_equipments',
                                   null=True, blank=True,
                                   verbose_name='کارشناس خرید')
    owner = models.ForeignKey(Owner, on_delete=models.SET_NULL,
                              null=True, blank=False, verbose_name='ذی حساب')
    sis_number = models.CharField(max_length=60, null=False,
                                  blank=False, verbose_name='شماره SIS', unique=True)
    lp_number = models.CharField(max_length=60, null=True,
                                 blank=True, verbose_name='شماره LP', unique=True)
    # charge = models.ForeignKey('Charge', on_delete = models.SET_NULL, null = True, blank = False, verbose_name = 'تهیه شده از اعتبار')
    charges = models.ManyToManyField(
        Charge, null=True, blank=True, verbose_name='اعتبارات',
        help_text='مشخص کنید از کدام اعتبار(های) دریافتی، خریداری شده است.')
    shop = models.ForeignKey(
        'Shop', on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='تهیه شده از فروشگاه',
        related_name='equipments')
    buy_date = models.DateField(null=True, blank=False, verbose_name='تاریخ خرید')
    amount = models.IntegerField(verbose_name='قیمت خرید به ریال',
                                 validators=[MinValueValidator(1), ])
    status = models.ForeignKey(
        'BasicInformations.StatusEquipment', on_delete=models.SET_NULL, null=True,
        blank=False, verbose_name='وضعیت فعلی')
    imperialistic = models.CharField(
        max_length=60, null=True, blank=True, verbose_name='بهره بردار')
    imperialistic_date = models.DateField(
        verbose_name='تاریخ بهره برداری')
    ip_address = models.CharField(max_length=15, null=True,
                                  blank=True, verbose_name='آدرس IP',
                                  validators=[ip_ic])
    port_number = models.IntegerField(null=True, blank=True, verbose_name='شماره پورت',
                                      validators=[MinValueValidator(1), ])
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='مکان تحویل گیرنده')
    depot = models.ForeignKey("Depot", verbose_name='انبار',
                              on_delete=models.SET_NULL, null=True, blank=True,)
    deploy_location = models.CharField(
        max_length=60, null=True, blank=True, verbose_name='محل استقرار')
    level_info = models.BooleanField(
        verbose_name='شامل اطلاعات طبقه بندی شده')
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات تکمیلی')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان درج')
    updated = models.DateTimeField(
        auto_now=True, null=True, blank=True, verbose_name='تاریخ و ز مان بروز رسانی')

    class Meta:
        verbose_name = 'کالا'
        verbose_name_plural = 'تجهیزات'

    def clean(self):
        super().clean()
        """Ensure that only one of `location` and `depot` can be set."""
        if (self.location and self.depot) or\
                (not self.location and not self.depot):
            raise ValidationError(
                "یکی از فیلد های «مکان» یا «انبار» باید مقداردهی شود.")
        if self.buy_date and self.imperialistic_date:
            if self.buy_date > self.imperialistic_date:
                raise ValidationError(
                    "تاریخ بهره‌برداری نباید همزمان یا پیش از تاریخ خرید باشد.")

    def __str__(self):
        return '{0}'.format(self.name)


class History(models.Model):
    event_date_time = models.DateTimeField(
        verbose_name='تاریخ و زمان رویداد')
    precept_number = models.CharField(
        max_length=60, verbose_name='شماره امریه', unique=True)
    equipment = models.ForeignKey(
        'Equipment', on_delete=models.SET_NULL, null=True, blank=False,
        verbose_name='کالا',
        related_name='history')
    status = models.ForeignKey(
        'BasicInformations.StatusEquipment', on_delete=models.SET_NULL, null=True,
        blank=False, verbose_name='وضعیت')
    location = models.ForeignKey(
        Location, verbose_name="مکان مقصد", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان درج')
    updated = models.DateTimeField(
        auto_now=True, null=True, blank=True, verbose_name='تاریخ و ز مان بروز رسانی')

    class Meta:
        verbose_name = 'تاریخچه'
        verbose_name_plural = 'تاریخچه ها'

    def __str__(self):
        return '{0}'.format(datetime2jalali(
            self.event_date_time).strftime('%y/%m/%d - %H:%M:%S'))

    def clean(self):
        if not self.event_date_time:
            raise ValidationError("تاریخ و زمان رویداد را کامل وارد کنید.")
        return super().clean()
