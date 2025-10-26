#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drivecar_project.settings')
django.setup()

from drivecar.models import *
from django.contrib.auth.models import User
from datetime import datetime, date

# Buscar usuário admin
try:
    u = User.objects.get(username='admin')
    print(f"Usuário encontrado: {u.username}")
    
    # Buscar veículo
    v = u.veiculo_set.first()
    if v:
        print(f"Veículo: {v.modelo}, KM atual: {v.km_atual}")
        
        # Verificar registros
        registros = RegistroManutencao.objects.filter(veiculo=v)
        print(f"Registros de manutenção: {registros.count()}")
        
        for r in registros[:5]:
            print(f"- {r.peca_servico}: KM {r.km_atual}, Data: {r.data_servico}")
        
        # Verificar alertas
        alertas = v.get_alertas_ativos()
        print(f"\nAlertas ativos: {len(alertas)}")
        
        for alerta in alertas:
            print(f"- {alerta['item']}: {alerta['descricao']} ({alerta['tipo']})")
            
            # Verificar se a peça existe
            try:
                peca = Peca.objects.get(nome=alerta['item'])
                print(f"  Categoria: {peca.get_categoria_display()}")
            except Peca.DoesNotExist:
                print(f"  ERRO: Peça '{alerta['item']}' não encontrada!")
                
        # Criar um registro antigo para gerar alerta se não houver
        if len(alertas) == 0:
            print("\nCriando registro antigo para gerar alerta...")
            data_antiga = date(2020, 1, 1)
            km_antigo = max(0, v.km_atual - 20000)
            
            # Buscar a peça Óleo do motor
            try:
                peca_oleo = Peca.objects.get(nome='Óleo do motor')
                r = RegistroManutencao.objects.create(
                    veiculo=v,
                    peca=peca_oleo,
                    data=data_antiga,
                    km=km_antigo,
                    preco=80.00
                )
            except Peca.DoesNotExist:
                print("Peça 'Óleo do motor' não encontrada")
            print(f"Registro criado: {r}")
            
            # Verificar alertas novamente
            alertas = v.get_alertas_ativos()
            print(f"Alertas após criação: {len(alertas)}")
            for alerta in alertas:
                print(f"- {alerta['item']}: {alerta['descricao']}")
                
    else:
        print("Nenhum veículo encontrado")
        
except User.DoesNotExist:
    print("Usuário admin não encontrado")