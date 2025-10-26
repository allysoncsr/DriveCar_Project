#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drivecar_project.settings')
django.setup()

from django.test import RequestFactory, Client
from django.contrib.auth.models import User
from drivecar.models import Veiculo, Peca
from drivecar.views import registros_peca
import json

print("=== TESTE DE SIMULAÇÃO DE FORMULÁRIO ===\n")

# Configurar cliente de teste
client = Client()

# Fazer login
user = User.objects.get(username='admin')
veiculo = Veiculo.objects.filter(usuario=user).first()
peca = Peca.objects.first()

if not (user and veiculo and peca):
    print("❌ Dados de teste não encontrados")
    exit()

print(f"📋 Dados de teste:")
print(f"   👤 Usuário: {user.username}")
print(f"   🚗 Veículo: {veiculo}")
print(f"   🔧 Peça: {peca}")

# Login no cliente
client.force_login(user)

# Simular POST com o valor que está causando problema
print(f"\n🧪 SIMULANDO POST COM PREÇO 25020:")

url = f'/veiculo/{veiculo.id}/peca/{peca.id}/registros/'
data = {
    'data': '2025-10-26',
    'km': '100000',
    'preco': '25020',  # Valor exato que o usuário está tentando salvar
    'troca': False,
    'garantia_meses': '',
    'observacoes': 'Teste simulação'
}

print(f"   📝 URL: {url}")
print(f"   📝 Dados: {data}")

response = client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

print(f"   📊 Status: {response.status_code}")
print(f"   📊 Content-Type: {response.get('Content-Type', 'N/A')}")

if response.status_code == 200:
    content = response.content.decode('utf-8')
    print(f"   ✅ Resposta recebida ({len(content)} caracteres)")
    
    # Verificar se há indicação de erro no HTML
    if 'form.errors' in content or 'error' in content.lower():
        print(f"   ⚠️  Possível erro no formulário")
    
    if 'Registro salvo com sucesso' in content:
        print(f"   ✅ Sucesso detectado na resposta")
    else:
        print(f"   ❌ Mensagem de sucesso não encontrada")
        
    # Mostrar trecho da resposta para debug
    lines = content.split('\n')[:10]  # Primeiras 10 linhas
    print(f"   📄 Primeiras linhas da resposta:")
    for i, line in enumerate(lines, 1):
        print(f"      {i:2d}: {line}")
        
else:
    print(f"   ❌ Erro HTTP: {response.status_code}")
    print(f"   📄 Conteúdo: {response.content.decode('utf-8')}")

# Verificar se o registro foi realmente salvo
print(f"\n🔍 VERIFICANDO BANCO DE DADOS:")
from drivecar.models import RegistroManutencao

registros_teste = RegistroManutencao.objects.filter(
    veiculo=veiculo,
    peca=peca,
    observacoes='Teste simulação'
)

if registros_teste.exists():
    reg = registros_teste.first()
    print(f"   ✅ Registro encontrado!")
    print(f"   💰 Preço salvo: {reg.preco}")
    print(f"   📅 Data: {reg.data}")
    print(f"   🚗 KM: {reg.km}")
    
    # Limpar teste
    reg.delete()
    print(f"   🧹 Registro de teste removido")
else:
    print(f"   ❌ Registro não foi salvo no banco")

print(f"\n✅ Teste de simulação concluído!")