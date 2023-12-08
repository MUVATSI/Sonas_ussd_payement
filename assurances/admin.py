from django.contrib import admin
from .models import Assure, Payment,Vehicule


class AdminAssure(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'postnom', 'numero', 'email', 'genre', 'date_enr')


class AdminVehicule(admin.ModelAdmin):
    list_display = ('assure', 'marque', 'plaque', 'numero_chassis', 'date_fabrication')


class AdminPayment(admin.ModelAdmin):
    list_display = ('assure', 'vehicule', 'montant', 'date_operation', 'mis_ajour', 'verifie')


admin.site.register(Assure, AdminAssure)
admin.site.register(Vehicule, AdminVehicule)
admin.site.register(Payment, AdminPayment)
admin.site.site_header = "SUPER ADMINISTRATEUR"
admin.site.site_title = ("SONAS POUR VOS ASSURANCES")
admin.site.index_title = ("APPLICATION DE GESTION D'ASSURANCE")
