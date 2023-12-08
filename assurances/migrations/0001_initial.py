# Generated by Django 4.0 on 2023-11-27 11:12

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assure',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=50)),
                ('prenom', models.CharField(max_length=50)),
                ('postnom', models.CharField(max_length=50)),
                ('number', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicule',
            fields=[
                ('numero_chassis', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('marque', models.CharField(max_length=30)),
                ('plaque', models.CharField(max_length=30)),
                ('date_fabrication', models.DateField(auto_now=True)),
                ('SoldeKwh', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=5)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assurances.assure')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('transaction_id', models.CharField(max_length=30)),
                ('amount', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=5)),
                ('operation_date', models.DateField(auto_now=True)),
                ('EquivKwh', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=5)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='assurances.assure')),
                ('meter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='assurances.vehicule')),
            ],
        ),
    ]
