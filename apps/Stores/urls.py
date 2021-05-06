from django.urls import path

from . import views

app_name = 'store'
urlpatterns = [
    path('equ-to-pdf/<int:eq_id>', views.equipment_to_pdf, name='equipment_to_pdf')
]
