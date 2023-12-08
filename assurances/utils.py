from django.core.paginator import (Paginator, EmptyPage, PageNotAnInteger)
from .models import *


def pagination(request, payements):
    page_par_defaut = 1
    page = request.GET.get('page', page_par_defaut)
    nombre_par_page = 10
    paginateur = Paginator(payements, nombre_par_page)

    try:
        contenu_par_pages = paginateur.page(page)
    except PageNotAnInteger:
        contenu_par_pages = paginateur.page(page_par_defaut)
    except EmptyPage:
        contenu_par_pages = paginateur.page(paginateur.num_pages)

    return contenu_par_pages


def get_payement(pk):
    """ """
    payement = Payment.objects.get(pk=pk)
    context = {
        'obj': payement
    }
    return context
