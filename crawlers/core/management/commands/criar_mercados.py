from core.models import Mercado
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def handle(self, *args, **options):
        

        Mercado.objects.get_or_create(
            rede = "SHIBATA",
            cidade = "São José dos Campos",
            uf = "SP",
            bairro = "Jardim Oriente",
            unidade = "Shibata - Jardim Oriente",
            filial = 1
        )
        # lat -23.237265, long = -45.896721

        Mercado.objects.get_or_create(
            rede = "SPANI",
            cidade = "São José dos Campos",
            uf = "SP",
            bairro = "Aquarius",
            unidade = "Spani - Aquarius",
            filial = 1
        )
        # lat -23.225743, long = -45.910693

        Mercado.objects.get_or_create(
            rede = "CARREFOUR",
            cidade = "São José dos Campos",
            uf = "SP",
            bairro = "Jardim Serimbura",
            unidade = "Carrefour - Jardim Serimbura",
            filial = 1
        )
        # lat -23.222826, long = -45.905961

        Mercado.objects.get_or_create(
            rede = "PAO_DE_ACUCAR",
            cidade = "São José dos Campos",
            uf = "SP",
            bairro = "Aquarius",
            unidade = "Pão de Açúcar - Aquarius",
            filial = 461
        )
        # lat -23.219339, long = -45.905450
