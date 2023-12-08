from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from assurances.views import AddPayment
from .models import *


@csrf_exempt
def index2(request, *args, **kwargs):
    global montant
    global response
    global choix
    global codeclient
    if request.method == 'POST':
        comptes = CompteMobileClient.objects.all()
        session_id = request.POST.get('sessionId')
        service_code = request.POST.get('serviceCode')
        phone_number = request.POST.get('phoneNumber')
        text = request.POST.get("text", "Default")
        text_array = text.split("*")
        user_response = text_array[-1]
        level = len(text_array)
        response = ""

        if text == "":
            response = "CON Choisissez votre devise \n"
            response += "1. USD \n"
            response += "2. CDF \n"

        # LOGIC USSD SESSION
        elif text == "1":
            response = "CON  \n"
            response += "1. Paiements \n"
            response += "2. Envoi Argent \n"
            response += "3. Retrait d'argent \n"
            response += "4. Achat Forfaits \n"

        elif text == "1*1":
            response = "CON  \n"
            response += "1. CANAL+ \n"
            response += "2. SONAS \n"
            response += "3. BBOXX \n"

        elif text == "1*1*2":
            response = "CON \n"
            response += "Saisir votre code client \n"

        elif text == "1*1*2*" + user_response and level == 4:
            response = "CON \n"
            codeclient= user_response
            response += "Entrez le montant à payer en USD"

        elif text_array[0] == "1" and level == 5:
            response = "CON \n"
            montant = user_response
            response += "Envoyer " + str(montant) + " USD à la SONAS: \n"
            response += "1. Oui\n"
            response += "2. Non\n"

        elif text_array[-1] == "1" and level == 6:
            response = "CON Entrer le mot de passe"

        elif text_array[-1] == "2" and level == 6:
            response = "END Merci d'avoir consulter le service"

        elif text_array[0] == "1" and level == 7:
            AddPayment(codeclient,montant)
            response = "END Operation de Paiement effectuer avec Succes"

        elif text == "1*1*1":
            response = "END Bientot nous allons inclure le payement mobile CANAL+\n"

        elif text == "1*1*3":
            response = "END Bientot nous allons inclure le payement mobile BBOX\n"

        elif text == "1*2":
            response = "CON  \n"
            response += "1. Entrer numero surnom \n"
            response += "2. Numeros Favoris \n"
            response += "3. Annulations de transaction \n"

        elif text == "1*3":
            response = "CON Entrer code d'agent/numero \n"

        elif text == "1*4":
            response = "CON  \n"
            response += "1. Forfait internet \n"
            response += "2. Forfait Appels \n"
            response += "3. Forfait SMS \n"

        # LOGIC CDF SESSION -------------------------------------
        elif text == "2":
            response = "CON  \n"
            response += "1. Paiements \n"
            response += "2. Envoi Argent \n"
            response += "3. Retrait d'argent \n"
            response += "4. Achat Forfaits \n"

        elif text == "2*1":
            response = "CON  \n"
            response += "1. CANAL+ \n"
            response += "2. SONAS \n"
            response += "3. BBOXX \n"

        elif text == "2*1*2":
            response = "CON \n"
            response += "Saisir votre code client \n"

        elif text == "2*1*2*" + user_response and level == 4:
            response = "CON \n"
            codeclient = user_response
            response += "Entrez le montant à payer en CDF"

        elif text_array[0] == "2" and level == 5:
            response = "CON \n"
            montant = user_response
            response += "Envoyer " + str(montant) + " CDF à la SONAS: \n"
            response += "1. Oui\n"
            response += "2. Non\n"

        elif text_array[0] == "2" and level == 7:
            montant = float(int(montant)/2700)
            AddPayment(codeclient, montant)
            response = "END Operation de paiement effectuer avec Succes"

        elif text == "2*1*1":
            response = "END Bientot nous allons inclure le payement mobile CANAL+\n"

        elif text == "2*1*3":
            response = "END Bientot nous allons inclure le payement mobile CANAL+\n"

        elif text == "2*2":
            response = "CON  \n"
            response += "1. Entrer numero surnom \n"
            response += "2. Numeros Favoris \n"
            response += "3. Annulations de transaction \n"

        elif text == "2*3":
            response = "CON Entrer code d'agent/numero \n"

        elif text == "2*4":
            response = "CON  \n"
            response += "1. Forfait internet \n"
            response += "2. Forfait Appels \n"
            response += "3. Forfait SMS \n"

    return HttpResponse(response)