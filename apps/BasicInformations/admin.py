import datetime

from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.db import models as db_model
from django.forms.widgets import NumberInput
from jalali_date import date2jalali, datetime2jalali
from jalali_date.admin import ModelAdminJalaliMixin

from . import models


class CreationDateFilter(SimpleListFilter):
    title = 'تاریخ و زمان درج'
    parameter_name = 'created'

    def lookups(self, request, model_admin):
        created_set = set(
            [obj
             for obj in model_admin.model.objects.order_by(
                 'created__date').distinct('created__date')
             ])
        return [
            (obj.id,  date2jalali(obj.created).strftime('%y/%m/%d'))
            for obj in created_set]

    def queryset(self, request, queryset):
        if self.value():
            return [x for x in queryset if datetime2jalali(x.created) == self.value()]


@admin.register(models.State)
class StateAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('name', 'get_created_jalali', 'get_updated_jalali')
    list_filter = ('created', 'updated', CreationDateFilter)
    search_fields = ('name', 'created', 'updated')
    ordering = ['created']

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created).strftime('%y/%m/%d - %H:%M:%S')
    get_created_jalali.admin_order_field = 'created'
    get_created_jalali.short_description = 'تاریخ و زمان درج'

    def get_updated_jalali(self, obj):
        return datetime2jalali(obj.updated).strftime('%y/%m/%d - %H:%M:%S')
    get_updated_jalali.admin_order_field = 'updated'
    get_updated_jalali.short_description = 'تاریخ و زمان بروز رسانی'

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

    # def history_view(self, request, object_id, extra_context=None):
    #     print(object_id)
    #     return super().history_view(request, object_id, extra_context)


@admin.register(models.City)
class CityAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('name', 'state', 'get_created_jalali', 'get_updated_jalali')
    list_filter = ('state', 'created', 'updated', CreationDateFilter)
    search_fields = ['name', 'state__name', 'created', 'updated']
    ordering = ['created']
    autocomplete_fields = ['state', ]

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created).strftime('%y/%m/%d - %H:%M:%S')
    get_created_jalali.admin_order_field = 'created'
    get_created_jalali.short_description = 'تاریخ و زمان درج'

    def get_updated_jalali(self, obj):
        return datetime2jalali(obj.updated).strftime('%y/%m/%d - %H:%M:%S')
    get_updated_jalali.admin_order_field = 'updated'
    get_updated_jalali.short_description = 'تاریخ و زمان بروز رسانی'

    def get_search_results(self, request, queryset, search_term):
        """To filter with regard of JalaliDate"""
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        try:
            search_date = datetime.datetime.strptime(search_term, '%y/%m/%d')
            search_date = search_term
            obj_list = [x.id for x in self.model.objects.all()
                        if datetime2jalali(x.created).strftime('%y/%m/%d') == search_date or
                        datetime2jalali(x.updated).strftime('%y/%m/%d') == search_date
                        ]
            queryset = self.model.objects.filter(id__in=obj_list)
            return queryset, use_distinct
        except ValueError as er:
            pass
        return queryset, use_distinct


@admin.register(models.Chevron)
class ChevronAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('title', 'code', 'get_created_jalali', 'get_updated_jalali')
    list_filter = ('title', 'code', 'created', 'updated', CreationDateFilter)
    search_fields = ('title', 'created', 'updated')
    ordering = ['created']

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


@admin.register(models.StatusEquipment)
class StatusEquipmentAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('title', 'code',  'get_created_jalali', 'get_updated_jalali')
    list_filter = ('title', 'code', 'created', 'updated', CreationDateFilter)
    search_fields = ('title', 'created', 'updated')
    ordering = ['created']

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


@admin.register(models.Skill)
class SkillAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('title', 'code',  'get_created_jalali', 'get_updated_jalali')
    list_filter = ('title', 'code', 'created', 'updated', CreationDateFilter)
    search_fields = ('title', 'created', 'description', 'updated')
    ordering = ['created']

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


@admin.register(models.ZonetHreat)
class ZonetHreatAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('title',  'get_created_jalali', 'get_updated_jalali')
    list_filter = ('title', 'created', 'updated', CreationDateFilter)
    search_fields = ('title', 'created', 'description', 'updated')
    ordering = ['created']

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created).strftime('%y/%m/%d - %H:%M:%S')
    get_created_jalali.admin_order_field = 'created'
    get_created_jalali.short_description = 'تاریخ و زمان درج'

    def get_updated_jalali(self, obj):
        return datetime2jalali(obj.updated).strftime('%y/%m/%d - %H:%M:%S')
    get_updated_jalali.admin_order_field = 'updated'
    get_updated_jalali.short_description = 'تاریخ و زمان بروز رسانی'

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


@admin.register(models.Card)
class CardAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('title', 'code', 'get_created_jalali', 'get_updated_jalali')
    list_filter = ('title', 'code', 'created', 'updated', CreationDateFilter)
    search_fields = ('title', 'created', 'description', 'updated')
    ordering = ['created']

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


@admin.register(models.AcademicField)
class AcademicFieldAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    search_fields = ['name', ]


@admin.register(models.ToolsCategory)
class ToolsCategoryAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    search_fields = ['name', ]


@admin.register(models.EventCategory)
class EventCategoryAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    search_fields = ['name', ]
