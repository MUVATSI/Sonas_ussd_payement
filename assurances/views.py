from django.contrib.auth import authenticate, login
from django.template.loader import get_template
from django.shortcuts import redirect, render
from .utils import pagination, get_payement
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from django.views import View
from random import randint
from .models import *
import datetime
import pdfkit


# My views are implemented here.
def home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin:index')
            # elif user.is_technician:
            #     return redirect('technician')
            else:
                return redirect('tech')
        else:
            messages.error(request, "Nom d'utilisateur ou Mot de passe incorect")
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


class HomeView(View):
    template_name = 'index.html'
    payements = Payment.objects.select_related('assure', 'enr_par', 'vehicule').all().order_by('-date_operation')

    context = {
        'payements': payements
    }

    def get(self, request, *args, **kwargs):
        contenu = pagination(request, self.payements)
        self.context['payements'] = contenu

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        # Validation
        if request.POST.get('id_validated'):
            validated = request.POST.get('validated')

            try:
                obj = Payment.objects.get(id=request.POST.get('id_validated'))
                if validated == 'True':
                    obj.verifie = True
                else:
                    obj.verifie = False
                obj.save()
                messages.success(request, "Etat modifié avec succes")
            except Exception as e:
                messages.error(request, f"Desolé, l'erreur {e} est survenue.")

        contenu = pagination(request, self.payements)
        self.context['payements'] = contenu

        return render(request, self.template_name, self.context)


class Ajouter(View):
    template_name = 'ajout_assure.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        data = {
            'nom': request.POST.get('nom'),
            'prenom': request.POST.get('prenom'),
            'postnom': request.POST.get('postnom'),
            'numero': request.POST.get('numero'),
            'email': request.POST.get('email'),
            'addresse': request.POST.get('addresse'),
            'genre': request.POST.get('genre'),
            'enr_par': request.user
        }
        try:
            created = Assure.objects.create(**data)

            if created:
                messages.success(request, "L'assuré a été ajouté avec succes")
            else:
                messages.error(request, "Desolé, un probleme est survenu lors de l'enregistrement")
        except Exception as e:
            messages.error(request, f"Probleme de {e}.")
        return render(request, self.template_name)


def AddPayment(idc, mt):
    assure = Assure.objects.get(pk=idc)
    q = Q(id__icontains=idc)
    selected_assure = Assure.objects.filter(q)
    vehicule = Vehicule.objects.get(assure__in=selected_assure)
    a = randint(10, 99)
    b = randint(100, 999)
    c = randint(100, 999)
    transaction_id = "CU" + str(a) + "-" + str(b) + "-" + str(c)
    data = {
        'transaction_id': transaction_id,
    }

    payment_encours = Payment()

    payment_encours.montant = mt
    payment_encours.assure = assure
    payment_encours.vehicule = vehicule
    payment_encours.transaction_id = transaction_id
    payment_encours.save()
    print("payment Saved Successful")


class PayementManuel(View):
    template_name = 'paiement.html'
    assures = Assure.objects.all()
    vehicules = Vehicule.objects.all()

    context = {
        'assures': assures,
        'vehicules': vehicules,
    }

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        a = randint(10, 99)
        b = randint(100, 999)
        c = randint(100, 999)
        transaction_id = "CU" + str(a) + "-" + str(b) + "-" + str(c)

        assure = request.POST.get('assure')
        cle_assure = Q(id__icontains=assure)
        selected_assure = Assure.objects.get(cle_assure)

        vehicule = request.POST.get('vehicule')
        cle_veh = Q(marque__icontains=vehicule)
        selected_veh = Vehicule.objects.get(cle_veh)

        data = {
            'assure': selected_assure,
            'vehicule': selected_veh,
            'montant': request.POST.get('montant'),
            'transaction_id': transaction_id,
            'enr_par': request.user,
        }
        try:
            created = Payment.objects.create(**data)
            if created:
                messages.success(request, "Le paiement a été ajouté avec succes")
            else:
                messages.error(request, "Desolé, un probleme est survenu lors de l'enregistrement")
        except Exception as e:
            messages.error(request, f"Probleme de {e}.")
        return render(request, self.template_name, self.context)


class GenererQuittance(View):
    """ This view helps to visualize the invoice """

    template_name = 'quittance.html'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        context = get_payement(pk)
        return render(request, self.template_name, context)

def get_quittance_pdf(request, *args, **kwargs):
    """ generate pdf file from html file """
    pk = kwargs.get('pk')
    context = get_payement(pk)
    context['date'] = datetime.datetime.today()
    template = get_template('quittance-pdf.html')
    html = template.render(context)
    # options of pdf format
    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
        "enable-local-file-access": ""
    }
    # generate pdf
    pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
    pdf = pdfkit.from_string(html, False, options)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = "attachement"
    return response
