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
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/veiculo/<int:veiculo_id>/", views.dashboard_veiculo, name="dashboard_veiculo"),
    
    # Veículos
    path("veiculos/cadastrar/", views.cadastrar_veiculo, name="cadastrar_veiculo"),
    path("veiculos/<int:veiculo_id>/editar/", views.editar_veiculo, name="editar_veiculo"),
    path("veiculos/<int:veiculo_id>/excluir/", views.excluir_veiculo, name="excluir_veiculo"),
    
    # Manutenção
    path("veiculo/<int:veiculo_id>/manutencao/", views.manutencao, name="manutencao"),
    path("registro/<int:registro_id>/editar/", views.editar_registro, name="editar_registro"),
    path("registro/<int:registro_id>/excluir/", views.excluir_registro, name="excluir_registro"),
    
    # Alertas
    path("alertas/", views.alertas, name="alertas"),
    path("alertas/veiculo/<int:veiculo_id>/", views.alertas_veiculo_fragment, name="alertas_veiculo_fragment"),
    path("registro/<int:registro_id>/desativar-alerta/", views.desativar_alerta, name="desativar_alerta"),
    path("api/alertas/", views.lista_alertas, name="lista_alertas"),
    
    # Fragments HTMX
    path("veiculo/<int:veiculo_id>/registros/", views.registros_fragment, name="registros_fragment"),
    
    # Exportação
    path("export/pdf/", views.export_pdf, name="export_pdf"),
    path("export/excel/", views.export_excel, name="export_excel"),
    
    # PWA
    path("offline/", views.offline, name="offline"),
]