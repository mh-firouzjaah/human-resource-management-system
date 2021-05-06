from django.shortcuts import get_object_or_404, render


from . import models


def guardtablet_to_pdf(request, guardtablet_id):
    return render(
        request, 'reports/guardtablet-to-pdf.html',
        {'guardtablet': get_object_or_404(models.GuardTablet, id=guardtablet_id)})
