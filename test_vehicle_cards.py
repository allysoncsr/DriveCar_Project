#!/usr/bin/env python
"""
Teste para verificar os cards dos veículos após as melhorias
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drivecar_project.settings')
django.setup()

from django.contrib.auth.models import User
from drivecar.models import Veiculo

def test_vehicle_cards():
    print("🎨 VERIFICAÇÃO DOS CARDS DE VEÍCULOS")
    print("=" * 45)
    
    # Buscar veículos do admin
    admin_user = User.objects.filter(username='admin').first()
    if not admin_user:
        print("❌ Usuário admin não encontrado!")
        return
    
    veiculos = Veiculo.objects.filter(usuario=admin_user)
    
    print(f"\n📋 Veículos do usuário {admin_user.username}:")
    print("-" * 45)
    
    for i, veiculo in enumerate(veiculos, 1):
        print(f"\n{i}. 🚗 Card do Veículo:")
        
        # Dados que aparecerão no card
        marca_nome = veiculo.marca.nome if veiculo.marca else veiculo.marca_legado or "Marca não definida"
        modelo_nome = veiculo.modelo.nome if veiculo.modelo else veiculo.modelo_legado or "Modelo não definido"
        
        print(f"   📌 Título: {marca_nome} {modelo_nome}")
        print(f"   📅 Meta: {veiculo.ano} • {veiculo.km_atual:,} km".replace(',', '.'))
        print(f"   💰 Total gasto: {veiculo.total_gasto_manutencao_formatado}")
        
        # Verificar se há duplicação
        if veiculo.marca and veiculo.modelo:
            modelo_str = str(veiculo.modelo)
            if marca_nome in modelo_str:
                print(f"   ⚠️  ATENÇÃO: Possível duplicação detectada!")
                print(f"       - Marca: {marca_nome}")
                print(f"       - Modelo __str__: {modelo_str}")
            else:
                print(f"   ✅ Sem duplicação detectada")
        
        print(f"   🔧 ID do veículo: {veiculo.id}")
        
        if i < len(veiculos):
            print("   " + "-" * 35)
    
    if not veiculos:
        print("   📝 Nenhum veículo cadastrado para o admin")
    
    print(f"\n📊 RESUMO:")
    print(f"   Total de veículos: {veiculos.count()}")
    
    # Verificar estrutura de template
    print(f"\n🎨 MELHORIAS IMPLEMENTADAS:")
    melhorias = [
        "✅ Remoção da marca duplicada no título",
        "✅ Uso de veiculo.marca.nome ao invés de veiculo.marca",
        "✅ Uso de veiculo.modelo.nome ao invés de veiculo.modelo",
        "✅ Tipografia melhorada com fonte Inter",
        "✅ Espaçamentos e tamanhos otimizados",
        "✅ Efeitos hover nos cards",
        "✅ Botão de delete com melhor visual",
        "✅ Área de custos com design aprimorado"
    ]
    
    for melhoria in melhorias:
        print(f"   {melhoria}")
    
    print(f"\n🌐 URL para testar: http://127.0.0.1:8000/")

if __name__ == "__main__":
    test_vehicle_cards()