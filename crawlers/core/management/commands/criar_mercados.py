from django.core.management.base import BaseCommand

from core.models import Mercado


class Command(BaseCommand):
    def handle(self, *args, **options):
        Mercado.objects.get_or_create(
            rede="SHIBATA",
            cidade="São José dos Campos",
            uf="SP",
            bairro="Jardim Oriente",
            unidade="Shibata - Jardim Oriente",
            filial=1,
            latitude=-23.237265,
            longitude=-45.896721,
        )

        Mercado.objects.get_or_create(
            rede="SPANI",
            cidade="São José dos Campos",
            uf="SP",
            bairro="Aquarius",
            unidade="Spani - Aquarius",
            filial=1,
            latitude=-23.225743,
            longitude=-45.910693,
        )

        Mercado.objects.get_or_create(
            rede="CARREFOUR",
            cidade="São José dos Campos",
            uf="SP",
            bairro="Jardim Serimbura",
            unidade="Carrefour - Jardim Serimbura",
            filial=1,
            latitude=-23.222826,
            longitude=-45.905961,
        )

        Mercado.objects.get_or_create(
            rede="PAO_DE_ACUCAR",
            cidade="São José dos Campos",
            uf="SP",
            bairro="Aquarius",
            unidade="Pão de Açúcar - Aquarius",
            filial=461,
            latitude=-23.219339,
            longitude=-45.905450,
        )

        Mercado.objects.get_or_create(
            rede="TENDA",
            cidade="São José dos Campos",
            uf="SP",
            bairro="Jardim Satélite",
            unidade="Tenda Atacado - São José dos Campos",
            filial=1,
            latitude=-23.219308,
            longitude=-45.895301,
        )
