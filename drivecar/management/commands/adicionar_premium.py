"""
Comando para adicionar VOLVO e LAND ROVER - Completando a biblioteca brasileira
"""
from django.core.management.base import BaseCommand
from drivecar.models import Marca, Modelo, Versao
from django.db import transaction


def adicionar_marcas_premium():
    """
    Adiciona VOLVO e LAND ROVER com seus modelos e versões disponíveis no Brasil
    """
    
    # Biblioteca das marcas premium faltantes
    marcas_premium = {
        'VOLVO': {
            'XC40': [
                'XC40 Momentum 2.0 Turbo',
                'XC40 R-Design 2.0 Turbo',
                'XC40 Inscription 2.0 Turbo',
                'XC40 Recharge Pure Electric'
            ],
            'XC60': [
                'XC60 Momentum 2.0 Turbo',
                'XC60 R-Design 2.0 Turbo',
                'XC60 Inscription 2.0 Turbo',
                'XC60 T8 Hybrid AWD'
            ],
            'XC90': [
                'XC90 Momentum 2.0 Turbo',
                'XC90 R-Design 2.0 Turbo',
                'XC90 Inscription 2.0 Turbo',
                'XC90 T8 Hybrid Excellence'
            ],
            'S60': [
                'S60 Momentum 2.0 Turbo',
                'S60 R-Design 2.0 Turbo',
                'S60 Inscription 2.0 Turbo'
            ],
            'V60': [
                'V60 Momentum 2.0 Turbo',
                'V60 R-Design 2.0 Turbo',
                'V60 Cross Country AWD'
            ],
            'C40': [
                'C40 Recharge Pure Electric',
                'C40 Recharge Plus'
            ],
            'EX30': [
                'EX30 Core 51 kWh',
                'EX30 Plus 69 kWh',
                'EX30 Ultra 69 kWh'
            ]
        },
        
        'LAND ROVER': {
            'Range Rover Evoque': [
                'Evoque S 2.0 Turbo',
                'Evoque SE 2.0 Turbo',
                'Evoque HSE 2.0 Turbo',
                'Evoque Autobiography 2.0 Turbo'
            ],
            'Range Rover Velar': [
                'Velar S 2.0 Turbo',
                'Velar SE 2.0 Turbo',
                'Velar HSE 3.0 V6',
                'Velar R-Dynamic 3.0 V6'
            ],
            'Range Rover Sport': [
                'Sport S 3.0 V6',
                'Sport SE 3.0 V6',
                'Sport HSE 3.0 V6',
                'Sport Autobiography 5.0 V8'
            ],
            'Range Rover': [
                'Range Rover Vogue 3.0 V6',
                'Range Rover HSE 3.0 V6',
                'Range Rover Autobiography 5.0 V8',
                'Range Rover SV 5.0 V8'
            ],
            'Discovery': [
                'Discovery S 2.0 Turbo',
                'Discovery SE 2.0 Turbo',
                'Discovery HSE 3.0 V6'
            ],
            'Discovery Sport': [
                'Discovery Sport S 2.0 Turbo',
                'Discovery Sport SE 2.0 Turbo',
                'Discovery Sport HSE 2.0 Turbo'
            ],
            'Defender': [
                'Defender 90 2.0 Turbo',
                'Defender 110 2.0 Turbo',
                'Defender 130 3.0 V6',
                'Defender X 5.0 V8'
            ]
        }
    }
    
    print("=== ADICIONANDO MARCAS PREMIUM FINAIS ===\n")
    
    total_marcas_novas = 0
    total_modelos_novos = 0
    total_versoes_novas = 0
    
    with transaction.atomic():
        for marca_nome, modelos in marcas_premium.items():
            # Criar ou obter marca
            marca_obj, marca_criada = Marca.objects.get_or_create(
                nome=marca_nome,
                defaults={'ativo': True}
            )
            
            if marca_criada:
                total_marcas_novas += 1
                print(f"✅ Nova marca premium: {marca_nome}")
            else:
                print(f"🔄 Completando marca existente: {marca_nome}")
            
            for modelo_nome, versoes in modelos.items():
                # Criar ou obter modelo
                modelo_obj, modelo_criado = Modelo.objects.get_or_create(
                    marca=marca_obj,
                    nome=modelo_nome,
                    defaults={'ativo': True}
                )
                
                if modelo_criado:
                    total_modelos_novos += 1
                    print(f"   📋 Novo modelo: {modelo_nome}")
                
                for versao_nome in versoes:
                    # Criar versão se não existir
                    versao_obj, versao_criada = Versao.objects.get_or_create(
                        modelo=modelo_obj,
                        nome=versao_nome,
                        defaults={'ativo': True}
                    )
                    
                    if versao_criada:
                        total_versoes_novas += 1
    
    print(f"\n📊 MARCAS PREMIUM ADICIONADAS:")
    print(f"   🏷️  Marcas novas: {total_marcas_novas}")
    print(f"   🚙 Modelos novos: {total_modelos_novos}")
    print(f"   ⚙️  Versões novas: {total_versoes_novas}")
    
    # Estatísticas finais completas
    print(f"\n🎯 BIBLIOTECA BRASILEIRA COMPLETA:")
    print(f"   🏷️  Total de marcas: {Marca.objects.count()}")
    print(f"   🚙 Total de modelos: {Modelo.objects.count()}")
    print(f"   ⚙️  Total de versões: {Versao.objects.count()}")
    
    # Mostrar detalhes das novas marcas
    print(f"\n🔍 DETALHES DAS MARCAS PREMIUM:")
    for marca_nome in marcas_premium.keys():
        marca = Marca.objects.get(nome=marca_nome)
        modelos = marca.modelo_set.all()
        total_versoes = sum(modelo.versao_set.count() for modelo in modelos)
        print(f"   📋 {marca_nome}: {modelos.count()} modelos, {total_versoes} versões")
        
        for modelo in modelos:
            versoes_count = modelo.versao_set.count()
            print(f"      • {modelo.nome} ({versoes_count} versões)")
    
    return True


class Command(BaseCommand):
    help = 'Adiciona VOLVO e LAND ROVER - Completando a biblioteca brasileira'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Adicionando marcas premium finais (VOLVO e LAND ROVER)...')
        )
        
        resultado = adicionar_marcas_premium()
        
        if resultado:
            self.stdout.write(
                self.style.SUCCESS('🎉 Biblioteca brasileira 100% COMPLETA!')
            )
            self.stdout.write(
                self.style.SUCCESS('✅ Todas as principais marcas do Brasil incluídas!')
            )
        else:
            self.stdout.write(
                self.style.ERROR('❌ Erro ao adicionar marcas premium!')
            )