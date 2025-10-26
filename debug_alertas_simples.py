#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drivecar_project.settings')
django.setup()

from drivecar.models import *
from django.contrib.auth.models import User
from datetime import datetime, date

# Verificar se existem alertas
print("=== DEBUG DE ALERTAS ===")

# Buscar todos os usuários
users = User.objects.all()
print(f"Usuários encontrados: {[u.username for u in users]}")

for user in users:
    print(f"\n--- Usuário: {user.username} ---")
    veiculos = user.veiculo_set.all()
    print(f"Veículos: {veiculos.count()}")
    
    for veiculo in veiculos:
        print(f"  Veículo: {veiculo.modelo} (KM: {veiculo.km_atual})")
        
        # Verificar registros
        registros = RegistroManutencao.objects.filter(veiculo=veiculo)
        print(f"  Registros de manutenção: {registros.count()}")
        
        # Verificar alertas
        try:
            alertas = veiculo.get_alertas_ativos()
            print(f"  Alertas ativos: {len(alertas)}")
            
            for alerta in alertas:
                print(f"    - {alerta['item']}: {alerta['descricao']} (Tipo: {alerta['tipo']})")
                
                # Verificar se a peça existe
                try:
                    peca = Peca.objects.get(nome=alerta['item'])
                    categoria = peca.get_categoria_display()
                    print(f"      Categoria: {categoria}")
                except Peca.DoesNotExist:
                    print(f"      ERRO: Peça '{alerta['item']}' não encontrada no banco!")
                    
        except Exception as e:
            print(f"  ERRO ao obter alertas: {e}")

print("\n=== TODAS AS PEÇAS CADASTRADAS ===")
pecas = Peca.objects.all()
for peca in pecas:
    print(f"- {peca.nome} (Categoria: {peca.get_categoria_display()})")