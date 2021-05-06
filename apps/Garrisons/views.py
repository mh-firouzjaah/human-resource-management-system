from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from . import models


def index(request):
    return HttpResponse("Modiriate Tamin Hefazat")


def details(request, person_id):
    return HttpResponse("You are looking at person {}".format(person_id))


def soldier_to_pdf(request, soldier_id):
    soldier = get_object_or_404(models.Soldier, id=soldier_id)
    if not request.user.is_superuser:
        if not soldier.location.garrison == request.user.garrison:
            raise PermissionDenied()

    soldier = get_object_or_404(models.Soldier, id=soldier_id)
    total_recesses = 0
    total_gone_recesses = 0
    total_surpluses = 0
    total_surpluses_bc_phone = 0
    total_diminutions = 0
    total_absences = 0

    if soldier.surpluses.count():
        total_surpluses = sum([x.day_count for x in soldier.surpluses.all()])
        total_surpluses += sum([x.day_count for x in soldier.imprisonments.all()])

    if soldier.mobile_portages.count():
        total_surpluses_bc_phone = sum(
            [x.day_count for x in soldier.mobile_portages.all()])
        total_surpluses += total_surpluses_bc_phone

    if soldier.diminutions.count():
        total_diminutions = sum([x.day_count for x in soldier.diminutions.all()])

    if soldier.absences.count():
        total_absences = sum([x.day_count() for x in soldier.absences.all()])

    if soldier.recesses.count():
        total_recesses = sum([x.day_count for x in soldier.recesses.all()])

    if soldier.gone_recesses.count():
        total_gone_recesses = sum([x.day_count for x in soldier.gone_recesses.all()])

    return render(request, 'reports/soldier-to-pdf.html',
                  {'soldier': soldier,
                   'total_surpluses': total_surpluses,
                   'total_surpluses_bc_phone': total_surpluses_bc_phone,
                   'total_recesses': total_recesses,
                   'total_gone_recesses': total_gone_recesses,
                   'left_recesses': total_recesses - total_gone_recesses,
                   'total_diminutions': total_diminutions,
                   'total_absences': total_absences
                   }
                  )


def personal_card(request, card_id):
    card = get_object_or_404(models.PersonalCard, id=card_id)
    personal = card.personal
    if not request.user.is_superuser:
        if request.user.garrison not in personal.locations.garrison:
            raise PermissionDenied()
    return render(request, 'reports/personal-card.html',
                  {'card': card})


def soldier_card(request, card_id):
    card = get_object_or_404(models.SoldierCard, id=card_id)
    soldier = card.soldier
    if not request.user.is_superuser:
        if request.user.garrison == soldier.location.garrison:
            raise PermissionDenied()
    return render(request, 'reports/soldier-card.html',
                  {'card': card})
