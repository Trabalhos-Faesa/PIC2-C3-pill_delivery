from django.shortcuts import render
from django.urls import path

from cliente.models import Entrega


app_name = 'cliente'

urlpatterns = [
    path(
        'raw-list-entregas',
        lambda req: render(
            req,
            'cliente/raw-list-entregas.html',
            {
                'title': 'Home',
                'entregas': Entrega.objects.filter(pedidos__isnull=False).distinct(),
            },
        ),
        name='raw-list-entregas',
    ),
]
