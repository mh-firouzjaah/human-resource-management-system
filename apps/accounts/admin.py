from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from jalali_date import datetime2jalali
from jalali_date.admin import ModelAdminJalaliMixin

from . import models
from . import views as custom_views

admin.autodiscover()

admin.site.site_header = 'Human Rescource Management System'
admin.site.site_title = 'Human Rescource Management System'
admin.site.index_title = 'مدیریت تمامی اطلاعات'

admin.site.login = custom_views.CustomLoginView.as_view()
admin.site.password_change = custom_views.CustomPasswordChangeView.as_view()


@admin.register(models.User)
class CustomUserAdmin(ModelAdminJalaliMixin, UserAdmin):
    add_fieldsets = ((None, {'classes': ('wide',), 'fields': (
        'personal', 'soldier', 'garrison', 'username', 'password1', 'password2', ), }), )

    UserAdmin.fieldsets[1][1]['fields'] = ('personal', 'soldier', 'garrison')

    autocomplete_fields = ('personal', 'soldier', 'garrison')

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_staff:
            if request.user.is_superuser:
                return ['last_login', 'date_joined']
            else:
                return ['is_staff', 'is_active', 'is_superuser', 'groups',
                        'user_permissions', 'last_login', 'date_joined']

    def save_model(self, request, obj, form, change):
        naming = obj.soldier or obj.personal
        obj.first_name = naming.first_name
        obj.last_name = naming.last_name
        return super().save_model(request, obj, form, change)

    def has_add_permission(self, request):
        return request.user.is_superuser  # False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser  # False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser  # False

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(models.CustomLogger)
class CustomLoggerAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    # date_hierarchy = 'event_date'
    list_filter = ['event_date', 'action_flag', 'user']
    search_fields = ['action', 'user', ]
    list_display = ['event_date_jalali', 'user',
                    'action', 'event_link', 'object_description']
    exclude = ('action_flag', 'object_link')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    # def has_view_permission(self, request, obj=None):
    #     return request.user.is_superuser

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        qs = qs.filter(user__garrison=request.user.garrison).distinct(
        ) if qs.count() >= 1 else qs

    def object_description(self, obj):
        return obj
    object_description.short_description = _('event description')

    def event_date_jalali(self, obj):
        return datetime2jalali(obj.event_date).strftime('%y/%m/%d _ %H:%M:%S')
    event_date_jalali.short_description = _('event date')
    event_date_jalali.admin_order_field = 'event_date'

    def event_link(self, obj):
        if obj.object_link:
            return mark_safe(obj.object_link)
        return ""
    event_link.short_description = _('event link')


def perm_str(self):
    if "add_" in self.codename:
        return _("Can add | {content_type}").format(content_type=self.content_type)
    elif "change_" in self.codename:
        return _("Can change | {content_type}").format(content_type=self.content_type)
    elif "delete_" in self.codename:
        return _("Can delete | {content_type}").format(content_type=self.content_type)
    elif "view_" in self.codename:
        return _("Can view | {content_type}").format(content_type=self.content_type)


Permission.__str__ = perm_str


@admin.register(Permission)
class CustomPermissionAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return request.user.is_superuser  # False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser  # False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser  # False

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser
