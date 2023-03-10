from django.db import migrations
from django.contrib.postgres.operations import UnaccentExtension, TrigramExtension


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_remove_produto_peso_g_mercado_filial_and_more'),
    ]

    operations = [
        UnaccentExtension(),
        TrigramExtension()
    ]
