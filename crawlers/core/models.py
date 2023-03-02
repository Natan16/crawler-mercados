
from django.db import models
from django.db.models.fields import DecimalField

UFS = [
    ('AC', 'Acre'),
    ('AL', 'Alagoas'),
    ('AP', 'Amapá'),
    ('AM', 'Amazonas'),
    ('BA', 'Bahia'),
    ('CE', 'Ceará'),
    ('DF', 'Distrito Federal'),
    ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'),
    ('MA', 'Maranhão'),
    ('MT', 'Mato Grosso'),
    ('MS', 'Mato Grosso do Sul'),
    ('MG', 'Minas Gerais'),
    ('PA', 'Pará'),
    ('PB', 'Paraíba'),
    ('PR', 'Paraná'),
    ('PE', 'Pernambuco'),
    ('PI', 'Piauí'),
    ('RJ', 'Rio de Janeiro'),
    ('RN', 'Rio Grande do Norte'),
    ('RS', 'Rio Grande do Sul'),
    ('RO', 'Rondônia'),
    ('RR', 'Roraima'),
    ('SC', 'Santa Catarina'),
    ('SP', 'São Paulo'),
    ('SE', 'Sergipe'),
    ('TO', 'Tocantins'),
    ('EX', 'Exterior'),
]

class Mercado(models.Model):
    rede = models.CharField(max_length=32)
    cidade = models.CharField(max_length=256)
    uf = models.CharField(max_length=2, null=True, blank=True, choices=UFS)
    bairro = models.CharField(max_length=1024, blank=True, null=True)
    unidade = models.CharField(max_length=1024, blank=True, null=True)
    filial = models.PositiveSmallIntegerField(default=1)
    
    # TODO: rede+filial unique toguether
    
class Produto(models.Model):
    item = models.CharField(max_length=512, unique=True)
    nome = models.CharField(max_length=512, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categoria = models.CharField(max_length=128, null=True, blank=True)
    departamento = models.CharField(max_length=128, null=True, blank=True)
    peso_bruto = DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    peso_liquido = DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    # ainda não sei de onde tirar o volume
    volume_ml = DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    unidades = models.IntegerField(default=1)

class Crawl(models.Model):
    mercado = models.ForeignKey(Mercado, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

class ProdutoCrawl(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    crawl = models.ForeignKey(Crawl, on_delete=models.CASCADE)
    preco = DecimalField(max_digits=12, decimal_places=2)

    def to_dict_json(self):
        return {
            "produto": {"nome": self.produto.nome},
            "mercado": {"unidade": self.crawl.mercado.unidade},
            "preco": self.preco
        }
