import datetime
from itertools import chain

from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from django.db import models as db_model
from django.forms import Select, Textarea
from django.urls import reverse
from django.utils.safestring import mark_safe
from jalali_date import date2jalali, datetime2jalali
from jalali_date.admin import (ModelAdminJalaliMixin, StackedInlineJalaliMixin,
                               TabularInlineJalaliMixin)

from . import models

HOURS = [(datetime.time(hour=x), '{:02d}:00'.format(x)) for x in range(0, 24)]
HOURS_WITH_HALF = [(datetime.time(hour=x, minute=30),
                    '{:02d}:30'.format(x)) for x in range(0, 24)]
HOUR_CHOICES = list(chain(*zip(HOURS, HOURS_WITH_HALF)))


class PersonalGuardInline(TabularInlineJalaliMixin, admin.TabularInline):
    '''Tabular Inline View for PersonalGuard'''

    model = models.PersonalGuard
    extra = 1
    formfield_overrides = {
        db_model.TextField: {'widget': Textarea(
            attrs={'rows': 8,
                   'cols': 30,
                   'style': 'height: 4rem;'})},
        db_model.TimeField: {
            'widget': Select(choices=HOUR_CHOICES)
        },
    }
    autocomplete_fields = ['personal', 'position']


class SoldierGuardInline(TabularInlineJalaliMixin, admin.TabularInline):
    '''Tabular Inline View for SoldierGuard'''

    model = models.SoldierGuard
    extra = 1
    formfield_overrides = {
        db_model.TextField: {'widget': Textarea(
            attrs={'rows': 4,
                   'cols': 30,
                   'style': 'height: 4rem;'})},
        db_model.TimeField: {
            'widget': Select(choices=HOUR_CHOICES)
        },
    }
    autocomplete_fields = ['soldier', 'position']


@admin.register(models.Position)
class PositionAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    '''Admin View for Position'''

    list_display = ('title', 'get_created_jalali', 'get_updated_jalali')
    list_filter = ('location', 'weapon', 'created', 'updated')
    search_fields = ('title', 'description', 'created', 'updated')
    ordering = ['created']
    autocomplete_fields = ['location', ]

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
            location__garrison=request.user.garrison
        ).distinct() if qs.count() >= 1 else qs

    def get_search_results(self, request, queryset, search_term):
        """To filter with regard of JalaliDate"""
        queryset, use_distinct = super().get_search_results(request,
                                                            queryset, search_term)
        try:
            search_date = datetime.datetime.strptime(search_term, '%y/%m/%d')
            search_date = search_term
        except Exception:
            pass
        else:
            obj_list = [x.id for x in self.model.objects.all()
                        if datetime2jalali(x.created).strftime('%y/%m/%d') == search_date or
                        datetime2jalali(x.updated).strftime('%y/%m/%d') == search_date
                        ]
            queryset |= self.model.objects.filter(id__in=obj_list)
        return queryset, use_distinct


@admin.register(models.PersonalMilitaryPolice)
class PersonalMilitaryPoliceAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    '''Admin View for PersonalMilitaryPolice'''

    list_display = ('personal', 'get_created_jalali', 'get_updated_jalali',)
    list_filter = ('created', 'updated')
    search_fields = ('personal__first_name', 'personal__last_name')
    autocomplete_fields = ['personal', ]

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
            personal__locations__garrison=request.user.garrison
        ).distinct() if qs.count() >= 1 else qs

    def get_search_results(self, request, queryset, search_term):
        """To filter with regard of JalaliDate"""
        queryset, use_distinct = super().get_search_results(request,
                                                            queryset, search_term)
        try:
            search_date = datetime.datetime.strptime(search_term, '%y/%m/%d')
            search_date = search_term
        except Exception:
            pass
        else:
            obj_list = [x.id for x in self.model.objects.all()
                        if datetime2jalali(x.created).strftime('%y/%m/%d') == search_date or
                        datetime2jalali(x.updated).strftime('%y/%m/%d') == search_date
                        ]
            queryset |= self.model.objects.filter(id__in=obj_list)
        return queryset, use_distinct


@admin.register(models.SoldierMilitaryPolice)
class SoldierMilitaryPoliceAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    '''Admin View for SoldierMilitaryPolice'''

    list_display = ('soldier', 'get_created_jalali', 'get_updated_jalali',)
    list_filter = ('created', 'updated')
    search_fields = ('soldier__first_name', 'soldier__last_name')
    autocomplete_fields = ['soldier', ]

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
            soldier__location__garrison=request.user.garrison
        ).distinct() if qs.count() >= 1 else qs

    def get_search_results(self, request, queryset, search_term):
        """To filter with regard of JalaliDate"""
        queryset, use_distinct = super().get_search_results(request,
                                                            queryset, search_term)
        try:
            search_date = datetime.datetime.strptime(search_term, '%y/%m/%d')
            search_date = search_term
        except Exception:
            pass
        else:
            obj_list = [x.id for x in self.model.objects.all()
                        if datetime2jalali(x.created).strftime('%y/%m/%d') == search_date or
                        datetime2jalali(x.updated).strftime('%y/%m/%d') == search_date
                        ]
            queryset |= self.model.objects.filter(id__in=obj_list)
        return queryset, use_distinct


@admin.register(models.GuardTablet)
class GuardTabletAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    '''Admin View for GuardTablet'''

    list_display = ('get_apply_date_jalali', 'get_created_jalali',
                    'get_updated_jalali', 'order_pdf')
    list_filter = ('apply_date', 'created', 'updated')
    search_fields = ('created', 'updated')
    inlines = (PersonalGuardInline, SoldierGuardInline, )

    exclude = ('garrison', )

    def order_pdf(self, obj):
        url = reverse('guard:guardtablet_to_pdf', args=[obj.id])
        return mark_safe(f'<a href="{url}" target="_blank">ایجاد گزارش</a>')
    order_pdf.short_description = 'عملیات'

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.garrison = request.user.garrison
        return super().save_model(request, obj, form, change)

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created).strftime('%y/%m/%d - %H:%M:%S')
    get_created_jalali.admin_order_field = 'created'
    get_created_jalali.short_description = 'تاریخ و زمان درج'

    def get_updated_jalali(self, obj):
        return datetime2jalali(obj.updated).strftime('%y/%m/%d - %H:%M:%S')
    get_updated_jalali.admin_order_field = 'updated'
    get_updated_jalali.short_description = 'تاریخ و زمان بروز رسانی'

    def get_apply_date_jalali(self, obj):
        return date2jalali(obj.apply_date).strftime('%y/%m/%d')
    get_apply_date_jalali.admin_order_field = 'apply_date'
    get_apply_date_jalali.short_description = 'تاریخ'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(
            garrison=request.user.garrison
        ).distinct() if qs.count() >= 1 else qs

    def get_search_results(self, request, queryset, search_term):
        """To filter with regard of JalaliDate"""
        queryset, use_distinct = super().get_search_results(request,
                                                            queryset, search_term)
        try:
            search_date = datetime.datetime.strptime(search_term, '%y/%m/%d')
            search_date = search_term
        except Exception:
            pass
        else:
            obj_list = [x.id for x in self.model.objects.all()
                        if datetime2jalali(x.created).strftime('%y/%m/%d') == search_date or
                        datetime2jalali(x.updated).strftime('%y/%m/%d') == search_date
                        ]
            queryset |= self.model.objects.filter(id__in=obj_list)
        return queryset, use_distinct


# @admin.register(models.PersonalGuard)
class PersonalGuardAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    '''Admin View for PersonalGuard'''

    list_display = ('get_created_jalali', 'get_updated_jalali',)
    list_filter = ('created', 'updated')
    search_fields = ('personal__first_name', 'personal__last_name')
    autocomplete_fields = ['personal', ]

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
            equipments__location__garrison=request.user.garrison
        ).distinct() if qs.count() >= 1 else qs

    def get_search_results(self, request, queryset, search_term):
        """To filter with regard of JalaliDate"""
        queryset, use_distinct = super().get_search_results(request,
                                                            queryset, search_term)
        try:
            search_date = datetime.datetime.strptime(search_term, '%y/%m/%d')
            search_date = search_term
        except Exception:
            pass
        else:
            obj_list = [x.id for x in self.model.objects.all()
                        if datetime2jalali(x.created).strftime('%y/%m/%d') == search_date or
                        datetime2jalali(x.updated).strftime('%y/%m/%d') == search_date
                        ]
            queryset |= self.model.objects.filter(id__in=obj_list)
        return queryset, use_distinct

    def save_model(self, request, obj, form, change):
        if obj.shift_start >= obj.shift_end:
            obj.shift_ends_next_day = True
        return super().save_model(request, obj, form, change)


# @admin.register(models.SoldierGuard)
class SoldierGuardAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    '''Admin View for SolierGuard'''

    list_display = ('get_created_jalali', 'get_updated_jalali',)
    list_filter = ('created', 'updated')
    search_fields = ('soldier__first_name', 'soldier__last_name')
    autocomplete_fields = ['soldier', ]

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
            equipments__location__garrison=request.user.garrison
        ).distinct() if qs.count() >= 1 else qs

    def get_search_results(self, request, queryset, search_term):
        """To filter with regard of JalaliDate"""
        queryset, use_distinct = super().get_search_results(request,
                                                            queryset, search_term)
        try:
            search_date = datetime.datetime.strptime(search_term, '%y/%m/%d')
            search_date = search_term
        except Exception:
            pass
        else:
            obj_list = [x.id for x in self.model.objects.all()
                        if datetime2jalali(x.created).strftime('%y/%m/%d') == search_date or
                        datetime2jalali(x.updated).strftime('%y/%m/%d') == search_date
                        ]
            queryset |= self.model.objects.filter(id__in=obj_list)
        return queryset, use_distinct

    def save_model(self, request, obj, form, change):
        if obj.shift_start >= obj.shift_end:
            obj.shift_ends_next_day = True
        return super().save_model(request, obj, form, change)
