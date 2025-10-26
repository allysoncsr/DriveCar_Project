#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drivecar_project.settings')
django.setup()

from drivecar.models import Marca, Modelo, Versao

print("=== ANÁLISE DETALHADA DA BIBLIOTECA ATUAL ===\n")

print("📊 RESUMO GERAL:")
print(f"   🏷️  Marcas: {Marca.objects.count()}")
print(f"   🚙 Modelos: {Modelo.objects.count()}")
print(f"   ⚙️  Versões: {Versao.objects.count()}")

print("\n🔍 ANÁLISE POR MARCA:")
for marca in Marca.objects.all().order_by('nome'):
    modelos = marca.modelo_set.all()
    total_versoes = sum(modelo.versao_set.count() for modelo in modelos)
    
    print(f"\n📋 {marca.nome}:")
    print(f"   Modelos: {modelos.count()}")
    print(f"   Versões: {total_versoes}")
    
    # Mostrar modelos sem versões
    modelos_sem_versoes = [m for m in modelos if m.versao_set.count() == 0]
    if modelos_sem_versoes:
        print(f"   ⚠️  Modelos sem versões: {[m.nome for m in modelos_sem_versoes]}")
    
    # Mostrar alguns modelos e suas versões
    for modelo in modelos[:3]:  # Primeiros 3 modelos
        versoes_count = modelo.versao_set.count()
        print(f"      • {modelo.nome} ({versoes_count} versões)")
        if versoes_count > 0:
            for versao in modelo.versao_set.all()[:2]:  # Primeiras 2 versões
                print(f"        - {versao.nome}")

print("\n🚗 ANÁLISE ESPECÍFICA - CITROËN:")
citroen = Marca.objects.filter(nome='CITROËN').first()
if citroen:
    c3_modelos = citroen.modelo_set.filter(nome__icontains='C3')
    print(f"   Modelos C3 encontrados: {c3_modelos.count()}")
    
    for modelo in c3_modelos:
        print(f"   📋 {modelo.nome}:")
        versoes = modelo.versao_set.all()
        if versoes.exists():
            for versao in versoes:
                print(f"      • {versao.nome}")
        else:
            print(f"      ⚠️  Nenhuma versão cadastrada")

print("\n📈 IDENTIFICAÇÃO DE LACUNAS:")
print("   🔴 Marcas ausentes importantes no Brasil:")
marcas_brasileiras = [
    "BYD", "HAVAL", "GWM", "JAC", "CAOA CHERY", "RENAULT", 
    "PEUGEOT", "JEEP", "RAM", "MITSUBISHI", "SUZUKI", "SUBARU",
    "VOLVO", "BMW", "MERCEDES-BENZ", "AUDI", "LAND ROVER"
]

marcas_existentes = set(m.nome for m in Marca.objects.all())
marcas_faltantes = [m for m in marcas_brasileiras if m not in marcas_existentes]

for marca in marcas_faltantes[:10]:  # Primeiras 10
    print(f"      • {marca}")

if len(marcas_faltantes) > 10:
    print(f"      ... e mais {len(marcas_faltantes) - 10} marcas")

print(f"\n✅ Análise concluída! Identificadas {len(marcas_faltantes)} marcas faltantes.")