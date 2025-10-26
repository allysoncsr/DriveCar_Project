#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drivecar_project.settings')
django.setup()

from drivecar.models import *
from django.contrib.auth.models import User

# Testar com o usuário allysonrocha que tem alertas
user = User.objects.get(username='allysonrocha')
veiculo = user.veiculo_set.first()

print(f"Testando com veículo: {veiculo.modelo}")
print(f"KM atual: {veiculo.km_atual}")

alertas = veiculo.get_alertas_ativos()
print(f"\nAlertas encontrados: {len(alertas)}")

for alerta in alertas:
    print(f"\nAlerta:")
    print(f"  Item: {alerta['item']}")
    print(f"  Peça completa: {alerta.get('peca_completa', 'N/A')}")
    print(f"  Status: {alerta['status']}")
    print(f"  Urgência: {alerta['urgencia']}")
    
    # Testar busca da peça
    peca_nome = alerta['item']
    peca_completa = alerta.get('peca_completa', peca_nome)
    
    print(f"  Tentando buscar peça...")
    print(f"  Verificando se 'óleo' está em '{peca_nome.lower()}': {'óleo' in peca_nome.lower()}")
    print(f"  Verificando se 'oleo' está em '{peca_nome.lower()}': {'oleo' in peca_nome.lower()}")
    
    try:
        # Simular a lógica da view
        peca = None
        if 'óleo' in peca_nome.lower() or 'oleo' in peca_nome.lower():
            print("    Buscando com prioridade na categoria motor...")
            peca = Peca.objects.filter(nome=peca_completa, categoria='motor').first()
        
        if not peca:
            print("    Buscando sem filtro de categoria...")
            peca = Peca.objects.filter(nome=peca_completa).first()
            
        if peca:
            print(f"    ✅ Encontrada: {peca.nome}")
            print(f"    Categoria: {peca.get_categoria_display()}")
        else:
            print(f"    ❌ Não encontrada")
    except Exception as e:
        print(f"    ❌ Erro na busca: {e}")