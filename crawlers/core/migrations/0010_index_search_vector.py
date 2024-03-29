# Generated by Django 4.2.8 on 2023-12-20 15:33

import django.contrib.postgres.indexes
import django.contrib.postgres.search
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0009_adiciona_coordenadas_geograficas_do_mercado"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="produto",
            index=django.contrib.postgres.indexes.GinIndex(
                django.contrib.postgres.search.SearchVector(
                    "nome", "departamento", "categoria", config="portuguese"
                ),
                name="produto_search_vector_idx",
            ),
        ),
    ]
