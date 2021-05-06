from django.urls import path

from . import views

app_name = 'people'

urlpatterns = [
    # ex: hostname/persons/
    path('', views.index, name='index'),
    # ex: hostname/persons/5/
    path('<int:person_id>', views.details, name='details'),
    path('generate-pdf/soldier/<int:soldier_id>',
         views.soldier_to_pdf, name='soldier_to_pdf'),
    path('generate-pdf/personal-card/<int:card_id>',
         views.personal_card, name='personal_card'),
    path('generate-pdf/soldier-card/<int:card_id>',
         views.soldier_card, name='soldier_card')
]
