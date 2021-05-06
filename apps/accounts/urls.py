from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path(
        'password/', views.CustomPasswordChangeView.as_view(),
        name='change_password'),
]
