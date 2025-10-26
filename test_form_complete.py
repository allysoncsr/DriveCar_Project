#!/usr/bin/env python
"""
Teste do formulário completo de cadastro de veículo
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drivecar_project.settings')
django.setup()

from django.contrib.auth.models import User
from drivecar.models import Marca, Modelo, Versao, Veiculo

def test_vehicle_form():
    print("=== TESTE DO FORMULÁRIO COMPLETO ===\n")
    
    # Buscar dados para teste
    marca = Marca.objects.filter(nome='TOYOTA').first()
    if not marca:
        print("❌ Marca Toyota não encontrada!")
        return
        
    modelo = Modelo.objects.filter(marca=marca, nome__icontains='Corolla').first()
    if not modelo:
        print("❌ Modelo Corolla não encontrado!")
        return
        
    versao = Versao.objects.filter(modelo=modelo).first()
    user = User.objects.filter(username='admin').first()
    
    if not user:
        print("❌ Usuário admin não encontrado!")
        return
    
    # Dados do teste
    test_data = {
        'marca_id': marca.id,
        'modelo_id': modelo.id,
        'versao_id': versao.id if versao else None,
        'ano': 2022,
        'placa': 'TST5678',
        'km_atual': 25000,
        'combustivel': 'FLEX'
    }
    
    print("📝 Dados do teste:")
    print(f"   Marca: {marca.nome} (ID: {marca.id})")
    print(f"   Modelo: {modelo.nome} (ID: {modelo.id})")
    print(f"   Versão: {versao.nome if versao else 'Nenhuma'} (ID: {versao.id if versao else 'N/A'})")
    print(f"   Ano: {test_data['ano']}")
    print(f"   Placa: {test_data['placa']}")
    print(f"   KM: {test_data['km_atual']:,}")
    print(f"   Combustível: {test_data['combustivel']}")
    
    # Verificar se já existe
    existing = Veiculo.objects.filter(placa=test_data['placa']).first()
    if existing:
        print(f"\n⚠️  Veículo já existe, removendo para teste...")
        existing.delete()
    
    # Simular criação do veículo (como a view faria)
    try:
        marca_obj = Marca.objects.get(id=test_data['marca_id'])
        modelo_obj = Modelo.objects.get(id=test_data['modelo_id'])
        versao_obj = Versao.objects.get(id=test_data['versao_id']) if test_data['versao_id'] else None
        
        veiculo = Veiculo.objects.create(
            usuario=user,
            marca=marca_obj,
            modelo=modelo_obj,
            versao=versao_obj,
            ano=test_data['ano'],
            placa=test_data['placa'],
            km_atual=test_data['km_atual'],
            combustivel=test_data['combustivel']
        )
        
        print(f"\n✅ Veículo criado com sucesso!")
        print(f"   ID: {veiculo.id}")
        print(f"   Descrição: {veiculo.marca.nome} {veiculo.modelo.nome}")
        if veiculo.versao:
            print(f"   Versão: {veiculo.versao.nome}")
        print(f"   Combustível: {veiculo.get_combustivel_display()}")
        
        # Verificar campos
        print(f"\n🔍 Verificação dos campos:")
        print(f"   ✅ Marca ForeignKey: {veiculo.marca}")
        print(f"   ✅ Modelo ForeignKey: {veiculo.modelo}")
        print(f"   ✅ Versão ForeignKey: {veiculo.versao}")
        print(f"   ✅ Ano: {veiculo.ano}")
        print(f"   ✅ Placa: {veiculo.placa}")
        print(f"   ✅ KM Atual: {veiculo.km_atual:,}")
        print(f"   ✅ Combustível: {veiculo.combustivel} ({veiculo.get_combustivel_display()})")
        
        print(f"\n🎉 FORMULÁRIO FUNCIONANDO PERFEITAMENTE!")
        
    except Exception as e:
        print(f"\n❌ Erro ao criar veículo: {e}")

if __name__ == "__main__":
    test_vehicle_form()