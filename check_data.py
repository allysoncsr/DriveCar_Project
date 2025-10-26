#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drivecar_project.settings')
django.setup()

from drivecar.models import Marca, Modelo, Versao

print("=== VERIFICAÇÃO DOS DADOS PADRONIZADOS ===\n")

print("📊 RESUMO:")
print(f"   🏷️  Marcas: {Marca.objects.count()}")
print(f"   🚙 Modelos: {Modelo.objects.count()}")
print(f"   ⚙️  Versões: {Versao.objects.count()}\n")

print("🏷️  MARCAS PADRONIZADAS:")
for marca in Marca.objects.all().order_by('nome'):
    print(f"   ✅ {marca.nome} ({marca.modelo_set.count()} modelos)")

print("\n🚙 EXEMPLOS DE MODELOS PADRONIZADOS:")
for marca in Marca.objects.all()[:3]:  # Primeiras 3 marcas
    print(f"\n   📋 {marca.nome}:")
    for modelo in marca.modelo_set.all()[:3]:  # Primeiros 3 modelos
        print(f"      • {modelo.nome}")

print("\n⚙️  EXEMPLO DE VERSÕES (TOYOTA COROLLA):")
try:
    toyota = Marca.objects.get(nome='TOYOTA')
    corolla = toyota.modelo_set.filter(nome__icontains='Corolla').first()
    if corolla:
        for versao in corolla.versao_set.all()[:5]:  # Primeiras 5 versões
            print(f"      • {versao.nome}")
except:
    print("      Nenhuma versão encontrada")

print("\n✅ Verificação concluída!")