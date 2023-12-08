# Generated by Django 4.0.5 on 2022-07-02 19:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_mercado_unidade"),
    ]

    operations = [
        migrations.AddField(
            model_name="produto",
            name="categoria",
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name="produto",
            name="departamento",
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name="produto",
            name="mercado",
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to="core.mercado"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="produto",
            name="peso_g",
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
        migrations.AddField(
            model_name="produto",
            name="volume_ml",
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
    ]
