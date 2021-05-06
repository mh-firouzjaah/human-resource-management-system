# -*- coding: utf-8 -*-
import datetime

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Garrison(models.Model):
    name = models.CharField(max_length=60, null=False, blank=False,
                            verbose_name='نام پایگاه', unique=True)
    city = models.ForeignKey(
        'BasicInformations.City', on_delete=models.SET_NULL, null=True, blank=False,
        verbose_name='شهر مربوطه')
    zonet_hreats = models.ManyToManyField(
        'BasicInformations.ZonetHreat', verbose_name='تهدیدات منطقه ای', blank=True)
    mp = models.IntegerField(null=False, blank=False,
                             verbose_name='متراژ پیرامونی', unique=False)
    mf = models.IntegerField(null=False, blank=False,
                             verbose_name='متراژ فنس', unique=False)
    md = models.IntegerField(null=False, blank=False,
                             verbose_name='متراژ دیوار', unique=False)
    mbv = models.IntegerField(null=False, blank=False,
                              verbose_name='متراژ موانع', unique=False)
    longitude = models.CharField(max_length=10, null=True,
                                 blank=True, verbose_name='طول جغرافیایی')
    latitude = models.CharField(max_length=10, null=True,
                                blank=True, verbose_name='عرض جغرافیایی')
    map_image = models.ImageField(
        null=True, blank=True, verbose_name='تصویر نقشه',
        upload_to='UploadFiles\Images\MapsOfGarrison')
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات تکمیلی')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان درج')
    updated = models.DateTimeField(
        auto_now=True, null=True, blank=True, verbose_name='تاریخ و زمان بروز رسانی')

    class Meta:
        verbose_name = 'پایگاه'
        verbose_name_plural = 'پایگاه ها'

    def __str__(self):
        return 'پایگاه {0}'.format(self.name)


class LocationCategory(models.Model):
    name = models.CharField(max_length=60, null=False, blank=False,
                            verbose_name='نام', unique=True)
    icon = models.ImageField(
        null=False, blank=False, verbose_name='نماد دسته بندی مکان',
        upload_to='UploadFiles\Images\IconsOfLocationCategories')
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات تکمیلی')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان درج')
    updated = models.DateTimeField(
        auto_now=True, null=True, blank=True, verbose_name='تاریخ و زمان بروز رسانی')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی های مکان ها'

    def __str__(self):
        return '{0}'.format(self.name)


class Location(models.Model):
    name = models.CharField(max_length=120, null=False, blank=False, verbose_name='نام')
    garrison = models.ForeignKey(
        'Garrison', on_delete=models.SET_NULL, null=True, blank=False,
        verbose_name='پایگاه')
    category = models.ForeignKey(
        'LocationCategory', on_delete=models.SET_NULL, null=True, blank=False,
        verbose_name='دسته بندی',
        related_name='locations')
    phone_number = models.CharField(
        max_length=11, null=True, blank=True, verbose_name='شماره تلفن')
    image = models.ImageField(
        null=True, blank=True, verbose_name='تصویر',
        upload_to='UploadFiles\Images\Locations')
    # liable = models.ForeignKey(
    #     'Personal', verbose_name=_('مسئول مکان'),
    #     on_delete=models.SET_NULL,
    #     null=True, blank=True)
    liable = models.CharField(max_length=60, null=False, verbose_name='مسئول مکان')
    longitude = models.CharField(max_length=10, null=True,
                                 blank=True, verbose_name='طول جغرافیایی',)
    latitude = models.CharField(max_length=10, null=True,
                                blank=True, verbose_name='عرض جغرافیایی')
    zonet_hreats = models.ManyToManyField(
        'BasicInformations.ZonetHreat', verbose_name='تهدیدات منطقه ای', blank=True)
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات تکمیلی')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان درج')
    updated = models.DateTimeField(
        auto_now=True, null=True, blank=True, verbose_name='تاریخ و زمان بروز رسانی')
    pass

    class Meta:
        verbose_name = 'مکان'
        verbose_name_plural = 'مکان ها'
        # ordering = ["-my-field-name"]

    def __str__(self):
        return 'مکان {0} در {1}'.format(self.name, self.garrison)


class EnvironsInformation(models.Model):
    title = models.CharField(max_length=60, null=False, blank=False, verbose_name='عنوان')
    garrison = models.ForeignKey(
        'Garrison', on_delete=models.SET_NULL, null=True, blank=False,
        verbose_name='پایگاه')
    address = models.TextField(null=True, blank=True, verbose_name='آدرس')
    phone_number = models.CharField(
        max_length=11, null=True, blank=True, verbose_name='شماره تلفن')
    longitude = models.CharField(max_length=10, null=True,
                                 blank=True, verbose_name='طول جغرافیایی')
    latitude = models.CharField(max_length=10, null=True,
                                blank=True, verbose_name='عرض جغرافیایی')
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات تکمیلی')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان درج')
    updated = models.DateTimeField(
        auto_now=True, null=True, blank=True, verbose_name='تاریخ و زمان بروز رسانی')
    pass

    class Meta:
        verbose_name = 'اطلاعات حومه'
        verbose_name_plural = 'اطلاعات حومه'
        # ordering = ["-my-field-name"]

    def __str__(self):
        return '{0} در حومه {1}'.format(self.title, self.garrison)


class Event(models.Model):
    # garrison = models.ForeignKey(
    #    'Garrison', on_delete=models.SET_NULL, null=True, blank=False,
    #    verbose_name='پایگاه')
    category = models.ForeignKey(
        'BasicInformations.EventCategory', on_delete=models.SET_NULL, null=True,
        blank=False, verbose_name='دسته بندی')

    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True, blank=False,
        verbose_name='مکان')
    date = models.DateField(max_length=60, null=False,
                            blank=False, verbose_name='تاریخ وقوع')
    time = models.TimeField(max_length=60, null=True,
                            blank=True, verbose_name='زمان وقوع')
    personal = models.ForeignKey(
        'Personal', verbose_name=_('پایور'),
        on_delete=models.SET_NULL,
        null=True, blank=True)
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات تکمیلی')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان درج')
    updated = models.DateTimeField(
        auto_now=True, null=True, blank=True, verbose_name='تاریخ و زمان بروز رسانی')
    pass

    class Meta:
        verbose_name = 'رویداد فیزیکی'
        verbose_name_plural = 'رویداد های فیزیکی'
        # ordering = ["-my-field-name"]

    def __str__(self):
        return '{0}'.format(self.category)


# -*- coding: utf-8 -*-


numeric = RegexValidator(r'^[0-9]*$', 'فقط عدد وارد کنید.')
min_length11 = RegexValidator(r'^.{11}$', "تعداد ارقام کافی نیست")
national_code_length = RegexValidator(r'^.{10}$', "کد ملی بایستی ده رقم باشد")
# for any charfield which has to be filled integer use this: validators=[numeric,]


class Personal(models.Model):
    personalCode = models.CharField(verbose_name='کد پایوری', validators=[numeric, ],
                                    max_length=10,  unique=True)
    nationalCode = models.CharField(
        verbose_name='کد ملی', validators=[numeric, national_code_length],
        max_length=10, null=True, unique=True)
    chevron = models.ForeignKey('BasicInformations.Chevron', on_delete=models.SET_NULL,
                                null=True, blank=False, verbose_name='درجه',
                                related_name='chevron_personal')
    level = models.ForeignKey('BasicInformations.Chevron', on_delete=models.SET_NULL,
                              null=True, blank=True, verbose_name='جایگاه',
                              related_name='levels_personal')
    locations = models.ManyToManyField(
        'Garrisons.Location', verbose_name='مکان ها',
        help_text='مشخص کنید در کدام مکان(ها)، فعال است.')
    first_name = models.CharField(max_length=60, null=True, verbose_name='نام')
    last_name = models.CharField(max_length=60, null=True, verbose_name='نشان')
    skill = models.ForeignKey(
        'BasicInformations.Skill', on_delete=models.SET_NULL, null=True, blank=False,
        verbose_name='تخصص و رسته')

    # جایگاه
    # level = models.ForeignKey(Chevron, on_delete = models.SET_NULL, null = True, blank = False, verbose_name = 'جایگاه')

    jobSubject = models.CharField(max_length=60, null=True, verbose_name='عنوان شغلی')
    actionJob = models.CharField(max_length=60, null=True, verbose_name='شغل عملی')
    phoneNumber = models.CharField(verbose_name='شماره تلفن منزل',
                                   max_length=11, null=True, validators=[numeric, ],)
    mobile_phone_number = models.CharField(
        max_length=11, verbose_name='شماره تلفن همراه', validators=[numeric, ],)
    address = models.TextField(null=True, blank=True, verbose_name='آدرس محل سکونت')
    office_phone_number = models.CharField(max_length=11, verbose_name='شماره تلفن اداری',
                                           validators=[numeric, ],)
    is_buy_expert = models.BooleanField(
        max_length=60, null=True, verbose_name='کارشناس خرید')
    is_buyer = models.BooleanField(max_length=60, null=True, verbose_name='عامل خرید')
    image = models.ImageField(
        null=True, blank=True, verbose_name='تصویر',
        upload_to='UploadFiles\Images\Personals')
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات تکمیلی')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان درج')
    updated = models.DateTimeField(
        auto_now=True, null=True, verbose_name='تاریخ و زمان بروز رسانی')

    class Meta:
        verbose_name = 'پایور'
        verbose_name_plural = 'پایوران'

    def __str__(self):
        return f'{self.chevron} {self.first_name} { self.last_name} - {self.personalCode}'

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'


class Soldier(models.Model):
    BULK_STATE_CHOICES = (
        ('A', 'کاملا سالم'),
        ('F', 'معاف از رزم'),
        ('B', 'مشکل از ناحیه دست'),
        ('C', 'مشکل از ناحیه پا'),
        ('D', 'دارای میگرن'),
        ('E', 'دارای بیماری خاص'),
        ('G', 'دیگر'),
    )
    PSYCHE_STATE_CHOICES = (
        ('A', 'گروه الف'),
        ('B', 'گروه ب'),
        ('C', 'گروه ب معاف از رزم'),
    )
    ACADEMIC_FIELD_CHOICES = (
        ('A', 'کامپیوتر'),
        ('B', 'الکترونیک'),
        ('C', 'شیمی'),
        ('C', 'مکانیک'),
        ('C', 'برق'),
        ('C', 'الهیات'),
        ('C', 'معماری'),
        ('C', 'حقوق'),
        ('C', 'ادبیات'),
        ('C', 'ریاضی'),
        ('C', 'حسابداری'),
        ('C', 'متالوژی'),
    )
    ACADEMIC_LEVEL_CHOICES = (
        ('A', 'زیر دیپلم'),
        ('B', 'دیپلم'),
        ('C', 'فوق دیپلم'),
        ('C', 'لیسانس'),
        ('C', 'فوق لیسانس'),
        ('C', 'دکتری'),
        ('C', 'دکتری تخصصی')
    )
    national_code = models.CharField(max_length=10,
                                     null=False, verbose_name='کد ملی', unique=True,
                                     validators=[numeric, national_code_length])
    first_name = models.CharField(
        max_length=60, verbose_name='نام')
    last_name = models.CharField(
        max_length=60, verbose_name='نشان')
    father_name = models.CharField(
        max_length=60, verbose_name='نام پدر')
    academic_level = models.CharField(
        max_length=60, null=True, blank=True, choices=ACADEMIC_LEVEL_CHOICES, default='A',
        verbose_name='مقطع تحصیلاات')
    academic_field = models.ForeignKey(
        'BasicInformations.AcademicField', verbose_name='رشته تحصیلی',
        on_delete=models.SET_NULL, null=True, blank=True,)
    city = models.ForeignKey(
        'BasicInformations.City', on_delete=models.SET_NULL, null=True, blank=False,
        verbose_name='شهر محل زندگی')
    street = models.CharField(null=True, blank=True, max_length=60, verbose_name='خیابان')
    precision_address = models.TextField(null=True, blank=True, verbose_name='آدرس دقیق')
    phone_number = models.CharField(verbose_name='شماره تلفن همراه',
                                    max_length=11, null=True, blank=True,
                                    validators=[numeric, min_length11])
    home_phone_number = models.CharField(verbose_name='شماره تلفن منزل',
                                         null=True, blank=True, max_length=11,
                                         validators=[numeric, ])
    father_phone_number = models.CharField(verbose_name='شماره تلفن همراه پدر',
                                           null=True, blank=True, max_length=11,
                                           validators=[numeric, min_length11])
    mother_phone_number = models.CharField(verbose_name='شماره تلفن همراه مادر',
                                           null=True, blank=True, max_length=11,
                                           validators=[numeric, min_length11])
    dispatch_date = models.DateField(verbose_name='تاریخ اعزام')
    station = models.PositiveSmallIntegerField(verbose_name='شماره مرحله',
                                               validators=[MinValueValidator(1), ])
    chevron = models.ForeignKey('BasicInformations.Chevron', on_delete=models.SET_NULL,
                                null=True, blank=False, verbose_name='درجه')
    skill = models.ForeignKey(
        'BasicInformations.Skill', on_delete=models.SET_NULL, null=True, blank=False,
        verbose_name='تخصص و رسته')

    location = models.ForeignKey(
        'Garrisons.Location', on_delete=models.SET_NULL, null=True, blank=False,
        verbose_name='واحد مشغول به کار')
    bulk_state = models.CharField(
        max_length=60, choices=BULK_STATE_CHOICES, default='A',
        verbose_name='وضعیت جسمانی')
    psyche_state = models.CharField(
        max_length=60, choices=BULK_STATE_CHOICES, default='A',
        verbose_name='وضعیت عقلانی و روانی')
    is_married = models.BooleanField(verbose_name='متاهل')
    child_count = models.PositiveSmallIntegerField(verbose_name='تعداد عائله',
                                                   null=True, blank=True,
                                                   validators=[MinValueValidator(1), ])
    image = models.ImageField(
        null=True, blank=True, verbose_name='تصویر',
        upload_to='UploadFiles\Images\Soldiers')
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات تکمیلی')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان درج')
    updated = models.DateTimeField(
        auto_now=True, null=True, verbose_name='تاریخ و زمان بروز رسانی')

    class Meta:
        verbose_name = 'وظیفه'
        verbose_name_plural = 'وظیفه ها'

    def __str__(self):
        return f'{self.chevron} و {self.first_name} { self.last_name} - {self.national_code}'

    def get_ful_name(self):
        return f'{self.first_name} {self.last_name}'


class PersonalLearnCourse(models.Model):
    title = models.CharField(max_length=60, null=False,
                             verbose_name='عنوان دوره')
    personal = models.ForeignKey(
        "Personal", verbose_name='پایور', on_delete=models.SET_NULL, null=True,
        blank=False, related_name="learned_courses")
    start = models.DateField(null=True, verbose_name='تاریخ شروع')
    end = models.DateField(null=True, verbose_name='تاریخ اتمام')
    point = models.PositiveSmallIntegerField(null=True, verbose_name='امتیاز',
                                             validators=[MinValueValidator(1), ])
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان درج')
    updated = models.DateTimeField(
        auto_now=True, null=True, verbose_name='تاریخ و ز مان بروز رسانی')

    class Meta:
        verbose_name = 'دوره طی شده پایور'
        verbose_name_plural = 'دوره های طی شده پایوران'

    def __str__(self):
        return f'{self.title}'

    def clean(self):
        '''Ensure that dates are regular'''
        super().clean()
        if self.start and self.end:
            if self.start >= self.end:
                raise ValidationError(
                    "تاریخ شروع نمی‌تواند همزمان یا متعاقب تاریخ پایان باشد.")


class SoldierLearnCourse(models.Model):
    title = models.CharField(max_length=60, null=False, verbose_name='عنوان دوره')
    soldier = models.ForeignKey(
        Soldier, related_name="learned_courses", verbose_name='وظیفه',
        on_delete=models.CASCADE)
    start = models.DateField(verbose_name='تاریخ شروع')
    end = models.DateField(verbose_name='تاریخ اتمام')
    point = models.PositiveSmallIntegerField(null=True, verbose_name='امتیاز',
                                             validators=[MinValueValidator(1), ])
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان درج')
    updated = models.DateTimeField(
        auto_now=True, null=True, verbose_name='تاریخ و ز مان بروز رسانی')

    class Meta:
        verbose_name = 'دوره طی شده وظیفه'
        verbose_name_plural = 'دوره های طی شده وظیفه ها'

    def __str__(self):
        return f'{self.title}'

    def clean(self):
        '''Ensure that dates are regular'''
        if self.start and self.end:
            if self.start >= self.end:
                raise ValidationError(
                    "تاریخ شروع نمی‌تواند همزمان یا متعاقب تاریخ پایان باشد.")
        return super().clean()

# class BuyExpert(models.Model):
    #     personal = models.ForeignKey('Personal', on_delete = models.SET_NULL, null = True, blank = False, verbose_name = 'پایور')
    #     created = models.DateTimeField(auto_now_add = True, verbose_name = 'تاریخ و زمان درج')
    #     updated = models.DateTimeField(auto_now = True, null = True, verbose_name = 'تاریخ و ز مان بروز رسانی')
    #     class Meta:
    #         verbose_name = 'کارشناس خرید'
    #         verbose_name_plural = 'کارشناس های خرید'

# class Buyer(models.Model):
    #     personal = models.ForeignKey('Personal', on_delete = models.SET_NULL, null = True, blank = False, verbose_name = 'پایور')
    #     created = models.DateTimeField(auto_now_add = True, verbose_name = 'تاریخ و زمان درج')
    #     updated = models.DateTimeField(auto_now = True, null = True, verbose_name = 'تاریخ و زمان بروز رسانی')
    #     class Meta:
    #         verbose_name = 'عامل خرید'
    #         verbose_name_plural = 'عوامل خرید'


class Owner(models.Model):
    personal = models.ForeignKey(
        'Personal', on_delete=models.SET_NULL, null=True, blank=False,
        verbose_name='پایور')
    garrison = models.ForeignKey(
        'Garrisons.Garrison', on_delete=models.SET_NULL, null=True, blank=False,
        verbose_name='پایگاه')
    # equipments = models.ManyToManyField(Equipment, verbose_name = 'تجهیزات مربوطه')
    owner_code = models.CharField(max_length=10, null=False,
                                  verbose_name='کد ذی حسابی', unique=True)
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات تکمیلی')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان درج')
    updated = models.DateTimeField(
        auto_now=True, null=True, verbose_name='تاریخ و زمان بروز رسانی')

    class Meta:
        verbose_name = 'ذی حساب'
        verbose_name_plural = 'ذی حساب ها'

    def __str__(self):
        return '{0}'.format(self.personal)


class Diminution(models.Model):
    SPARE_CHOICES = (
        ('C', 'انجام پروژه قبل از خدمت'),
        ('D', 'انجام پروژه در حال خدمت'),
        ('A', 'نظامی بودن پدر'),
        ('F', 'وضعیت جسمانی'),
        ('B', 'فعالیت در بسیج'),
        ('E', 'تشویقی فرمانده'),
        ('G', 'دیگر'),
    )
    soldier = models.ForeignKey(
        'Soldier', related_name='diminutions', on_delete=models.SET_NULL, null=True,
        blank=False, verbose_name='وظیفه')
    day_count = models.PositiveSmallIntegerField(verbose_name='تعداد روز',
                                                 validators=[MinValueValidator(1), ])
    spare = models.CharField(max_length=60,
                             choices=SPARE_CHOICES, default='B', verbose_name='دلیل')
    register_date_time = models.DateField(verbose_name='تاریخ ثبت')
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات تکمیلی')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان درج')
    updated = models.DateTimeField(
        auto_now=True, null=True, verbose_name='تاریخ و زمان بروز رسانی')

    class Meta:
        verbose_name = 'کسری خدمت وظیفه'
        verbose_name_plural = 'کسری خدمت وظیفه ها'

    def __str__(self):
        return 'کسری خدمت وظیفه {0}'.format(self.soldier)


class PersonalCard(models.Model):
    personal = models.ForeignKey(
        'Personal', on_delete=models.SET_NULL, null=True, blank=False,
        verbose_name='پایور', related_name="cards")
    card = models.ForeignKey('BasicInformations.Card', on_delete=models.SET_NULL,
                             null=True, blank=False, verbose_name='کارت')
    register_date = models.DateField(
        verbose_name='تاریخ صدور')
    exp_date = models.DateField(
        verbose_name='تاریخ اتمام اعتبار')
    number = models.CharField(max_length=60, null=True, blank=True,
                              verbose_name='شماره نامه', unique=True)
    is_active = models.BooleanField(
        default=False, verbose_name='ابطال دستی')
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات تکمیلی')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان درج')
    updated = models.DateTimeField(
        auto_now=True, null=True, verbose_name='تاریخ و زمان بروز رسانی')

    class Meta:
        verbose_name = 'کارت پایور'
        verbose_name_plural = 'کارت های پایوران'

    def __str__(self):
        return '{0} برای {1}'.format(self.card, self.personal)

    def clean(self):
        '''Ensure that dates are regular'''
        if self.register_date and self.exp_date:
            if self.register_date >= self.exp_date:
                raise ValidationError(
                    "تاریخ صدور نمی‌تواند همزمان یا متعاقب تاریخ اتمام اعتبار باشد.")
        return super().clean()


class SoldierCard(models.Model):
    soldier = models.ForeignKey(
        'Soldier', on_delete=models.SET_NULL, null=True, blank=False,
        verbose_name='وظیفه', related_name="cards")
    card = models.ForeignKey('BasicInformations.Card', on_delete=models.SET_NULL,
                             null=True, blank=False, verbose_name='کارت')
    register_date = models.DateField(
        verbose_name='تاریخ صدور')
    exp_date = models.DateField(
        verbose_name='تاریخ اتمام اعتبار')
    number = models.CharField(max_length=60, null=True, blank=True,
                              verbose_name='شماره نامه', unique=True)
    is_active = models.BooleanField(
        default=False, verbose_name='ابطال دستی')
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات تکمیلی')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان درج')
    updated = models.DateTimeField(
        auto_now=True, null=True, verbose_name='تاریخ و زمان بروز رسانی')

    class Meta:
        verbose_name = 'کارت وظیفه'
        verbose_name_plural = 'کارت های وظیفه'

    def __str__(self):
        return '{0} برای {1}'.format(self.card, self.soldier)

    def clean(self):
        '''Ensure that dates are regular'''
        if self.register_date and self.exp_date:
            if self.register_date >= self.exp_date:
                raise ValidationError(
                    "تاریخ صدور نمی‌تواند همزمان یا متعاقب تاریخ اتمام اعتبار باشد.")
        return super().clean()


class Chastise(models.Model):
    personal = models.ForeignKey(
        'Personal', on_delete=models.SET_NULL, null=True, blank=False,
        verbose_name='پایور')
    doorkeeper = models.ForeignKey('Personal', on_delete=models.SET_NULL, null=True,
                                   blank=True, verbose_name='آمر',
                                   related_name='doorkeeper_personal_chastise')
    reason = models.TextField(verbose_name='علت')
    register_date = models.DateField(
        verbose_name='تاریخ ثبت')
    sentence = models.TextField(null=True, blank=True, verbose_name='حکم')
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات تکمیلی')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان درج')
    updated = models.DateTimeField(
        auto_now=True, null=True, verbose_name='تاریخ و زمان بروز رسانی')

    class Meta:
        verbose_name = 'تنبیه پایور'
        verbose_name_plural = 'تنبیهات پایور'

    def __str__(self):
        return 'تنبیه برای پایور {0}'.format(self.personal)


class Surplus(models.Model):
    soldier = models.ForeignKey(
        'Soldier', related_name='surpluses', on_delete=models.SET_NULL, null=True,
        blank=False, verbose_name='وظیفه')
    personal = models.ForeignKey(
        'Personal', on_delete=models.SET_NULL, null=True, blank=False,
        verbose_name='آمر')
    reporter = models.CharField(max_length=60, null=False,
                                blank=True, verbose_name='گزارش دهنده')
    register_date = models.DateField(
        verbose_name='تاریخ ثبت')
    reason = models.TextField(verbose_name='علت')
    day_count = models.PositiveSmallIntegerField(verbose_name='تعداد روز',
                                                 validators=[MinValueValidator(1), ])
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات تکمیلی')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان درج')
    updated = models.DateTimeField(
        auto_now=True, null=True, verbose_name='تاریخ و زمان بروز رسانی')

    class Meta:
        verbose_name = 'اضافه خدمت وظیفه'
        verbose_name_plural = 'اضافات خدمت وظیفه ها'

    def __str__(self):
        return 'اضافه خدمت برای وظیفه {0}'.format(self.soldier)


class MobilePortagePersonal(models.Model):
    personal = models.ForeignKey(
        'Personal', on_delete=models.SET_NULL, null=True, blank=False,
        verbose_name='پایور')
    register_date = models.DateField(
        verbose_name='تاریخ ثبت')
    doorkeeper = models.ForeignKey('Personal', on_delete=models.SET_NULL, null=True,
                                   blank=True, verbose_name='شخص توقیف کننده',
                                   related_name='doorkeeper_personal')
    location = models.ForeignKey(
        'Garrisons.Location', on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='محل توقیف')
    model = models.TextField(verbose_name='شی یا اشیا')
    smart = models.BooleanField(verbose_name='هوشمند')
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات تکمیلی')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان درج')
    updated = models.DateTimeField(
        auto_now=True, null=True, verbose_name='تاریخ و زمان بروز رسانی')

    class Meta:
        verbose_name = 'حمل غیرمجاز شی توسط پایور'
        verbose_name_plural = 'حمل غیرمجاز اشیا توسط پایوران'

    def __str__(self):
        return 'حمل غیرمجاز گوشی تلفن توسط پایور {0}'.format(self.personal)


class MobilePortage(models.Model):
    soldier = models.ForeignKey(
        'Soldier', related_name='mobile_portages', on_delete=models.SET_NULL, null=True,
        blank=False, verbose_name='وظیفه')
    register_date = models.DateField(
        verbose_name='تاریخ ثبت')
    day_count = models.PositiveSmallIntegerField(verbose_name='تعداد روز اضافه خدمت',
                                                 validators=[MinValueValidator(1), ],
                                                 default=0,)
    doorkeeper = models.ForeignKey('Personal', on_delete=models.SET_NULL, null=True,
                                   blank=True, verbose_name='شخص توقیف کننده')
    location = models.ForeignKey(
        'Garrisons.Location', on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='محل توقیف')
    model = models.TextField(verbose_name='اشیا')
    smart = models.BooleanField(verbose_name='هوشمند')
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات تکمیلی')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان درج')
    updated = models.DateTimeField(
        auto_now=True, null=True, verbose_name='تاریخ و زمان بروز رسانی')

    class Meta:
        verbose_name = 'حمل غیرمجاز شی توسط وظیفه'
        verbose_name_plural = 'حمل غیرمجاز اشیا توسط وظیفه ها'

    def __str__(self):
        return 'حمل غیرمجاز شی توسط وظیفه {0}'.format(self.soldier)


class Volatile(models.Model):
    soldier = models.ForeignKey(
        'Soldier', related_name='volatiles', on_delete=models.SET_NULL, null=True,
        blank=False, verbose_name='وظیفه')
    start_date = models.DateField(
        verbose_name='تاریخ شروع')
    end_date = models.DateField(
        verbose_name='تاریخ پایان')
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات تکمیلی')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان درج')
    updated = models.DateTimeField(
        auto_now=True, null=True, verbose_name='تاریخ و زمان بروز رسانی')

    class Meta:
        verbose_name = 'فرار وظیفه'
        verbose_name_plural = 'فرار وظیفه ها'

    def __str__(self):
        return 'فرار وظیفه {0}'.format(self.soldier)

    def day_count(self):
        return (self.end_date - self.start_date).days

    def clean(self):
        '''Ensure that dates are regular'''
        super().clean()
        if (self.start_date >= self.end_date):
            raise ValidationError(
                "تاریخ شروع نمی‌تواند همزمان یا متعاقب تاریخ پایان باشد.")


class Absence(models.Model):
    soldier = models.ForeignKey(
        'Soldier', related_name='absences', on_delete=models.SET_NULL, null=True,
        blank=False, verbose_name='وظیفه')
    start_date = models.DateField(
        verbose_name='تاریخ شروع')
    end_date = models.DateField(
        verbose_name='تاریخ پایان')
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات تکمیلی')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان درج')
    updated = models.DateTimeField(
        auto_now=True, null=True, verbose_name='تاریخ و زمان بروز رسانی')

    class Meta:
        verbose_name = 'نهست'
        verbose_name_plural = 'نهست ها'

    def __str__(self):
        return 'نهست وظیفه {0}'.format(self.soldier)

    def day_count(self):
        return (self.end_date - self.start_date).days

    def clean(self):
        '''Ensure that dates are regular'''
        super().clean()
        if (self.start_date >= self.end_date):
            raise ValidationError(
                "تاریخ شروع نمی‌تواند همزمان یا متعاقب تاریخ پایان باشد.")


class Prison(models.Model):
    soldier = models.ForeignKey(
        'Soldier', related_name='imprisonments', on_delete=models.SET_NULL, null=True,
        blank=False, verbose_name='وظیفه')
    reason = models.CharField(max_length=128, verbose_name='علت')
    day_count = models.PositiveSmallIntegerField(verbose_name='تعداد روز اضافه خدمت',
                                                 validators=[MinValueValidator(1), ])
    receipt = models.CharField(verbose_name='دریافت شده توسط',
                               max_length=128, )
    precept_number = models.CharField(verbose_name='شماره امریه',
                                      max_length=60,  unique=True)
    location = models.CharField(verbose_name='محل بازداشت',
                                max_length=128, )
    doorkeeper = models.CharField(max_length=60, null=False,
                                  blank=True, verbose_name='پلیس هوایی')
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات تکمیلی')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان درج')
    updated = models.DateTimeField(verbose_name='تاریخ و زمان بروز رسانی',
                                   auto_now=True, null=True, )

    class Meta:
        verbose_name = 'بازداشت وظیفه'
        verbose_name_plural = 'بازداشت وظیفه ها'

    def __str__(self):
        return 'بازداشت وظیفه {0}'.format(self.soldier)


class PrisonPersonal(models.Model):
    personal = models.ForeignKey(
        'Personal', on_delete=models.SET_NULL, null=True, blank=False,
        verbose_name='پایور')
    reason = models.CharField(max_length=128, verbose_name='علت')
    receipt = models.CharField(
        max_length=128, verbose_name='دریافت شده توسط')
    precept_number = models.CharField(
        max_length=60, verbose_name='شماره امریه', unique=True)
    location = models.CharField(
        max_length=128, verbose_name='محل بازداشت')
    doorkeeper = models.CharField(max_length=60, null=False,
                                  blank=True, verbose_name='پلیس هوایی')
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات تکمیلی')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان درج')
    updated = models.DateTimeField(
        auto_now=True, null=True, verbose_name='تاریخ و زمان بروز رسانی')

    class Meta:
        verbose_name = 'بازداشت پایور'
        verbose_name_plural = 'بازداشت پایوران'

    def __str__(self):
        return 'بازداشت پایور {0}'.format(self.personal)


class Recess(models.Model):
    TYPEREC_CHOICES = (
        ('A', 'استحقاقی'),
        ('B', 'تشویقی'),
        ('C', 'دیگر'),
    )
    soldier = models.ForeignKey(
        'Soldier', related_name='recesses', on_delete=models.SET_NULL, null=True,
        blank=False, verbose_name='وظیفه')
    day_count = models.PositiveSmallIntegerField(verbose_name='تعداد روز',
                                                 validators=[MinValueValidator(1), ])
    typerec = models.CharField(
        max_length=60, choices=TYPEREC_CHOICES, default='B',
        verbose_name='نوع')
    receipt = models.ForeignKey(Personal, verbose_name='دریافت شده توسط',
                                on_delete=models.SET_NULL, null=True, blank=True)
    reason = models.CharField(null=True, blank=True,
                              max_length=128, verbose_name='علت دریافت')
    precept_number = models.CharField(
        max_length=60, null=True, blank=True, verbose_name='شماره نامه', unique=True)
    date = models.DateField(null=True, blank=True, verbose_name='تاریخ ثبت')
    use = models.BooleanField(verbose_name='استفاده شده')
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات تکمیلی')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان درج')
    updated = models.DateTimeField(
        auto_now=True, null=True, verbose_name='تاریخ و زمان بروز رسانی')

    class Meta:
        verbose_name = 'مرخصی'
        verbose_name_plural = 'مرخصی ها'

    def __str__(self):
        return 'مرخصی وظیفه {0}'.format(self.soldier)


class GoRecess(models.Model):
    TYPEREC_CHOICES = (
        ('A', 'استحقاقی'),
        ('B', 'تشویقی'),
        ('C', 'دیگر'),
    )
    soldier = models.ForeignKey('Soldier',
                                related_name='gone_recesses',
                                verbose_name='وظیفه',
                                null=True, blank=False,
                                on_delete=models.SET_NULL)
    day_count = models.PositiveSmallIntegerField(verbose_name='تعداد روز',
                                                 validators=[MinValueValidator(1), ])
    typerec = models.CharField(choices=TYPEREC_CHOICES,
                               max_length=60,  default='B',
                               verbose_name='نوع')
    start_date = models.DateField(verbose_name='از تاریخ')
    end_date = models.DateField(verbose_name='تا تاریخ')
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات تکمیلی')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان درج')
    updated = models.DateTimeField(verbose_name='تاریخ و زمان بروز رسانی',
                                   auto_now=True, null=True, )

    class Meta:
        verbose_name = 'مرخصی رفته'
        verbose_name_plural = 'مرخصی های رفته'

    def __str__(self):
        return 'مرخصی رفته وظیفه {0}'.format(self.soldier)

    def clean(self):
        '''Ensure that dates are regular'''
        super().clean()
        if (self.start_date >= self.end_date):
            raise ValidationError(
                "تاریخ شروع نمی‌تواند همزمان یا متعاقب تاریخ پایان باشد.")

        if self.end_date != self.start_date + datetime.timedelta(days=self.day_count):
            raise ValidationError(
                "تاریخ پایان با توجه به تعداد روز درست نمی‌باشد.")

        total_available_recesses = sum([x.day_count for x in self.soldier.recesses.all()])
        total_gone_recesses = sum([x.day_count for x in self.soldier.gone_recesses.all()])

        if self.id:
            total_gone_recesses = sum([x.day_count
                                       for x in self.soldier.gone_recesses.exclude(
                                           id=self.id)])

        total_leftover = total_available_recesses - total_gone_recesses

        if self.day_count > total_leftover:
            raise ValidationError(
                "تعداد روزهای مرخصی رفته از مجموع مرخصی‌های باقی‌مانده وظیفه بیشتر خواهد شد.")
