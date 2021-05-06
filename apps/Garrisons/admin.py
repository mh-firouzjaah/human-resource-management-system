import datetime

from admin_auto_filters.filters import AutocompleteFilter
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.urls import reverse
from django.utils.safestring import mark_safe
from jalali_date import date2jalali, datetime2jalali
from jalali_date.admin import (ModelAdminJalaliMixin, StackedInlineJalaliMixin,
                               TabularInlineJalaliMixin)

from . import models
from .models import (EnvironsInformation, Event, Garrison, Location,
                     LocationCategory)


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


@admin.register(Garrison)
class GarrisonAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('name', 'city', 'get_created_jalali', 'get_updated_jalali')
    list_filter = ('city', 'updated', CreationDateFilter)
    search_fields = ('name', 'city__name', 'description',)
    ordering = ['created']
    # date_hierarchy = 'created'
    filter_horizontal = ('zonet_hreats',)
    autocomplete_fields = ['city', ]

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
            admin_user=request.user).distinct() if qs.count() >= 1 else qs

    def get_search_results(self, request, queryset, search_term):
        """To filter Search results"""
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        if not request.user.is_superuser:
            '''
            if ("location/add/" in str(request.META.get('HTTP_REFERER'))) or re.search(
                    r"location/\d/change/", str(request.META.get('HTTP_REFERER'))):
            '''
            queryset = self.model.objects.filter(admin_user=request.user)

        if search_term:
            try:
                search_date = datetime.datetime.strptime(search_term, '%y/%m/%d')
                search_date = search_term
            except ValueError:
                pass
            else:
                obj_list = [x.id for x in self.model.objects.all()
                            if datetime2jalali(x.created).strftime('%y/%m/%d') == search_date or
                            datetime2jalali(x.updated).strftime('%y/%m/%d') == search_date
                            ]
                queryset |= self.model.objects.filter(id__in=obj_list)
        return queryset, use_distinct


@admin.register(LocationCategory)
class LocationCategoryAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('name', 'get_created_jalali', 'get_updated_jalali')
    list_filter = ('updated', CreationDateFilter)
    search_fields = ('name', 'description',)
    ordering = ['created']

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created).strftime('%y/%m/%d - %H:%M:%S')
    get_created_jalali.admin_order_field = 'created'
    get_created_jalali.short_description = 'تاریخ و زمان درج'

    def get_updated_jalali(self, obj):
        return datetime2jalali(obj.updated).strftime('%y/%m/%d - %H:%M:%S')
    get_updated_jalali.admin_order_field = 'updated'
    get_updated_jalali.short_description = 'تاریخ و زمان بروز رسانی'

    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs
    #     return qs.filter(locations__garrison=request.user.garrison).distinct() if qs.count() >= 1 else qs

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


@ admin.register(Location)
class LocationAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('name', 'garrison', 'liable', 'category', 'phone_number',
                    )  # 'get_created_jalali', 'get_updated_jalali'
    list_filter = ('liable', 'created', 'updated', )  # CreationDateFilter
    search_fields = ('name', 'garrison__name',
                     'liable', 'phone_number',
                     'description', 'created', 'updated')
    ordering = ['created']
    filter_horizontal = ('zonet_hreats',)
    autocomplete_fields = ['garrison', 'category', ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(
            garrison=request.user.garrison).distinct() if qs.count() >= 1 else qs

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


@ admin.register(EnvironsInformation)
class EnvironsInformationAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('title', 'garrison', 'phone_number',
                    'get_created_jalali', 'get_updated_jalali')
    list_filter = ('garrison', 'created', 'updated', )  # CreationDateFilter
    search_fields = ('title', 'garrison__name', 'address', 'phone_number',
                     'description', 'created', 'updated')
    ordering = ['created']
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
            garrison=request.user.garrison).distinct() if qs.count() >= 1 else qs

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


@ admin.register(Event)
class EventAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    # 'get_created_jalali', 'get_updated_jalali'
    list_display = ('category', 'location', 'date', 'time')
    list_filter = ('category', 'location', 'date', 'time',
                   'created', 'updated', )  # CreationDateFilter
    search_fields = ('time', 'date',
                     'description', 'created', 'updated', 'personal__first_name',
                     'personal__last_name')
    ordering = ['created']
    autocomplete_fields = ['category', 'personal', 'location']


class CityFilter(AutocompleteFilter):
    title = 'شهر'  # display title
    field_name = 'city'  # name of the foreign key field


class AcademicFieldFilter(AutocompleteFilter):
    title = 'رشته تحصیلی'  # display title
    field_name = 'academic_field'  # name of the foreign key field


# class CityFilter(AutocompleteFilter):
    #     title = 'شهر'  # display title
    #     field_name = 'city'  # name of the foreign key field


@admin.register(models.Personal)
class PersonalAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'jobSubject',
                    'get_created_jalali', 'get_updated_jalali')
    list_filter = ('is_buy_expert', 'is_buyer', 'locations', 'created', 'updated')
    search_fields = ('first_name', 'last_name', 'personalCode', 'jobSubject',
                     'actionJob', 'phoneNumber', 'description', 'created', 'updated')
    ordering = ['created']
    # filter_horizontal = ()
    autocomplete_fields = ['locations', 'chevron', 'skill', 'level']
    # prepopulated_fields = {'slug' : ('title',)}

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
        return qs.filter(locations__garrison=request.user.garrison).distinct() if qs.count() >= 1 else qs

    def get_search_results(self, request, queryset, search_term):
        """To filter with regard of JalaliDate"""

        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        '''
        if not request.user.is_superuser:
            queryset = self.model.objects.filter(garrison=request.user.garrison)
        '''
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

        import re
        if 'equipment/add/' in str(request.META.get('HTTP_REFERER')) or\
                re.search(r"equipment/\d/change/", str(request.META.get('HTTP_REFERER'))):
            queryset = queryset.filter(is_buyer=True)
        if 'is_buy_expert' in request.GET:
            queryset = queryset.filter(is_buy_expert=True)
        return queryset, use_distinct


@admin.register(models.PersonalLearnCourse)
class PersonalLearnCourseAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('title', 'point', 'get_created_jalali', 'get_updated_jalali',
                    'get_started_jalali', 'get_ended_jalali')
    list_filter = ('title', 'point', 'created', 'updated')
    search_fields = ('title', 'point', 'created', 'updated')
    ordering = ['created']
    autocomplete_fields = ['personal', ]

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created).strftime('%y/%m/%d - %H:%M:%S')
    get_created_jalali.admin_order_field = 'created'
    get_created_jalali.short_description = 'تاریخ و زمان درج'

    def get_updated_jalali(self, obj):
        return datetime2jalali(obj.updated).strftime('%y/%m/%d - %H:%M:%S')
    get_updated_jalali.admin_order_field = 'updated'
    get_updated_jalali.short_description = 'تاریخ و زمان بروز رسانی'

    def get_started_jalali(self, obj):
        return date2jalali(obj.start).strftime('%y/%m/%d')
    get_started_jalali.admin_order_field = 'start'
    get_started_jalali.short_description = 'تاریخ شروع'

    def get_ended_jalali(self, obj):
        return date2jalali(obj.end).strftime('%y/%m/%d')
    get_ended_jalali.admin_order_field = 'end'
    get_ended_jalali.short_description = 'تاریخ پایان'

    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs
    #     return qs.filter(
    #         personal__locations__garrison=request.user.garrison).distinct() if qs.count() >= 1 else qs

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


@admin.register(models.SoldierLearnCourse)
class SoldierLearnCourseAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('soldier', 'title', 'point', 'get_created_jalali',
                    'get_updated_jalali', 'get_started_jalali', 'get_ended_jalali')
    list_filter = ('title', 'point', 'created', 'updated')
    search_fields = ('title', 'point', 'created', 'updated')
    ordering = ['created']
    autocomplete_fields = ['soldier', ]

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created).strftime('%y/%m/%d - %H:%M:%S')
    get_created_jalali.admin_order_field = 'created'
    get_created_jalali.short_description = 'تاریخ و زمان درج'

    def get_updated_jalali(self, obj):
        return datetime2jalali(obj.updated).strftime('%y/%m/%d - %H:%M:%S')
    get_updated_jalali.admin_order_field = 'updated'
    get_updated_jalali.short_description = 'تاریخ و زمان بروز رسانی'

    def get_started_jalali(self, obj):
        return date2jalali(obj.start).strftime('%y/%m/%d')
    get_started_jalali.admin_order_field = 'start'
    get_started_jalali.short_description = 'تاریخ شروع'

    def get_ended_jalali(self, obj):
        return date2jalali(obj.end).strftime('%y/%m/%d')
    get_ended_jalali.admin_order_field = 'end'
    get_ended_jalali.short_description = 'تاریخ پایان'

    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs
    #     return qs.filter(
    #         personal__locations__garrison=request.user.garrison).distinct() if qs.count() >= 1 else qs

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


@admin.register(models.Owner)
class OwnerAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('personal', 'owner_code', 'get_created_jalali', 'get_updated_jalali')
    list_filter = ('personal', 'garrison', 'created', 'updated')
    search_fields = ('personal__first_name', 'personal__last_name',
                     'owner_code', 'created', 'updated')
    ordering = ['created']
    autocomplete_fields = ['personal', 'garrison', ]

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
            garrison=request.user.garrison).distinct() if qs.count() >= 1 else qs

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


@admin.register(models.Soldier)
class SoldierAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'location',
                    'get_created_jalali', 'get_updated_jalali', 'order_pdf')
    list_filter = [CityFilter, AcademicFieldFilter,
                   'is_married',
                   'academic_level', 'chevron', 'bulk_state',
                   'psyche_state', ]
    search_fields = ['national_code',
                     'first_name', 'last_name',
                     'description', 'created', 'updated', 'phone_number',
                     'home_phone_number', 'father_phone_number', 'mother_phone_number',
                     ]
    ordering = ['created']
    autocomplete_fields = ['location', 'city', 'chevron', 'skill', ]
    # date_hierarchy = 'publication_date'
    # filter_horizontal = ('authors',)

    class Media:
        pass

    def order_pdf(self, obj):
        url = reverse('people:soldier_to_pdf', args=[obj.id])
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

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(
            location__garrison=request.user.garrison).distinct() if qs.count() >= 1 else qs

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


@admin.register(models.Diminution)
class DiminutionAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('soldier', 'day_count', 'spare',
                    'get_created_jalali', 'get_updated_jalali')
    list_filter = ('spare', 'day_count', 'created', 'updated')
    search_fields = ('soldier__first_name', 'soldier__last_name',
                     'day_count', 'spare', 'description')
    ordering = ['created']
    autocomplete_fields = ['soldier', ]
    # date_hierarchy = 'publication_date'
    # filter_horizontal = ('authors',)

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
        return qs.filter(soldier__location__garrison=request.user.garrison).distinct() if qs.count() >= 1 else qs

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


@admin.register(models.PersonalCard)
class PersonalCardAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = (
        'personal', 'card', 'get_registered_jalali', 'get_expired_jalali', 'number',
        'is_active', 'order_pdf')
    list_filter = ('card', 'is_active', 'created', 'updated')
    ordering = ['created']
    search_fields = ['card__title', 'personal__first_name', 'personal__last_name', ]
    autocomplete_fields = ['personal', 'card', ]

    def order_pdf(self, obj):
        url = reverse('people:personal_card', args=[obj.id])
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

    def get_registered_jalali(self, obj):
        return date2jalali(obj.register_date).strftime('%y/%m/%d')
    get_registered_jalali.admin_order_field = 'register_date'
    get_registered_jalali.short_description = 'تاریخ شروع اعتبار'

    def get_expired_jalali(self, obj):
        return date2jalali(obj.exp_date).strftime('%y/%m/%d')
    get_expired_jalali.admin_order_field = 'exp_date'
    get_expired_jalali.short_description = 'تاریخ پایان اعتبار'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(
            personal__locations__garrison=request.user.garrison
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


@admin.register(models.SoldierCard)
class SoldierCardAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = (
        'soldier', 'card', 'get_registered_jalali', 'get_expired_jalali', 'number',
        'is_active', 'order_pdf')
    list_filter = ['card', 'is_active', 'created', 'updated', ]
    ordering = ['created']
    autocomplete_fields = ['soldier', 'card', ]

    class Media:
        pass

    def order_pdf(self, obj):
        url = reverse('people:soldier_card', args=[obj.id])
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

    def get_registered_jalali(self, obj):
        return date2jalali(obj.register_date).strftime('%y/%m/%d')
    get_registered_jalali.admin_order_field = 'register_date'
    get_registered_jalali.short_description = 'تاریخ شروع اعتبار'

    def get_expired_jalali(self, obj):
        return date2jalali(obj.exp_date).strftime('%y/%m/%d')
    get_expired_jalali.admin_order_field = 'exp_date'
    get_expired_jalali.short_description = 'تاریخ پایان اعتبار'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(soldier__location__garrison=request.user.garrison).distinct() if qs.count() >= 1 else qs

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


@admin.register(models.Chastise)
class ChastiseAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('personal', 'reason', 'get_registered_jalali',
                    'sentence', 'get_created_jalali', 'get_updated_jalali')
    list_filter = ('created', 'updated')
    ordering = ['created']
    autocomplete_fields = ['personal', 'doorkeeper', ]
    search_fields = ('personal__first_name', 'personal__last_name', 'description')

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created).strftime('%y/%m/%d - %H:%M:%S')
    get_created_jalali.admin_order_field = 'created'
    get_created_jalali.short_description = 'تاریخ و زمان درج'

    def get_updated_jalali(self, obj):
        return datetime2jalali(obj.updated).strftime('%y/%m/%d - %H:%M:%S')
    get_updated_jalali.admin_order_field = 'updated'
    get_updated_jalali.short_description = 'تاریخ و زمان بروز رسانی'

    def get_registered_jalali(self, obj):
        return date2jalali(obj.register_date).strftime('%y/%m/%d')
    get_registered_jalali.admin_order_field = 'register_date'
    get_registered_jalali.short_description = 'تاریخ شروع'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(personal__locations__garrison=request.user.garrison).distinct() if qs.count() >= 1 else qs

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


@admin.register(models.Surplus)
class SurplusAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('soldier', 'personal',
                    'reporter', 'reason', 'get_registered_jalali', 'day_count',
                    'get_created_jalali', 'get_updated_jalali')
    list_filter = ('day_count', 'created', 'updated')
    ordering = ['created']
    autocomplete_fields = ['soldier', 'personal', ]
    search_fields = ('soldier__first_name', 'soldier__last_name', 'description')

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created).strftime('%y/%m/%d - %H:%M:%S')
    get_created_jalali.admin_order_field = 'created'
    get_created_jalali.short_description = 'تاریخ و زمان درج'

    def get_updated_jalali(self, obj):
        return datetime2jalali(obj.updated).strftime('%y/%m/%d - %H:%M:%S')
    get_updated_jalali.admin_order_field = 'updated'
    get_updated_jalali.short_description = 'تاریخ و زمان بروز رسانی'

    def get_registered_jalali(self, obj):
        return date2jalali(obj.register_date).strftime('%y/%m/%d')
    get_registered_jalali.admin_order_field = 'register_date'
    get_registered_jalali.short_description = 'تاریخ شروع'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(soldier__location__garrison=request.user.garrison).distinct() if qs.count() >= 1 else qs

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


@admin.register(models.MobilePortage)
class MobilePortageAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('soldier', 'model', 'doorkeeper', 'get_registered_jalali',
                    'day_count', 'smart', 'get_created_jalali', 'get_updated_jalali')
    list_filter = ('smart', 'day_count', 'location', 'created', 'updated')

    ordering = ['created']
    autocomplete_fields = ['soldier', 'doorkeeper', 'location']
    search_fields = ('soldier__first_name', 'soldier__last_name', 'description')

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created).strftime('%y/%m/%d - %H:%M:%S')
    get_created_jalali.admin_order_field = 'created'
    get_created_jalali.short_description = 'تاریخ و زمان درج'

    def get_updated_jalali(self, obj):
        return datetime2jalali(obj.updated).strftime('%y/%m/%d - %H:%M:%S')
    get_updated_jalali.admin_order_field = 'updated'
    get_updated_jalali.short_description = 'تاریخ و زمان بروز رسانی'

    def get_registered_jalali(self, obj):
        return date2jalali(obj.register_date).strftime('%y/%m/%d')
    get_registered_jalali.admin_order_field = 'register_date'
    get_registered_jalali.short_description = 'تاریخ شروع'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(soldier__location__garrison=request.user.garrison).distinct() if qs.count() >= 1 else qs

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


@admin.register(models.MobilePortagePersonal)
class MobilePortagePersonalAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('personal', 'model', 'doorkeeper', 'get_registered_jalali',
                    'smart', 'get_created_jalali', 'get_updated_jalali')
    list_filter = ('smart', 'location', 'created', 'updated')

    ordering = ['created']
    autocomplete_fields = ['personal', 'doorkeeper', 'location']
    search_fields = ('personal__first_name', 'personal__last_name', 'description')

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created).strftime('%y/%m/%d - %H:%M:%S')
    get_created_jalali.admin_order_field = 'created'
    get_created_jalali.short_description = 'تاریخ و زمان درج'

    def get_updated_jalali(self, obj):
        return datetime2jalali(obj.updated).strftime('%y/%m/%d - %H:%M:%S')
    get_updated_jalali.admin_order_field = 'updated'
    get_updated_jalali.short_description = 'تاریخ و زمان بروز رسانی'

    def get_registered_jalali(self, obj):
        return date2jalali(obj.register_date).strftime('%y/%m/%d')
    get_registered_jalali.admin_order_field = 'register_date'
    get_registered_jalali.short_description = 'تاریخ شروع'

    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs
    #         # check01
    #     return qs.filter(soldier__location__garrison=request.user.garrison).distinct() if qs.count() >= 1 else qs

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


@admin.register(models.Volatile)
class VolatileAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('soldier', 'get_started_jalali', 'get_ended_jalali',
                    'get_created_jalali', 'get_updated_jalali')
    list_filter = ('created', 'updated')
    ordering = ['created']
    autocomplete_fields = ['soldier', ]
    search_fields = ('soldier__first_name', 'soldier__last_name', 'description')

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created).strftime('%y/%m/%d - %H:%M:%S')
    get_created_jalali.admin_order_field = 'created'
    get_created_jalali.short_description = 'تاریخ و زمان درج'

    def get_updated_jalali(self, obj):
        return datetime2jalali(obj.updated).strftime('%y/%m/%d - %H:%M:%S')
    get_updated_jalali.admin_order_field = 'updated'
    get_updated_jalali.short_description = 'تاریخ و زمان بروز رسانی'

    def get_started_jalali(self, obj):
        return date2jalali(obj.start_date).strftime('%y/%m/%d')
    get_started_jalali.admin_order_field = 'start_date'
    get_started_jalali.short_description = 'تاریخ شروع فرار'

    def get_ended_jalali(self, obj):
        return date2jalali(obj.end_date).strftime('%y/%m/%d')
    get_ended_jalali.admin_order_field = 'end_date'
    get_ended_jalali.short_description = 'تاریخ پایان فرار'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(soldier__location__garrison=request.user.garrison).distinct() if qs.count() >= 1 else qs

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


@admin.register(models.Absence)
class AbsenceAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('soldier', 'get_started_jalali', 'get_ended_jalali',
                    'get_created_jalali', 'get_updated_jalali')
    list_filter = ('created', 'updated')
    ordering = ['created']
    autocomplete_fields = ['soldier', ]
    search_fields = ('soldier__first_name', 'soldier__last_name', 'description')

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created).strftime('%y/%m/%d - %H:%M:%S')
    get_created_jalali.admin_order_field = 'created'
    get_created_jalali.short_description = 'تاریخ و زمان درج'

    def get_updated_jalali(self, obj):
        return datetime2jalali(obj.updated).strftime('%y/%m/%d - %H:%M:%S')
    get_updated_jalali.admin_order_field = 'updated'
    get_updated_jalali.short_description = 'تاریخ و زمان بروز رسانی'

    def get_started_jalali(self, obj):
        return date2jalali(obj.start_date).strftime('%y/%m/%d')
    get_started_jalali.admin_order_field = 'start_date'
    get_started_jalali.short_description = 'تاریخ شروع نهست'

    def get_ended_jalali(self, obj):
        return date2jalali(obj.end_date).strftime('%y/%m/%d')
    get_ended_jalali.admin_order_field = 'end_date'
    get_ended_jalali.short_description = 'تاریخ پایان نهست'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(soldier__location__garrison=request.user.garrison).distinct() if qs.count() >= 1 else qs

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


@admin.register(models.Prison)
class PrisonAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_filter = ('created', 'updated')
    list_display = (
        'soldier', 'reason', 'day_count', 'receipt', 'precept_number', 'location',
        'doorkeeper', 'description', 'get_created_jalali', 'get_updated_jalali')
    ordering = ['created']
    autocomplete_fields = ['soldier', ]
    search_fields = ('soldier__first_name', 'soldier__last_name', 'description')

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
        return qs.filter(soldier__location__garrison=request.user.garrison).distinct() if qs.count() >= 1 else qs

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


@admin.register(models.PrisonPersonal)
class PrisonPersonalAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_filter = ('created', 'updated')
    list_display = (
        'personal', 'reason', 'receipt', 'precept_number', 'location',
        'doorkeeper', 'description', 'get_created_jalali', 'get_updated_jalali')
    ordering = ['created']
    autocomplete_fields = ['personal', ]
    search_fields = ('personal__first_name', 'personal__last_name', 'description')

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created).strftime('%y/%m/%d - %H:%M:%S')
    get_created_jalali.admin_order_field = 'created'
    get_created_jalali.short_description = 'تاریخ و زمان درج'

    def get_updated_jalali(self, obj):
        return datetime2jalali(obj.updated).strftime('%y/%m/%d - %H:%M:%S')
    get_updated_jalali.admin_order_field = 'updated'
    get_updated_jalali.short_description = 'تاریخ و زمان بروز رسانی'

    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs
    #     return qs.filter(soldier__location__garrison=request.user.garrison).distinct() if qs.count() >= 1 else qs

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


@admin.register(models.Recess)
class RecessAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_filter = ('typerec', 'use', 'created', 'updated')
    list_display = (
        'soldier', 'reason', 'day_count', 'typerec', 'precept_number', 'receipt',
        'get_record_jalali', 'description', 'get_created_jalali', 'get_updated_jalali')
    ordering = ['created']
    autocomplete_fields = ['soldier', 'receipt']
    search_fields = ('soldier__first_name', 'soldier__last_name', 'description')

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created).strftime('%y/%m/%d - %H:%M:%S')
    get_created_jalali.admin_order_field = 'created'
    get_created_jalali.short_description = 'تاریخ و زمان درج'

    def get_updated_jalali(self, obj):
        return datetime2jalali(obj.updated).strftime('%y/%m/%d - %H:%M:%S')
    get_updated_jalali.admin_order_field = 'updated'
    get_updated_jalali.short_description = 'تاریخ و زمان بروز رسانی'

    def get_record_jalali(self, obj):
        if obj.date:
            return date2jalali(obj.date).strftime('%y/%m/%d')
    get_record_jalali.admin_order_field = 'date'
    get_record_jalali.short_description = 'تاریخ ثبت'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(soldier__location__garrison=request.user.garrison).distinct() if qs.count() >= 1 else qs

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


@admin.register(models.GoRecess)
class GoRecessAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_filter = ('typerec', 'created', 'updated')
    list_display = (
        'soldier', 'day_count', 'typerec', 'get_started_jalali', 'get_ended_jalali',
        'description', 'get_created_jalali', 'get_updated_jalali')
    ordering = ['created']
    autocomplete_fields = ['soldier', ]
    search_fields = ('soldier__first_name', 'soldier__last_name', 'description')

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created).strftime('%y/%m/%d - %H:%M:%S')
    get_created_jalali.admin_order_field = 'created'
    get_created_jalali.short_description = 'تاریخ و زمان درج'

    def get_updated_jalali(self, obj):
        return datetime2jalali(obj.updated).strftime('%y/%m/%d - %H:%M:%S')
    get_updated_jalali.admin_order_field = 'updated'
    get_updated_jalali.short_description = 'تاریخ و زمان بروز رسانی'

    def get_started_jalali(self, obj):
        return date2jalali(obj.start_date).strftime('%y/%m/%d')
    get_started_jalali.admin_order_field = 'start_date'
    get_started_jalali.short_description = 'تاریخ شروع'

    def get_ended_jalali(self, obj):
        return date2jalali(obj.end_date).strftime('%y/%m/%d')
    get_ended_jalali.admin_order_field = 'end_date'
    get_ended_jalali.short_description = 'تاریخ پایان'

    # def save_model(self, request, obj, form, change):
    # if obj.start_date and obj.day_count:
    #     obj.end_date = obj.start_date + datetime.timedelta(days=obj.day_count)
    # return super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(soldier__location__garrison=request.user.garrison).distinct() if qs.count() >= 1 else qs

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
