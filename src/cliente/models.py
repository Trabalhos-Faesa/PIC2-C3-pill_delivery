from django.db import models

from utils.validators import validate_cpf, validate_digits


class Cliente(models.Model):
    nome: models.CharField = models.CharField(max_length=20)
    sobrenome: models.CharField = models.CharField(max_length=100)
    email: models.EmailField = models.EmailField()
    cpf: models.CharField = models.CharField(max_length=11, unique=True, validators=[validate_cpf], verbose_name='CPF')
    telefone: models.CharField = models.CharField(max_length=11, unique=True, validators=[validate_digits])

    def __str__(self):
        return f'#{self.pk}, {self.nome} <{self.email}>'
