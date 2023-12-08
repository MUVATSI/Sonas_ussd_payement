from decimal import Decimal
from django.contrib.auth.models import User
from django.db import models


# My models are implemented here.
#
class Assure(models.Model):
    id = models.AutoField(primary_key=True)
    GENRES = (
        ('M', 'Masculin'),
        ('F', 'Feminin'),
    )
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    postnom = models.CharField(max_length=50)
    numero = models.CharField(max_length=50)
    addresse = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    genre = models.CharField(max_length=1, default='M', choices= GENRES)
    date_enr = models.DateTimeField(auto_now_add=True)
    enr_par = models.ForeignKey(User,null=True, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Assure"
        verbose_name_plural = "Assures"

    def __str__(self):
        return self.nom


# ----VEHICULE_CLASS------#
class Vehicule(models.Model):
    numero_chassis = models.CharField(primary_key=True, max_length=20)
    marque = models.CharField(max_length=30)
    plaque = models.CharField(max_length=30)
    date_fabrication = models.DateField()
    assure = models.ForeignKey(Assure,null=True, on_delete=models.SET_NULL)
    # taxe = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))

    class Meta:
        verbose_name = "Vehicule"
        verbose_name_plural = "Vehicules"

    def __str__(self):
        return f"{self.assure}_{self.marque}"


# ----------------PAYEMENT_CLASS------#
class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    assure = models.ForeignKey(Assure,null=True, on_delete=models.CASCADE)
    enr_par = models.ForeignKey(User,null=True, on_delete=models.PROTECT)
    vehicule = models.ForeignKey(Vehicule,null=True, on_delete=models.SET_NULL)
    transaction_id = models.CharField(max_length=30)
    montant = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    date_operation = models.DateTimeField(auto_now=True)
    mis_ajour = models.DateField(null=True, blank=True)
    verifie = models.BooleanField(default=False)
    # Mois_Equivalent = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))

    class Meta:
        verbose_name = "Payement"
        verbose_name_plural = "Payements"

    def __str__(self):
        return f"{self.assure}_{self.date_operation}"