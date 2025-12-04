from django.contrib import admin

from .models import (
    Cliente,
    Entrega,
    Entregador,
    Farmacia,
    ItemPedido,
    Medicamento,
    Pedido,
)


admin.site.register(Cliente)
admin.site.register(Entrega)
admin.site.register(Entregador)
admin.site.register(Farmacia)
admin.site.register(ItemPedido)
admin.site.register(Medicamento)
admin.site.register(Pedido)
