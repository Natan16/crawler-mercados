from django.contrib.postgres.operations import TrigramExtension, UnaccentExtension
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0007_remove_produto_peso_g_mercado_filial_and_more"),
    ]

    operations = [UnaccentExtension(), TrigramExtension()]
