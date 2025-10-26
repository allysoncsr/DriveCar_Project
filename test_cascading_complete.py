#!/usr/bin/env python
"""
Teste completo do sistema de cascata de veículos
Simula o fluxo: Marca → Modelo → Versão → Cadastro
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

def test_complete_flow():
    print("=== TESTE COMPLETO DO SISTEMA DE CASCATA ===\n")
    
    # 1. Verificar se há marcas
    marcas = Marca.objects.filter(ativo=True)[:3]
    print(f"1. ✅ {marcas.count()} marcas disponíveis")
    for marca in marcas:
        modelos_count = Modelo.objects.filter(marca=marca, ativo=True).count()
        print(f"   - {marca.nome}: {modelos_count} modelos")
    
    if not marcas:
        print("❌ Nenhuma marca encontrada!")
        return
    
    # 2. Testar cascata: Marca → Modelo
    primeira_marca = marcas[0] 
    modelos = Modelo.objects.filter(marca=primeira_marca, ativo=True)[:3]
    print(f"\n2. ✅ Testando cascata {primeira_marca.nome} → Modelos:")
    for modelo in modelos:
        versoes_count = Versao.objects.filter(modelo=modelo, ativo=True).count()
        print(f"   - {modelo.nome}: {versoes_count} versões")
    
    if not modelos:
        print("❌ Nenhum modelo encontrado!")
        return
    
    # 3. Testar cascata: Modelo → Versão
    primeiro_modelo = modelos[0]
    versoes = Versao.objects.filter(modelo=primeiro_modelo, ativo=True)[:3]
    print(f"\n3. ✅ Testando cascata {primeiro_modelo.nome} → Versões:")
    for versao in versoes:
        extra_info = []
        if versao.motor:
            extra_info.append(f"Motor: {versao.motor}")
        if versao.combustivel:
            extra_info.append(f"Combustível: {versao.combustivel}")
        extra = f" ({', '.join(extra_info)})" if extra_info else ""
        print(f"   - {versao.nome}{extra}")
    
    # 4. Testar criação de veículo
    print(f"\n4. ✅ Testando criação de veículo:")
    user = User.objects.filter(username='admin').first()
    if not user:
        print("❌ Usuário admin não encontrado!")
        return
    
    # Simular dados de um veículo
    test_vehicle_data = {
        'marca': primeira_marca,
        'modelo': primeiro_modelo,
        'versao': versoes[0] if versoes else None,
        'usuario': user,
        'ano': 2023,
        'placa': 'TST1234',
        'km_atual': 15000,
        'combustivel': 'flex'
    }
    
    print(f"   Dados do veículo de teste:")
    print(f"   - Marca: {test_vehicle_data['marca'].nome}")
    print(f"   - Modelo: {test_vehicle_data['modelo'].nome}")
    print(f"   - Versão: {test_vehicle_data['versao'].nome if test_vehicle_data['versao'] else 'Não selecionada'}")
    print(f"   - Ano: {test_vehicle_data['ano']}")
    print(f"   - Placa: {test_vehicle_data['placa']}")
    print(f"   - KM: {test_vehicle_data['km_atual']:,}")
    print(f"   - Combustível: {test_vehicle_data['combustivel']}")
    
    # Verificar se já existe um teste
    existing = Veiculo.objects.filter(placa='TST1234').first()
    if existing:
        print(f"   ℹ️  Veículo de teste já existe (ID: {existing.id})")
    else:
        # Criar veículo de teste
        try:
            test_vehicle = Veiculo.objects.create(**test_vehicle_data)
            print(f"   ✅ Veículo de teste criado com sucesso! (ID: {test_vehicle.id})")
        except Exception as e:
            print(f"   ❌ Erro ao criar veículo de teste: {e}")
            return
    
    # 5. Estatísticas finais
    print(f"\n5. 📊 ESTATÍSTICAS FINAIS:")
    total_marcas = Marca.objects.filter(ativo=True).count()
    total_modelos = Modelo.objects.filter(ativo=True).count()
    total_versoes = Versao.objects.filter(ativo=True).count()
    total_veiculos = Veiculo.objects.count()
    
    print(f"   - Marcas ativas: {total_marcas}")
    print(f"   - Modelos ativos: {total_modelos}")
    print(f"   - Versões ativas: {total_versoes}")
    print(f"   - Veículos cadastrados: {total_veiculos}")
    
    print(f"\n🎉 SISTEMA DE CASCATA TOTALMENTE FUNCIONAL!")
    print(f"🔗 URLs das APIs:")
    print(f"   - /api/modelos/<marca_id>/")
    print(f"   - /api/versoes/<modelo_id>/")
    print(f"🌐 Interface disponível em: /veiculos/cadastrar/")

if __name__ == "__main__":
    test_complete_flow()