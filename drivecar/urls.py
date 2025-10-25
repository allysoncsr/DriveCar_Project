from django.urls import path
from . import views

app_name = "drivecar"

urlpatterns = [
    path("", views.index, name="index"),  # página inicial
    path("veiculos/cadastrar/", views.cadastrar_veiculo, name="cadastrar_veiculo"),
    path("veiculos/<int:veiculo_id>/excluir/", views.excluir_veiculo, name="excluir_veiculo"),
    path("alertas/", views.lista_alertas, name="lista_alertas"),
    # endpoints HTMX (ex.: carregar lista de registros)
    path("veiculo/<int:veiculo_id>/registros/", views.registros_veiculo, name="registros_veiculo"),
    path("veiculo/<int:veiculo_id>/manutencao/", views.manutencao, name="manutencao"),
    path("veiculo/<int:veiculo_id>/peca/<int:peca_id>/registros/", views.registros_peca, name="registros_peca"),
    path("veiculo/<int:veiculo_id>/peca/<int:peca_id>/registro/<int:registro_id>/excluir/", views.excluir_registro, name="excluir_registro"),
    path("api/veiculo/<int:veiculo_id>/peca/<int:peca_id>/registros/", views.api_registro_create, name="api_registro_create"),
]
