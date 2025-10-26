#!/usr/bin/env python
"""
Teste das APIs do sistema de cascata de veículos
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drivecar_project.settings')
django.setup()

from drivecar.models import Marca, Modelo, Versao

def test_cascading_system():
    print("=== TESTE DO SISTEMA DE CASCATA ===\n")
    
    # Teste 1: Listar marcas
    print("1. Marcas disponíveis:")
    marcas = Marca.objects.filter(ativo=True)[:3]
    for marca in marcas:
        print(f"   ID: {marca.id} - {marca.nome}")
    
    if not marcas:
        print("   ❌ Nenhuma marca encontrada!")
        return
    
    # Teste 2: Listar modelos de uma marca
    primeira_marca = marcas[0]
    print(f"\n2. Modelos da {primeira_marca.nome}:")
    modelos = Modelo.objects.filter(marca=primeira_marca, ativo=True)[:3]
    for modelo in modelos:
        print(f"   ID: {modelo.id} - {modelo.nome}")
    
    if not modelos:
        print("   ❌ Nenhum modelo encontrado!")
        return
    
    # Teste 3: Listar versões de um modelo
    primeiro_modelo = modelos[0]
    print(f"\n3. Versões do {primeiro_modelo.nome}:")
    versoes = Versao.objects.filter(modelo=primeiro_modelo, ativo=True)[:3]
    for versao in versoes:
        motor_info = f" ({versao.motor})" if versao.motor else ""
        print(f"   ID: {versao.id} - {versao.nome}{motor_info}")
    
    if not versoes:
        print("   ❌ Nenhuma versão encontrada!")
        return
    
    print(f"\n✅ Sistema funcionando! Total: {marcas.count()} marcas, "
          f"{Modelo.objects.filter(ativo=True).count()} modelos, "
          f"{Versao.objects.filter(ativo=True).count()} versões")

if __name__ == "__main__":
    test_cascading_system()