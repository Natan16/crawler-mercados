from core.models import Mercado
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def handle(self, *args, **options):
        
        # isso aqui podia ser na hora de rodar o crawler mesmo
        Mercado.objects.get_or_create(
            rede = "SHIBATA",
            cidade = "São José dos Campos",
            uf = "SP",
            bairro = "Jardim Oriente",
            unidade = "Shibata - Jardim Oriente",
            filial = 1
        )

        Mercado.objects.get_or_create(
            rede = "SPANI",
            cidade = "São José dos Campos",
            uf = "SP",
            bairro = "Aquarius",
            unidade = "Spani - Aquarius",
            filial = 1
        )

        Mercado.objects.get_or_create(
            rede = "CARREFOUR",
            cidade = "São José dos Campos",
            uf = "SP",
            bairro = "Jardim Serimbura",
            unidade = "Carrefour - Jardim Serimbura",
            filial = 1
        )

        Mercado.objects.get_or_create(
            rede = "PAO_DE_ACUCAR",
            cidade = "São José dos Campos",
            uf = "SP",
            bairro = "Aquarius",
            unidade = "Pão de Açúcar - Aquarius",
            filial = 461
        )
