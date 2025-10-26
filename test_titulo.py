#!/usr/bin/env python
"""
Teste rápido da propriedade titulo_limpo
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drivecar_project.settings')
django.setup()

from drivecar.models import Veiculo

print("🔍 TESTE DA PROPRIEDADE titulo_limpo:")
print("=" * 40)

for veiculo in Veiculo.objects.all():
    print(f"ID {veiculo.id}: '{veiculo.titulo_limpo}'")
    if veiculo.marca and veiculo.modelo:
        print(f"    Marca: {veiculo.marca.nome}")
        print(f"    Modelo: {veiculo.modelo.nome}")
    else:
        print(f"    Marca legado: {veiculo.marca_legado}")
        print(f"    Modelo legado: {veiculo.modelo_legado}")
    print()