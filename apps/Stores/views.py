from django.shortcuts import get_object_or_404, render

from . import models

def equipment_to_pdf(request, eq_id):
    return render(request, 'reports/equipment-to-pdf.html',
                  {'equipment': get_object_or_404(models.Equipment, id=eq_id)})
