# Views for common tasks

from django.shortcuts import render
from .models import ML_algorithms
import datetime
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


def index(request):
    # logging
    logger.warning('Homepage was accessed at '+str(datetime.datetime.now())+' hours!')
    algorithms = ML_algorithms.objects.filter(name__icontains=request.GET.get('search', ''))
    context = {"algorithms":algorithms}
    return render(request, "index.html", context)

