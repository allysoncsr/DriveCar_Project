#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drivecar_project.settings')
django.setup()

from drivecar.models import Peca

print("Testando busca por categoria motor:")
peca = Peca.objects.filter(nome='Óleo do motor', categoria='motor').first()
if peca:
    print(f"✅ Encontrada: {peca.nome} - {peca.get_categoria_display()}")
else:
    print("❌ Não encontrada")

print("\nTodas as peças com 'Óleo do motor':")
pecas = Peca.objects.filter(nome='Óleo do motor')
for i, p in enumerate(pecas):
    print(f"{i+1}. {p.nome} - {p.categoria} - {p.get_categoria_display()}")

print("\nTeste da lógica da view:")
peca_completa = 'Óleo do motor'
peca_nome = 'Óleo'

# Simular a lógica da view
peca = None
if 'óleo' in peca_nome.lower() or 'oleo' in peca_nome.lower():
    peca = Peca.objects.filter(nome=peca_completa, categoria='motor').first()
    print(f"Busca priorizada por motor: {peca.nome if peca else 'Nenhuma'} - {peca.get_categoria_display() if peca else 'N/A'}")

if not peca:
    peca = Peca.objects.filter(nome=peca_completa).first()
    print(f"Busca geral: {peca.nome if peca else 'Nenhuma'} - {peca.get_categoria_display() if peca else 'N/A'}")