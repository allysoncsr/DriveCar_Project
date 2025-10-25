from django.contrib import admin
from .models import Veiculo, Peca, RegistroManutencao, Alerta

@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ("marca", "modelo", "ano", "placa", "km_atual")
    search_fields = ("marca", "modelo", "placa")


@admin.register(Peca)
class PecaAdmin(admin.ModelAdmin):
    list_display = ("nome", "categoria")
    list_filter = ("categoria",)
    search_fields = ("nome",)


@admin.register(RegistroManutencao)
class RegistroAdmin(admin.ModelAdmin):
    list_display = ("veiculo", "peca", "data", "km", "preco", "troca")
    list_filter = ("peca__categoria", "troca")
    search_fields = ("veiculo__placa", "peca__nome")


@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    list_display = ("descricao", "veiculo", "tipo", "km_previsto", "data_prevista", "ativo")
    list_filter = ("tipo", "ativo")
    search_fields = ("descricao",)
