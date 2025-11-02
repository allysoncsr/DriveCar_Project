from django.urls import path
from . import views

app_name = "drivecar"

urlpatterns = [
    # Autenticação
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("register/", views.register, name="register"),
    
    # Páginas principais
    path("", views.index, name="index"),
    
    # Veículos
    path("veiculos/cadastrar/", views.cadastrar_veiculo, name="cadastrar_veiculo"),
    path("veiculos/<int:veiculo_id>/editar/", views.editar_veiculo, name="editar_veiculo"),
    path("veiculos/<int:veiculo_id>/excluir/", views.excluir_veiculo, name="excluir_veiculo"),
    
    # Manutenção
    path("veiculo/<int:veiculo_id>/manutencao/", views.manutencao, name="manutencao"),
    path("registro/<int:registro_id>/excluir/", views.excluir_registro, name="excluir_registro"),
    
    # APIs para select cascateado
    path("api/modelos/<int:marca_id>/", views.api_modelos, name="api_modelos"),
    path("api/versoes/<int:modelo_id>/", views.api_versoes, name="api_versoes"),
]