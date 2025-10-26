"""
Biblioteca Expandida de Veículos Brasileiros 2025
Incluindo marcas elétricas, híbridas e completando versões faltantes
"""
from django.core.management.base import BaseCommand
from drivecar.models import Marca, Modelo, Versao
from django.db import transaction

def importar_biblioteca_expandida():
    """
    Importa biblioteca completa com foco no mercado brasileiro 2025
    Inclui: elétricos, híbridos, e versões completas
    """
    
    # Biblioteca expandida com marcas do mercado brasileiro
    biblioteca_expandida = {
        
        # === MARCAS ELETRICAS E HIBRIDAS (NOVAS) ===
        'BYD': {
            'Dolphin': [
                'Dolphin Dynamic 44,9 kWh', 
                'Dolphin Comfort 44,9 kWh', 
                'Dolphin Premium 60,48 kWh'
            ],
            'Yuan Plus': [
                'Yuan Plus Blade 60,48 kWh',
                'Yuan Plus GL-i 50,12 kWh'
            ],
            'Tan': [
                'Tan EV 108,8 kWh',
                'Tan DM-i Hybrid 2.0'
            ],
            'Song Plus': [
                'Song Plus Champion Edition DM-i',
                'Song Plus EV 71,7 kWh'
            ],
            'Seal': [
                'Seal Performance AWD 82,56 kWh',
                'Seal GT 85,44 kWh'
            ]
        },
        
        'HAVAL': {
            'H6': [
                'H6 Supreme 2.0 Turbo AWD',
                'H6 Ultra Luxury 2.0 Turbo',
                'H6 Elite 1.5 Turbo'
            ],
            'Jolion': [
                'Jolion Premium 1.5' 
            ]
        },
        
        'GWM': {
            'Ora 03': [
                'Ora 03 GT 48 kWh',
                'Ora 03 Skin 48 kWh'
            ],
            'Poer': [
                'Poer 4WD 2.0 Turbo Diesel',
                'Poer Hybrid 2.0 Turbo'
            ]
        },
        
        'JAC': {
            'iEV40': [
                'iEV40 Pro 55 kWh',
                'iEV40 Plus 50,4 kWh'
            ],
            'E-JS1': [
                'E-JS1 Premium EV'
            ],
            'T40': [
                'T40 1.5 16V Flex',
                'T40 Plus 1.6 CVT'
            ],
            'T50': [
                'T50 Comfort 1.5',
                'T50 Luxury 1.6 CVT'
            ]
        },
        
        'CAOA CHERY': {
            'iCar': [
                'iCar 1 EV 30,6 kWh',
                'iCar 2 EV 37,9 kWh'
            ],
            'Tiggo 2': [
                'Tiggo 2 Look 1.5',
                'Tiggo 2 Act 1.5 CVT'
            ],
            'Tiggo 3x': [
                'Tiggo 3x Plus 1.5',
                'Tiggo 3x Pro 1.5 CVT'
            ],
            'Tiggo 5x': [
                'Tiggo 5x Pro 1.5 Turbo',
                'Tiggo 5x TXS 1.5 Turbo CVT'
            ],
            'Tiggo 7': [
                'Tiggo 7 Pro 1.5 Turbo',
                'Tiggo 7 Sport 1.6 Turbo AWD'
            ],
            'Tiggo 8': [
                'Tiggo 8 Pro Max 2.0 Turbo',
                'Tiggo 8 Plus Hybrid 1.5 DHT'
            ],
            'Arrizo 5': [
                'Arrizo 5 Comfort 1.5',
                'Arrizo 5 RX 1.5 CVT'
            ]
        },
        
        # === MARCAS EUROPEIAS FALTANTES ===
        'RENAULT': {
            'Kwid': [
                'Kwid Zen 1.0',
                'Kwid Intense 1.0 CVT',
                'Kwid Outsider 1.0'
            ],
            'Sandero': [
                'Sandero Life 1.0',
                'Sandero Zen 1.6',
                'Sandero Intense 1.6 CVT'
            ],
            'Logan': [
                'Logan Life 1.0',
                'Logan Zen 1.6',
                'Logan Intense 1.6 CVT'
            ],
            'Stepway': [
                'Stepway Zen 1.6',
                'Stepway Intense 1.6 CVT'
            ],
            'Duster': [
                'Duster Life 1.6',
                'Duster Zen 1.6 4x2',
                'Duster Intense 1.6 4x4 CVT'
            ],
            'Captur': [
                'Captur Life 1.6',
                'Captur Zen 1.6 CVT',
                'Captur Intense 1.3 Turbo CVT'
            ],
            'Oroch': [
                'Oroch Life 1.6',
                'Oroch Zen 1.6',
                'Oroch Intense 2.0 4x4'
            ]
        },
        
        'PEUGEOT': {
            '208': [
                '208 Active 1.6',
                '208 Allure 1.6 AT',
                '208 GT Line 1.6 Turbo'
            ],
            '2008': [
                '2008 Active 1.6',
                '2008 Allure 1.6 AT',
                '2008 GT Line 1.6 Turbo AT'
            ],
            '3008': [
                '3008 Allure 1.6 Turbo',
                '3008 GT Line 1.6 Turbo',
                '3008 Hybrid4 300 AWD'
            ],
            '5008': [
                '5008 Allure 1.6 Turbo',
                '5008 GT Line 1.6 Turbo'
            ]
        },
        
        # === MARCAS AMERICANAS FALTANTES ===
        'JEEP': {
            'Renegade': [
                'Renegade Sport 1.8 Flex',
                'Renegade Longitude 1.8 AT',
                'Renegade Limited 1.3 Turbo AT',
                'Renegade Trailhawk 2.0 Turbo Diesel 4x4'
            ],
            'Compass': [
                'Compass Sport 1.3 Turbo',
                'Compass Longitude 1.3 Turbo AT',
                'Compass Limited 1.3 Turbo AT',
                'Compass Trailhawk 2.0 Turbo Diesel 4x4'
            ],
            'Commander': [
                'Commander Sport 1.3 Turbo',
                'Commander Longitude 1.3 Turbo AT',
                'Commander Limited 2.0 Turbo AT',
                'Commander Overland 2.0 Turbo AT'
            ],
            'Grand Cherokee': [
                'Grand Cherokee Laredo 3.6 V6',
                'Grand Cherokee Limited 3.6 V6',
                'Grand Cherokee Summit 5.7 V8'
            ],
            'Wrangler': [
                'Wrangler Sport 2.0 Turbo',
                'Wrangler Sahara 2.0 Turbo AT',
                'Wrangler Rubicon 2.0 Turbo 4x4'
            ]
        },
        
        'RAM': {
            '1500': [
                'RAM 1500 Express 3.6 V6',
                'RAM 1500 Big Horn 5.7 V8',
                'RAM 1500 Laramie 5.7 V8',
                'RAM 1500 Limited 5.7 V8'
            ],
            '2500': [
                'RAM 2500 Tradesman 6.4 V8',
                'RAM 2500 Big Horn 6.7 Turbo Diesel'
            ]
        },
        
        # === MARCAS JAPONESAS FALTANTES ===
        'MITSUBISHI': {
            'Mirage': [
                'Mirage GL 1.2',
                'Mirage GLX 1.2 CVT'
            ],
            'Eclipse Cross': [
                'Eclipse Cross HPE 1.5 Turbo',
                'Eclipse Cross HPE-S 1.5 Turbo CVT'
            ],
            'Outlander': [
                'Outlander HPE 2.0',
                'Outlander HPE-S 2.4 AWD',
                'Outlander PHEV 2.4 Hybrid AWD'
            ],
            'Pajero': [
                'Pajero TR4 2.0 Flex',
                'Pajero Sport HPE 2.4 Diesel 4x4'
            ],
            'L200': [
                'L200 Triton GL 2.4 Diesel',
                'L200 Triton GLX 2.4 Diesel 4x4',
                'L200 Triton HPE 2.4 Diesel 4x4'
            ]
        },
        
        'SUZUKI': {
            'Jimny': [
                'Jimny 1.5 4x4 MT',
                'Jimny Sierra 1.5 4x4 AT'
            ],
            'Vitara': [
                'Vitara 4You 1.6',
                'Vitara 4Sport 1.4 Turbo AWD'
            ]
        },
        
        'SUBARU': {
            'Impreza': [
                'Impreza 2.0 AWD',
                'Impreza Sedan 2.0 AWD CVT'
            ],
            'XV': [
                'XV 2.0 AWD',
                'XV Premium 2.0 AWD CVT'
            ],
            'Forester': [
                'Forester 2.5 AWD',
                'Forester XT 2.0 Turbo AWD'
            ],
            'Legacy': [
                'Legacy 2.5 AWD CVT'
            ],
            'Outback': [
                'Outback 2.5 AWD CVT',
                'Outback XT 2.4 Turbo AWD'
            ]
        },
        
        # === MARCAS PREMIUM FALTANTES ===
        'BMW': {
            'Série 1': [
                '118i Sport 1.5 Turbo',
                '120i M Sport 2.0 Turbo'
            ],
            'Série 2': [
                '220i Coupé 2.0 Turbo',
                'M240i xDrive 3.0 Turbo'
            ],
            'Série 3': [
                '320i Sport 2.0 Turbo',
                '330i M Sport 2.0 Turbo',
                'M3 Competition 3.0 Bi-Turbo'
            ],
            'Série 5': [
                '530i Luxury 2.0 Turbo',
                'M550i xDrive 4.4 V8 Turbo'
            ],
            'X1': [
                'X1 sDrive20i 2.0 Turbo',
                'X1 xDrive25i 2.0 Turbo AWD'
            ],
            'X3': [
                'X3 xDrive30i 2.0 Turbo',
                'X3 M40i 3.0 Turbo'
            ],
            'X5': [
                'X5 xDrive40i 3.0 Turbo',
                'X5 M50i 4.4 V8 Turbo'
            ],
            'iX3': [
                'iX3 Impressive 80 kWh',
                'iX3 M Sport 80 kWh'
            ]
        },
        
        'MERCEDES-BENZ': {
            'Classe A': [
                'A200 Sedan 1.3 Turbo',
                'A250 Sport 2.0 Turbo'
            ],
            'Classe C': [
                'C180 Exclusive 1.6 Turbo',
                'C200 EQ Boost 1.5 Turbo Híbrido',
                'C300 AMG Line 2.0 Turbo'
            ],
            'Classe E': [
                'E200 Exclusive 2.0 Turbo',
                'E300 AMG Line 2.0 Turbo'
            ],
            'GLA': [
                'GLA200 Style 1.3 Turbo',
                'GLA250 AMG Line 2.0 Turbo'
            ],
            'GLC': [
                'GLC250 Exclusive 2.0 Turbo',
                'GLC300 AMG Line 2.0 Turbo'
            ],
            'EQA': [
                'EQA250 AMG Line 66,5 kWh',
                'EQA350 4MATIC 66,5 kWh'
            ]
        },
        
        'AUDI': {
            'A3': [
                'A3 Sedan Prestige 1.4 Turbo',
                'A3 Sportback Performance 2.0 Turbo'
            ],
            'A4': [
                'A4 Prestige Plus 2.0 Turbo',
                'A4 Performance Black 2.0 Turbo'
            ],
            'Q3': [
                'Q3 Prestige 1.4 Turbo',
                'Q3 Performance Black 2.0 Turbo'
            ],
            'Q5': [
                'Q5 Prestige Plus 2.0 Turbo',
                'Q5 Performance Black 3.0 V6'
            ],
            'e-tron': [
                'e-tron 55 Prestige 95 kWh',
                'e-tron GT RS 93,4 kWh'
            ]
        },
        
        # === COMPLETAR VERSÕES CITROËN ===
        'CITROËN_EXTRA': {  # Versões adicionais para Citroën
            'C3': [
                'C3 Feel Pack 1.0 Flex',  # VERSÃO SOLICITADA
                'C3 Shine Pack 1.0 Turbo',
                'C3 Origins 1.0 Pack',
                'C3 You! 1.0 Flex'
            ],
            'C4 Cactus': [
                'C4 Cactus Feel 1.6 Flex',
                'C4 Cactus Shine 1.6 AT',
                'C4 Cactus Rip Curl 1.6 AT'
            ],
            'Berlingo': [
                'Berlingo Feel 1.6',
                'Berlingo Live 1.6 HDi Diesel'
            ]
        }
    }
    
    print("=== IMPORTAÇÃO DA BIBLIOTECA EXPANDIDA ===\n")
    
    total_marcas_novas = 0
    total_modelos_novos = 0
    total_versoes_novas = 0
    
    with transaction.atomic():
        for marca_nome, modelos in biblioteca_expandida.items():
            
            # Tratamento especial para versões extras da Citroën
            if marca_nome == 'CITROËN_EXTRA':
                marca_obj = Marca.objects.get(nome='CITROËN')
                print(f"🔄 Completando versões da CITROËN...")
            else:
                # Criar ou obter marca
                marca_obj, marca_criada = Marca.objects.get_or_create(
                    nome=marca_nome,
                    defaults={'ativo': True}
                )
                
                if marca_criada:
                    total_marcas_novas += 1
                    print(f"✅ Nova marca: {marca_nome}")
            
            for modelo_nome, versoes in modelos.items():
                # Criar ou obter modelo
                modelo_obj, modelo_criado = Modelo.objects.get_or_create(
                    marca=marca_obj,
                    nome=modelo_nome,
                    defaults={'ativo': True}
                )
                
                if modelo_criado:
                    total_modelos_novos += 1
                
                for versao_nome in versoes:
                    # Criar versão se não existir
                    versao_obj, versao_criada = Versao.objects.get_or_create(
                        modelo=modelo_obj,
                        nome=versao_nome,
                        defaults={'ativo': True}
                    )
                    
                    if versao_criada:
                        total_versoes_novas += 1
    
    print(f"\n📊 IMPORTAÇÃO CONCLUÍDA:")
    print(f"   🏷️  Marcas novas: {total_marcas_novas}")
    print(f"   🚙 Modelos novos: {total_modelos_novos}")
    print(f"   ⚙️  Versões novas: {total_versoes_novas}")
    
    # Estatísticas finais
    print(f"\n📈 TOTAIS ATUAIS:")
    print(f"   🏷️  Total de marcas: {Marca.objects.count()}")
    print(f"   🚙 Total de modelos: {Modelo.objects.count()}")
    print(f"   ⚙️  Total de versões: {Versao.objects.count()}")
    
    return True


class Command(BaseCommand):
    help = 'Expande a biblioteca de veículos com marcas brasileiras, incluindo elétricos e híbridos'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Iniciando expansão da biblioteca de veículos...')
        )
        
        resultado = importar_biblioteca_expandida()
        
        if resultado:
            self.stdout.write(
                self.style.SUCCESS('✅ Biblioteca expandida com sucesso!')
            )
        else:
            self.stdout.write(
                self.style.ERROR('❌ Erro na expansão da biblioteca!')
            )