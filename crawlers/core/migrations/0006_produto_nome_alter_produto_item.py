# Generated by Django 4.0.5 on 2022-07-03 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_crawl_remove_produto_mercado_remove_produto_preco_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='nome',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='produto',
            name='item',
            field=models.CharField(max_length=512, unique=True),
        ),
    ]