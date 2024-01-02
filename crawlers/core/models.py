from enum import Enum

from django.db import models
from django.db.models.fields import DecimalField

from commons.geoutils import Coords
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVector

UFS = [
    ("AC", "Acre"),
    ("AL", "Alagoas"),
    ("AP", "Amapá"),
    ("AM", "Amazonas"),
    ("BA", "Bahia"),
    ("CE", "Ceará"),
    ("DF", "Distrito Federal"),
    ("ES", "Espírito Santo"),
    ("GO", "Goiás"),
    ("MA", "Maranhão"),
    ("MT", "Mato Grosso"),
    ("MS", "Mato Grosso do Sul"),
    ("MG", "Minas Gerais"),
    ("PA", "Pará"),
    ("PB", "Paraíba"),
    ("PR", "Paraná"),
    ("PE", "Pernambuco"),
    ("PI", "Piauí"),
    ("RJ", "Rio de Janeiro"),
    ("RN", "Rio Grande do Norte"),
    ("RS", "Rio Grande do Sul"),
    ("RO", "Rondônia"),
    ("RR", "Roraima"),
    ("SC", "Santa Catarina"),
    ("SP", "São Paulo"),
    ("SE", "Sergipe"),
    ("TO", "Tocantins"),
    ("EX", "Exterior"),
]


class Mercado(models.Model):
    rede = models.CharField(max_length=32)
    cidade = models.CharField(max_length=256)
    uf = models.CharField(max_length=2, null=True, blank=True, choices=UFS)
    bairro = models.CharField(max_length=1024, blank=True, null=True)
    unidade = models.CharField(max_length=1024, blank=True, null=True)
    filial = models.PositiveSmallIntegerField(default=1)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    @property
    def coordenadas(self):
        return Coords(self.latitude, self.longitude)


class UnidadeDeMedida(Enum):
    GRAMA = "grama"
    ML = "minilitro"
    NENHUMA = "nenhuma"


class Produto(models.Model):
    item = models.CharField(max_length=512, unique=True)
    nome = models.CharField(max_length=512, null=True, blank=True)  # TODO: tirar os espaços entre o peso e sua unidade
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categoria = models.CharField(max_length=128, null=True, blank=True)
    departamento = models.CharField(max_length=128, null=True, blank=True)
    peso_bruto = DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    peso_liquido = DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    volume_ml = DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    unidades = models.IntegerField(default=1)

    @property
    def medida(self):
        return self.volume_ml or self.peso_liquido or self.peso_bruto or 1

    @property
    def unidade_de_medida(self):
        if self.volume_ml is not None:
            return UnidadeDeMedida.ML
        if self.peso_liquido is not None or self.peso_bruto is not None:
            return UnidadeDeMedida.GRAMA
        return UnidadeDeMedida.NENHUMA
    
    class Meta:
        indexes = [
            GinIndex(
                SearchVector("nome", "departamento", "categoria", config="portuguese"),
                name="produto_search_vector_idx",
            )
        ]


class Crawl(models.Model):
    mercado = models.ForeignKey(Mercado, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)


class ProdutoCrawl(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    crawl = models.ForeignKey(Crawl, on_delete=models.CASCADE)
    preco = DecimalField(max_digits=12, decimal_places=2)

    def to_dict_json(self):
        return {
            "id": self.pk,
            "produto": {"nome": self.produto.nome, "id": self.produto.pk},
            "mercado": {"unidade": self.crawl.mercado.unidade, "rede": self.crawl.mercado.rede},
            "preco": self.preco,
        }


# l = [set(p.produtocrawl_set.all().values_list("preco")) for p in Produto.objects.all()[:100] if len(set([pc.crawl.mercado_id for pc in ProdutoCrawl.objects.filter(produto=p)])) > 1]
