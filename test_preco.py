#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drivecar_project.settings')
django.setup()

from drivecar.models import Veiculo, Peca, RegistroManutencao
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import date

print("=== TESTE DE SALVAMENTO DE PREÇO ===\n")

# Buscar usuário e veículo para teste
user = User.objects.first()
veiculo = Veiculo.objects.filter(usuario=user).first()
peca = Peca.objects.first()

if not (user and veiculo and peca):
    print("❌ Dados de teste não encontrados")
    print(f"   Usuário: {user}")
    print(f"   Veículo: {veiculo}")
    print(f"   Peça: {peca}")
    exit()

print(f"📋 Dados de teste:")
print(f"   👤 Usuário: {user.username}")
print(f"   🚗 Veículo: {veiculo}")
print(f"   🔧 Peça: {peca}")

# Teste com diferentes formatos de preço
valores_teste = [
    "25020",      # Valor simples
    "250.20",     # Com ponto decimal
    "250,20",     # Com vírgula decimal
    "25.020,00",  # Formato brasileiro completo
    "R$ 25.020,00",  # Com R$
]

print(f"\n🧪 TESTANDO CONVERSÕES:")

for valor_original in valores_teste:
    print(f"\n   📝 Testando: '{valor_original}'")
    
    # Simular processamento da view
    try:
        # Remove R$, espaços e pontos (milhares), converte vírgula para ponto
        if 'R$' in valor_original:
            preco_numerico = valor_original.replace('R$', '').replace(' ', '').replace('.', '').replace(',', '.')
        elif ',' in valor_original and '.' not in valor_original:
            # Apenas vírgula, é decimal brasileiro
            preco_numerico = valor_original.replace(',', '.')
        elif '.' in valor_original and ',' in valor_original:
            # Formato brasileiro: ponto para milhares, vírgula para decimal
            preco_numerico = valor_original.replace('.', '').replace(',', '.')
        else:
            # Valor simples
            preco_numerico = valor_original
            
        valor_decimal = Decimal(preco_numerico)
        print(f"      ✅ Convertido para: {valor_decimal}")
        
        # Tentar salvar no banco
        registro = RegistroManutencao(
            veiculo=veiculo,
            peca=peca,
            data=date.today(),
            km=100000,
            preco=valor_decimal,
            troca=False
        )
        registro.full_clean()  # Validação
        print(f"      ✅ Validação: OK")
        
    except Exception as e:
        print(f"      ❌ Erro: {e}")

# Teste específico com o valor 25020
print(f"\n🎯 TESTE ESPECÍFICO COM 25020:")
try:
    registro_teste = RegistroManutencao.objects.create(
        veiculo=veiculo,
        peca=peca,
        data=date.today(),
        km=100001,
        preco=Decimal('25020.00'),
        troca=False,
        observacoes="Teste automático - preço 25020"
    )
    print(f"   ✅ Registro criado com ID: {registro_teste.id}")
    print(f"   💰 Preço salvo: {registro_teste.preco}")
    
    # Limpar teste
    registro_teste.delete()
    print(f"   🧹 Registro de teste removido")
    
except Exception as e:
    print(f"   ❌ Erro ao salvar: {e}")

print(f"\n✅ Teste concluído!")