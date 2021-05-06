import datetime
from itertools import chain

from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import models as db_model
from django.forms.models import BaseInlineFormSet
from django.forms.widgets import NumberInput
from django.urls import reverse
from django.utils.safestring import mark_safe
from jalali_date import date2jalali, datetime2jalali
from jalali_date.admin import ModelAdminJalaliMixin, TabularInlineJalaliMixin

from . import models

HOURS = [(datetime.time(hour=x), '{:02d}:00'.format(x)) for x in range(0, 24)]
HOURS_WITH_HALF = [(datetime.time(hour=x, minute=30),
                    '{:02d}:30'.format(x)) for x in range(0, 24)]
HOUR_CHOICES = list(chain(*zip(HOURS, HOURS_WITH_HALF)))


class EquipmentHistoryInlineFormSet(BaseInlineFormSet):
    def clean(self, *args, **kwargs):
        print(self.instance, self.instance.buy_date)
        for form in self.forms:
            if form.is_valid():
                if form.cleaned_data and form.cleaned_data.get('event_date_time', None):
                    ev_date = form.cleaned_data.get('event_date_time', None)
                    if ev_date.date() <= self.instance.buy_date:
                        form.add_error(
                            'event_date_time',
                            "تاریخ رویداد نمی‌تواند متعاقب تاریخ ایجاد تجهیزات باشد.")
        return super().clean()


class EquipmentHistoryInline(TabularInlineJalaliMixin, admin.TabularInline):
    '''Tabular Inline View for EquipmentHistory'''
    model = models.History
    formset = EquipmentHistoryInlineFormSet
    extra = 1
    autocomplete_fields = ['status', 'location']


@admin.register(models.Equipment)
class EquipmentAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('name', 'location', 'category', 'brand', 'model', 'status',
                    'get_buy_date_jalali', 'order_pdf',
                    'get_created_jalali', 'get_updated_jalali')
    list_filter = ('location', 'category', 'brand', 'buy_date', 'shop',
                   'status', 'level_info', 'created', 'updated')
    search_fields = (
        'deploy_location', 'name', 'description_equipment', 'brand', 'model',
        'serial_number', 'buy_date', 'sis_number', 'charges__amount', 'shop__name',
        'amount', 'imperialistic', 'imperialistic_date', 'ip_address', 'port_number',
        'location__name', 'level_info', 'description', 'created', 'updated')
    ordering = ['created']
    # filter_horizontal = ('charges',)
    autocomplete_fields = ['buyer', 'owner', 'shop',
                           'status', 'location',  'charges', 'depot', 'category']
    # raw_id_fields = ['buy_expert', ]
    inlines = [EquipmentHistoryInline, ]

    formfield_overrides = {
        db_model.IntegerField: {'widget': NumberInput(
            attrs={'style': 'width: 20em;'})},
    }

    def order_pdf(self, obj):
        url = reverse('store:equipment_to_pdf', args=[obj.id])
        return mark_safe(f'<a href="{url}" target="_blank">ایجاد گزارش</a>')
    order_pdf.short_description = 'عملیات'

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created).strftime('%y/%m/%d - %H:%M:%S')
    get_created_jalali.admin_order_field = 'created'
    get_created_jalali.short_description = 'تاریخ و زمان درج'

    def get_updated_jalali(self, obj):
        return datetime2jalali(obj.updated).strftime('%y/%m/%d - %H:%M:%S')
    get_updated_jalali.admin_order_field = 'updated'
    get_updated_jalali.short_description = 'تاریخ و زمان بروز رسانی'

    def get_buy_date_jalali(self, obj):
        return date2jalali(obj.buy_date).strftime('%y/%m/%d')
    get_buy_date_jalali.admin_order_field = 'buy_date'
    get_buy_date_jalali.short_description = 'تاریخ خرید'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(
            location__garrison=request.user.garrison
        ).distinct() if qs.count() >= 1 else qs

    def get_search_results(self, request, queryset, search_term):
        """To filter with regard of JalaliDate"""
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        try:
            search_date = datetime.datetime.strptime(search_term, '%y/%m/%d')
            search_date = search_term
        except ValueError as er:
            pass
        else:
            obj_list = [x.id for x in self.model.objects.all()
                        if datetime2jalali(x.created).strftime('%y/%m/%d') == search_date or
                        datetime2jalali(x.updated).strftime('%y/%m/%d') == search_date
                        ]
            queryset |= self.model.objects.filter(id__in=obj_list)
        return queryset, use_distinct


@admin.register(models.Charge)
class ChargeAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('name', 'amount', 'get_receive_date_jalali',
                    'get_created_jalali', 'get_updated_jalali')
    list_filter = ('amount', 'receive_date', 'created', 'updated')
    search_fields = ('name', 'amount', 'description',
                     'receive_date', 'created', 'updated')
    ordering = ['receive_date']
    autocomplete_fields = ['garrison', ]

    formfield_overrides = {
        db_model.IntegerField: {'widget': NumberInput(
            attrs={'style': 'width: 20em;'})},
    }

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created).strftime('%y/%m/%d - %H:%M:%S')
    get_created_jalali.admin_order_field = 'created'
    get_created_jalali.short_description = 'تاریخ و زمان درج'

    def get_updated_jalali(self, obj):
        return datetime2jalali(obj.updated).strftime('%y/%m/%d - %H:%M:%S')
    get_updated_jalali.admin_order_field = 'updated'
    get_updated_jalali.short_description = 'تاریخ و زمان بروز رسانی'

    def get_receive_date_jalali(self, obj):
        return date2jalali(obj.receive_date).strftime('%y/%m/%d')
    get_receive_date_jalali.admin_order_field = 'receive_date'
    get_receive_date_jalali.short_description = 'تاریخ دریافت اعتبار'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(
            garrison=request.user.garrison
        ).distinct() if qs.count() >= 1 else qs

    def get_search_results(self, request, queryset, search_term):
        """To filter with regard of JalaliDate"""
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        try:
            search_date = datetime.datetime.strptime(search_term, '%y/%m/%d')
            search_date = search_term
        except ValueError as er:
            pass
        else:
            obj_list = [x.id for x in self.model.objects.all()
                        if datetime2jalali(x.created).strftime('%y/%m/%d') == search_date or
                        datetime2jalali(x.updated).strftime('%y/%m/%d') == search_date
                        ]
            queryset |= self.model.objects.filter(id__in=obj_list)
        return queryset, use_distinct


@admin.register(models.Shop)
class ShopAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('name', 'city', 'phone_number',
                    'get_created_jalali', 'get_updated_jalali')
    list_filter = ('city', 'created', 'updated')
    search_fields = (
        'name', 'city__name', 'address', 'phone_number', 'manager_full_name',
        'manager_mobile_number', 'information_security_license', 'samta_license',
        'description', 'created', 'updated')
    ordering = ['created']
    autocomplete_fields = ['city', ]

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created).strftime('%y/%m/%d - %H:%M:%S')
    get_created_jalali.admin_order_field = 'created'
    get_created_jalali.short_description = 'تاریخ و زمان درج'

    def get_updated_jalali(self, obj):
        return datetime2jalali(obj.updated).strftime('%y/%m/%d - %H:%M:%S')
    get_updated_jalali.admin_order_field = 'updated'
    get_updated_jalali.short_description = 'تاریخ و زمان بروز رسانی'

    '''
        اگر لازم بود فروشگاه هم برحسب پایگاه یوزری که داره کار میکنه فیلتر بشه
        اون سه تا کوتیشنی که پایین هستن رو بیارین زیر این متن فارسی تا
        تابع زیر از حالت کامنت دربیاد خودش فیلتر ها رو اعمال میکنه

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(
            equipments__location__garrison=request.user.garrison
        ).distinct() if qs.count() >= 1 else qs
    '''

    def get_search_results(self, request, queryset, search_term):
        """To filter with regard of JalaliDate"""
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        try:
            search_date = datetime.datetime.strptime(search_term, '%y/%m/%d')
            search_date = search_term
        except ValueError as er:
            pass
        else:
            obj_list = [x.id for x in self.model.objects.all()
                        if datetime2jalali(x.created).strftime('%y/%m/%d') == search_date or
                        datetime2jalali(x.updated).strftime('%y/%m/%d') == search_date
                        ]
            queryset |= self.model.objects.filter(id__in=obj_list)
        return queryset, use_distinct


@admin.register(models.Depot)
class DepotAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('name', 'get_created_jalali', 'get_updated_jalali')
    list_filter = ('created', 'updated')
    search_fields = ('name', 'created', 'updated')
    ordering = ['created']
    filter_horizontal = ('zonet_hreats',)
    autocomplete_fields = ['garrison', ]

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created).strftime('%y/%m/%d - %H:%M:%S')
    get_created_jalali.admin_order_field = 'created'
    get_created_jalali.short_description = 'تاریخ و زمان درج'

    def get_updated_jalali(self, obj):
        return datetime2jalali(obj.updated).strftime('%y/%m/%d - %H:%M:%S')
    get_updated_jalali.admin_order_field = 'updated'
    get_updated_jalali.short_description = 'تاریخ و زمان بروز رسانی'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(
            garrison=request.user.garrison
        ).distinct() if qs.count() >= 1 else qs

    def get_search_results(self, request, queryset, search_term):
        """To filter with regard of JalaliDate"""
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        try:
            search_date = datetime.datetime.strptime(search_term, '%y/%m/%d')
            search_date = search_term
        except ValueError as er:
            pass
        else:
            obj_list = [x.id for x in self.model.objects.all()
                        if datetime2jalali(x.created).strftime('%y/%m/%d') == search_date or
                        datetime2jalali(x.updated).strftime('%y/%m/%d') == search_date
                        ]
            queryset |= self.model.objects.filter(id__in=obj_list)
        return queryset, use_distinct


@admin.register(models.History)
class HistoryAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('get_event_date_time_jalali', 'status',
                    'get_created_jalali', 'get_updated_jalali')
    list_filter = ('event_date_time', 'status', 'created', 'updated')
    search_fields = ('event_date_time', 'precept_number', 'created', 'updated')
    ordering = ['event_date_time']
    autocomplete_fields = ['equipment', 'status', 'location']

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created).strftime('%y/%m/%d - %H:%M:%S')
    get_created_jalali.admin_order_field = 'created'
    get_created_jalali.short_description = 'تاریخ و زمان درج'

    def get_updated_jalali(self, obj):
        return datetime2jalali(obj.updated).strftime('%y/%m/%d - %H:%M:%S')
    get_updated_jalali.admin_order_field = 'updated'
    get_updated_jalali.short_description = 'تاریخ و زمان بروز رسانی'

    def get_event_date_time_jalali(self, obj):
        return datetime2jalali(obj.event_date_time).strftime('%y/%m/%d - %H:%M:%S')
    get_event_date_time_jalali.admin_order_field = 'event_date_time'
    get_event_date_time_jalali.short_description = 'تاریخ و زمان بروز رویداد'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(
            equipment__location__garrison=request.user.garrison
        ).distinct() if qs.count() >= 1 else qs

    def get_search_results(self, request, queryset, search_term):
        """To filter with regard of JalaliDate"""
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        try:
            search_date = datetime.datetime.strptime(search_term, '%y/%m/%d')
            search_date = search_term
        except ValueError as er:
            pass
        else:
            obj_list = [x.id for x in self.model.objects.all()
                        if datetime2jalali(x.created).strftime('%y/%m/%d') == search_date or
                        datetime2jalali(x.updated).strftime('%y/%m/%d') == search_date
                        ]
            queryset |= self.model.objects.filter(id__in=obj_list)
        return queryset, use_distinct
