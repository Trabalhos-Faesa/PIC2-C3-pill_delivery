from django.db import models

from utils.validators import validate_cpf, validate_digits


class Cliente(models.Model):
    nome: models.CharField = models.CharField(max_length=50)
    sobrenome: models.CharField = models.CharField(blank=True, null=True, max_length=100)
    email: models.EmailField = models.EmailField(unique=True)
    cpf: models.CharField = models.CharField(
        blank=True, null=True,
        max_length=11,
        unique=True,
        validators=[validate_cpf],
        verbose_name='CPF',
    )
    telefone: models.CharField = models.CharField(
        blank=True, null=True,
        max_length=11,
        unique=True,
        validators=[validate_digits],
    )

    def __str__(self):
        return f'#{self.pk}, {self.nome} {self.sobrenome if self.sobrenome else ""} <{self.email}>'


class Farmacia(models.Model):
    nome: models.CharField = models.CharField(max_length=50)
    geo_loc: models.CharField = models.CharField(max_length=50)

    def __str__(self):
        return f'#{self.pk}, [{self.geo_loc}], {self.nome}'


class Medicamento(models.Model):
    nome: models.CharField = models.CharField(max_length=50)
    qtd_estoque: models.PositiveIntegerField = models.PositiveIntegerField(default=0, verbose_name='Qtd. em Estoque')
    farmacia: models.ForeignKey = models.ForeignKey(Farmacia, on_delete=models.PROTECT)
    preco: models.DecimalField = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'#{self.pk}, {self.qtd_estoque}x {self.nome}'


class Entregador(models.Model):
    nome: models.CharField = models.CharField(max_length=50)
    sobrenome: models.CharField = models.CharField(
        blank=True, null=True,
        max_length=100,
    )
    email: models.EmailField = models.EmailField(unique=True)
    cpf: models.CharField = models.CharField(
        blank=True, null=True,
        unique=True,
        max_length=11,
        validators=[validate_cpf],
        verbose_name='CPF',
    )
    telefone: models.CharField = models.CharField(
        max_length=11,
        unique=True,
        validators=[validate_digits],
    )

    def __str__(self):
        return f'#{self.pk}, {self.nome} {self.sobrenome if self.sobrenome else ""} <{self.email}> <{self.telefone}>'

    class Meta:
        verbose_name_plural = 'Entregadores'


class Entrega(models.Model):
    entregador: models.OneToOneField = models.OneToOneField(
        Entregador,
        on_delete=models.PROTECT,
    )
    real_time_geo_loc_key: models.CharField = models.CharField(
        blank=True, null=True,
        max_length=50,
    )

    def __str__(self):
        return f'#{self.pk}, [{self.real_time_geo_loc_key}], [Entregador: {self.entregador}]'


class Pedido(models.Model):
    class Status(models.IntegerChoices):
        CLIENTE_ESCOLHENDO = 0, 'Cliente escolhendo'
        SOLICITADO = 1, 'Solicitado'
        SENDO_SEPARADO = 2, 'Sendo separado'
        A_CAMINHO = 3, 'A caminho'
        ENTREGUE = 4, 'Entregue'

    status: models.PositiveSmallIntegerField = models.PositiveSmallIntegerField(choices=Status.choices)
    data: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    cliente: models.ForeignKey = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    entrega: models.ForeignKey = models.ForeignKey(
        Entrega,
        blank=True, null=True,
        related_name='pedidos',
        on_delete=models.PROTECT,
    )

    @property
    def status_label(self):
        return Pedido.Status(self.status).label

    def __str__(self):
        return f'#{self.pk}, [Status: {self.status_label}], [Cliente: {self.cliente}], [Entrega: {self.entrega}]'


class ItemPedido(models.Model):
    pedido: models.ForeignKey = models.ForeignKey(
        Pedido,
        related_name='itens',
        on_delete=models.CASCADE,
    )
    medicamento: models.ForeignKey = models.ForeignKey(
        Medicamento,
        on_delete=models.DO_NOTHING,
    )
    quantidade: models.PositiveIntegerField = models.PositiveIntegerField(default=1)
    preco_unitario: models.DecimalField = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def sub_total(self):
        return self.quantidade * self.preco_unitario

    def __str__(self):
        return f'{self.quantidade}x {self.medicamento.nome}, [Pedido: {self.pedido}]'

    class Meta:
        unique_together = ('pedido', 'medicamento')
        verbose_name = 'Item do Pedido'
        verbose_name_plural = 'Itens do Pedido'
