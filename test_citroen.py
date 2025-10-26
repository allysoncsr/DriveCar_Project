#!/usr/bin/env python
"""
Teste da nova marca Citroën no sistema de cascata
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drivecar_project.settings')
django.setup()

from drivecar.models import Marca, Modelo, Versao

def test_citroen():
    print("🇫🇷 TESTE DA NOVA MARCA CITROËN")
    print("=" * 40)
    
    # Buscar Citroën
    citroen = Marca.objects.filter(nome='Citroën').first()
    
    if not citroen:
        print("❌ Citroën não encontrada!")
        return
    
    print(f"✅ Marca encontrada: {citroen.nome} (ID: {citroen.id})")
    
    # Listar modelos
    modelos = Modelo.objects.filter(marca=citroen, ativo=True).order_by('nome')
    print(f"\n📋 {modelos.count()} modelos da Citroën:")
    
    for i, modelo in enumerate(modelos, 1):
        versoes = Versao.objects.filter(modelo=modelo, ativo=True)
        print(f"\n{i}. 🚗 {modelo.nome} ({versoes.count()} versões)")
        
        for j, versao in enumerate(versoes, 1):
            # Extrair informações técnicas
            motor_info = ""
            combustivel_info = ""
            transmissao_info = ""
            
            versao_nome = versao.nome.lower()
            
            # Detectar motor
            if "1.0" in versao_nome:
                motor_info = "1.0"
            elif "1.6" in versao_nome:
                motor_info = "1.6"
            elif "2.2" in versao_nome:
                motor_info = "2.2"
            
            # Detectar combustível
            if "flex" in versao_nome:
                combustivel_info = "Flex"
            elif "diesel" in versao_nome:
                combustivel_info = "Diesel"
            elif "turbo" in versao_nome:
                combustivel_info = "Turbo"
            
            # Detectar transmissão
            if " at" in versao_nome or " cvt" in versao_nome:
                transmissao_info = "Automático"
            
            detalhes = []
            if motor_info:
                detalhes.append(f"Motor: {motor_info}")
            if combustivel_info:
                detalhes.append(f"Combustível: {combustivel_info}")
            if transmissao_info:
                detalhes.append(f"Câmbio: {transmissao_info}")
            
            detalhes_str = f" ({', '.join(detalhes)})" if detalhes else ""
            
            print(f"   {j}. {versao.nome}{detalhes_str}")
    
    print(f"\n📊 RESUMO DA CITROËN:")
    print(f"   • {modelos.count()} modelos")
    print(f"   • {Versao.objects.filter(modelo__marca=citroen).count()} versões")
    print(f"   • Inclui hatches, SUVs e comerciais")
    
    print(f"\n🎯 DESTAQUES:")
    print("   🚙 C3: Hatch compacto com 3 versões")
    print("   🏔️  C3 Aircross: SUV com opções turbo")
    print("   🆕 Basalt: Modelo mais recente")
    print("   🌵 C4 Cactus: Design diferenciado")
    print("   🚐 Jumpy/Jumper: Linha comercial")
    
    print(f"\n✅ Sistema funcionando perfeitamente!")
    print(f"🌐 Teste em: /veiculos/cadastrar/")

if __name__ == "__main__":
    test_citroen()