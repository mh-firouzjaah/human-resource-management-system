from django.urls import path

from . import views

app_name = 'guard'

urlpatterns = [
    path('generate-pdf/guardtablet/<int:guardtablet_id>',
         views.guardtablet_to_pdf, name='guardtablet_to_pdf'),
]
