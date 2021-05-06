from django.contrib import admin
from django.contrib.admin import sites


class ModeTeHeAdminSite(admin.AdminSite):
    def get_app_list(self, request):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        ordering = {
            "استان ها": 1,
            "شهر ها": 2,
            "تهدیدات منطقه ای": 3,
            "درجات نظامی": 4,
            "تخصص ها و رسته ها": 5,
            "رشته های دانشگاهی": 6,
            "کارت های حفاظتی": 7,
            "وضعیت های تجهیزات": 8,

            "پایگاه ها": 9,
            "اطلاعات حومه": 10,
            "دسته بندی های مکان ها": 11,
            "مکان ها": 12,

            "پایوران": 13,
            "دوره های طی شده پایوران": 14,
            "کارت های پایوران": 15,
            "حمل غیرمجاز اشیا توسط پایوران": 16,
            "بازداشت پایوران": 17,
            "تنبیهات پایور": 18,
            "ذی حساب ها": 19,

            "وظیفه ها": 20,
            "دوره های طی شده وظیفه ها": 21,
            "کارت های وظیفه": 22,
            "حمل غیرمجاز اشیا توسط وظیفه ها": 23,
            "بازداشت وظیفه ها": 24,
            "اضافات خدمت وظیفه ها": 25,
            "کسری خدمت وظیفه ها": 26,
            "مرخصی ها": 27,
            "مرخصی های رفته": 28,
            "نهست ها": 29,
            "فرار وظیفه ها": 30,

            "اعتبارات": 31,
            "فروشگاه ها": 32,
            "انبار ها": 33,
            "تجهیزات": 34,
            "تاریخچه ها": 35,

            "پست های نگهبانی": 36,
            "پایوران پلیس هوایی": 37,
            "وظیفه های پلیس هوایی": 38,
            "لوحه های نگهبانی": 39,

            "اجازه‌ها": 40,
            "گروه\u200cها": 41,
            "کاربرها": 42,
            "رویدادها": 43,

            "دسته بندی های تجهیزات": 44,
            "دسته بندی های رویداد ها": 45,
            "رویداد های فیزیکی": 46,
            "": 47,
            "": 48,
        }
        app_dict = self._build_app_dict(request)
        # a.sort(key=lambda x: b.index(x[0]))
        # Sort the apps alphabetically.
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

        # Sort the models alphabetically within each app.
        for app in app_list:
            app['models'].sort(key=lambda x: ordering[x['name']])

        return app_list


md = ModeTeHeAdminSite()
admin.site = md
sites.site = md
