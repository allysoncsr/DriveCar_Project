import json
from django.core.management.base import BaseCommand
from drivecar.models import Marca, Modelo, Versao


class Command(BaseCommand):
    help = 'Importa biblioteca de veículos (Marcas, Modelos e Versões)'

    def handle(self, *args, **options):
        # Biblioteca de veículos
        vehicle_library = {
            "TOYOTA": {
                "Corolla": [
                    "Corolla GLi 2.0 Flex Automático",
                    "Corolla XEi 2.0 Flex Automático"
                ],
                "Corolla Cross": [
                    "Cross XRE 2.0 Flex Automático",
                    "Cross Hybrid 1.8 Automático"
                ],
                "Hilux": [
                    "Hilux SR 2.8 Diesel Automática 4x4",
                    "Hilux SRV 2.8 Diesel Automática 4x4"
                ],
                "Yaris": [
                    "Yaris XL 1.5 Flex",
                    "Yaris XLS 1.5 Flex"
                ],
                "Etios": [
                    "Etios X 1.3 Flex",
                    "Etios XS 1.5 Flex"
                ],
                "RAV4": [
                    "RAV4 2.5 Hybrid",
                    "RAV4 SX 2.5 Flex"
                ],
                "Prius": [
                    "Prius 1.8 Hybrid",
                    "Prius C (Aqua) Hybrid"
                ],
                "Camry": [
                    "Camry 2.5 Hybrid",
                    "Camry XLE"
                ],
                "Avanza / Rush (quando aplicável)": [
                    "Rush 1.5 Flex",
                    "Avanza 1.5"
                ],
                "Crown (importado/exótico)": [
                    "Crown Hybrid",
                    "Crown Sedan"
                ],
                "Sequoia (importado)": [
                    "Sequoia SR5",
                    "Sequoia Limited"
                ],
                "Fortuner (importado/por vezes nome Hilux SW4)": [
                    "Fortuner 2.7",
                    "Fortuner 2.8 Diesel 4x4"
                ],
                "SW4 (Hilux SW4)": [
                    "SW4 SRV 2.8 Diesel",
                    "SW4 SR 2.8 Diesel"
                ],
                "Yaris Cross": [
                    "Yaris Cross 1.5",
                    "Yaris Cross Hybrid"
                ],
                "Space Cruiser / Innova (quando disponível)": [
                    "Innova 2.0",
                    "Innova Crysta 2.7"
                ],
                "Land Cruiser Prado": [
                    "Prado TX 2.8 Diesel",
                    "Prado VX 2.8 Diesel"
                ],
                "Land Cruiser 300": [
                    "LC300 V6",
                    "LC300 TX"
                ],
                "Urban Cruiser / Rush (compact SUVs)": [
                    "Urban Cruiser 1.5",
                    "Urban Cruiser Hyryder"
                ],
                "Belta (modelos antigos)": [
                    "Belta 1.0",
                    "Belta 1.3"
                ],
                "Yaris Sedan (variações)": [
                    "Yaris Sedan XL",
                    "Yaris Sedan XLS"
                ]
            },
            "HONDA": {
                "Civic": [
                    "Civic Sport 2.0 Flex Automático",
                    "Civic Touring 1.5 Turbo"
                ],
                "City": [
                    "City LX 1.5",
                    "City EXL 1.5 CVT"
                ],
                "HR-V": [
                    "HR-V EX 1.5 Flex CVT",
                    "HR-V Advance 1.5 Turbo"
                ],
                "WR-V": [
                    "WR-V 1.5 Flex",
                    "WR-V EXL"
                ],
                "Fit / Jazz": [
                    "Fit LX 1.5",
                    "Fit EX 1.5 CVT"
                ],
                "Fit Shuttle / Freed (quando existente)": [
                    "Freed 1.5",
                    "Shuttle 1.5"
                ],
                "CR-V": [
                    "CR-V LX Turbo",
                    "CR-V EXL Hybrid"
                ],
                "Accord (modelos antigos/importados)": [
                    "Accord 2.0",
                    "Accord Hybrid"
                ],
                "Pilot (importado)": [
                    "Pilot EXL",
                    "Pilot Touring"
                ],
                "HR-V e:HEV (híbrido)": [
                    "HR-V e:HEV Touring",
                    "HR-V e:HEV EX"
                ],
                "Fit e:HEV (híbrido)": [
                    "Fit e:HEV",
                    "Fit Hybrid LX"
                ],
                "Amaze (mercados regionais)": [
                    "Amaze 1.2",
                    "Amaze CVT"
                ],
                "NSX (supercar)": [
                    "NSX Hybrid",
                    "NSX Type S"
                ],
                "Civic Type R (performance)": [
                    "Type R GT",
                    "Type R Limited"
                ],
                "Odyssey (quando disponível)": [
                    "Odyssey EX",
                    "Odyssey ELX"
                ],
                "S2000 (clássico)": [
                    "S2000 Roadster",
                    "S2000 Base"
                ],
                "Integra (novo/antigo)": [
                    "Integra GS",
                    "Integra Type S"
                ],
                "Legend (luxo/híbrido)": [
                    "Legend Hybrid",
                    "Legend Executive"
                ],
                "Beat / small cars (mercados)": [
                    "Beat 1.2",
                    "Beat DX"
                ],
                "Brio (quando disponível no Brasil/regionais)": [
                    "Brio 1.2",
                    "Brio VX"
                ]
            },
            "CHEVROLET": {
                "Onix": [
                    "Onix 1.0 LT",
                    "Onix 1.0 Premier"
                ],
                "Onix Plus (sedan)": [
                    "Onix Plus LT",
                    "Onix Plus Premier"
                ],
                "Prisma (nome antigo/Onix Plus em parte)": [
                    "Prisma 1.0",
                    "Prisma 1.4"
                ],
                "Tracker": [
                    "Tracker LT 1.0 Turbo",
                    "Tracker Premier 1.2 Turbo"
                ],
                "Spin": [
                    "Spin LT 1.8",
                    "Spin Activ"
                ],
                "Cruze (quando disponível/importado usado)": [
                    "Cruze LT 1.4 Turbo",
                    "Cruze Premier"
                ],
                "S10": [
                    "S10 LS 2.8 Diesel",
                    "S10 High Country 2.8 Diesel"
                ],
                "Trailblazer": [
                    "Trailblazer LTZ 2.8 Diesel",
                    "Trailblazer Premier"
                ],
                "Cobalt (modelos antigos)": [
                    "Cobalt LT 1.4",
                    "Cobalt Elite"
                ],
                "Classic (antigo)": [
                    "Classic 1.0",
                    "Classic 1.4"
                ],
                "Camaro (importado)": [
                    "Camaro LT",
                    "Camaro SS"
                ],
                "Corvette (importado)": [
                    "Corvette Stingray",
                    "Corvette Z06"
                ],
                "Blazer": [
                    "Blazer LT 2.0",
                    "Blazer Premier 3.6"
                ],
                "Colorado (mercados onde aplicável)": [
                    "Colorado LT",
                    "Colorado Z71"
                ],
                "Equinox (quando importado/vendido)": [
                    "Equinox 2.0 Turbo",
                    "Equinox Premier"
                ],
                "Niva (mercados específicos/antigo GM Russia)": [
                    "Niva 4x4",
                    "Niva GL"
                ],
                "Chevette (clássico)": [
                    "Chevette 1.6",
                    "Chevette SL"
                ],
                "Meriva (antigo)": [
                    "Meriva 1.8",
                    "Meriva Joy"
                ],
                "Aveo (antigo)": [
                    "Aveo LT",
                    "Aveo LS"
                ],
                "Astro / vans (mercados regionais)": [
                    "Astro Cargo",
                    "Astro Passenger"
                ]
            },
            "FIAT": {
                "Uno": [
                    "Uno Way 1.0",
                    "Uno Attractive 1.0"
                ],
                "Mobi": [
                    "Mobi Like 1.0",
                    "Mobi Way 1.0"
                ],
                "Argo": [
                    "Argo Drive 1.0",
                    "Argo Trekking 1.3"
                ],
                "Cronos": [
                    "Cronos Drive 1.3",
                    "Cronos Precision 1.8"
                ],
                "Toro": [
                    "Toro Endurance 1.8 Flex",
                    "Toro Volcano 2.0 Diesel 4x4"
                ],
                "Strada": [
                    "Strada Hard Working 1.4",
                    "Strada Volcano 1.3"
                ],
                "Palio (antigo)": [
                    "Palio Fire 1.0",
                    "Palio Weekend"
                ],
                "Punto (antigo/importado usado)": [
                    "Punto Attractive",
                    "Punto T-Jet"
                ],
                "Doblo": [
                    "Doblo Cargo",
                    "Doblo Adventure"
                ],
                "Ducato": [
                    "Ducato Cargo",
                    "Ducato Passenger"
                ],
                "Siena (antigo)": [
                    "Siena EL 1.4",
                    "Siena Attractive"
                ],
                "Bravo (antigo)": [
                    "Bravo T-Jet",
                    "Bravo Essence"
                ],
                "Idea (antigo)": [
                    "Idea Adventure",
                    "Idea ELX"
                ],
                "500 / 500X (importado)": [
                    "500 Cult",
                    "500X Trekking"
                ],
                "Fiorino (van pequeno)": [
                    "Fiorino Furgão",
                    "Fiorino Pickup"
                ],
                "Linea (antigo)": [
                    "Linea Essence",
                    "Linea T-Jet"
                ],
                "Multipla (antigo/impr.)": [
                    "Multipla 1.6",
                    "Multipla 1.8"
                ],
                "X1H (nome comercial regionais)": [
                    "X1H Base",
                    "X1H Adventure"
                ],
                "Freemont (importado/antigo)": [
                    "Freemont Drive",
                    "Freemont Precision"
                ]
            },
            "VOLKSWAGEN": {
                "Gol": [
                    "Gol 1.0 Flex",
                    "Gol 1.6 MSI"
                ],
                "Fox": [
                    "Fox 1.0",
                    "Fox Connect"
                ],
                "Polo": [
                    "Polo 1.0 MPI",
                    "Polo 1.0 TSI"
                ],
                "Virtus": [
                    "Virtus 1.6",
                    "Virtus 1.0 TSI"
                ],
                "T-Cross": [
                    "T-Cross 200 TSI",
                    "T-Cross Highline"
                ],
                "Nivus": [
                    "Nivus Comfortline 1.0 TSI",
                    "Nivus Highline 1.0 TSI"
                ],
                "Taos": [
                    "Taos Comfortline",
                    "Taos Highline"
                ],
                "Tiguan": [
                    "Tiguan Allspace",
                    "Tiguan R-Line"
                ],
                "Amarok": [
                    "Amarok Trendline 2.0",
                    "Amarok V6 3.0"
                ],
                "Saveiro": [
                    "Saveiro Robust 1.6",
                    "Saveiro Cross"
                ],
                "Up!": [
                    "Up! Take 1.0",
                    "Up! Cross"
                ],
                "Voyage (sedan derivado do Gol)": [
                    "Voyage 1.6",
                    "Voyage Trendline"
                ],
                "Passat (importado/usado)": [
                    "Passat Variant",
                    "Passat R-Line"
                ],
                "Jetta (quando disponível/importado)": [
                    "Jetta 1.4 TSI",
                    "Jetta GLI"
                ],
                "Caravelle / Kombi moderna (vans importadas)": [
                    "Caravelle Comfortline",
                    "Kombi Trend"
                ],
                "e-Golf / ID Family (elétricos)": [
                    "e-Golf",
                    "ID.4"
                ],
                "Fox Cross / CrossFox (antigos)": [
                    "CrossFox 1.6",
                    "CrossFox Adventure"
                ],
                "Gol Rallye (edições especiais)": [
                    "Gol Rallye 1.6",
                    "Gol GT"
                ],
                "EA288 / variantes (motorização/edições)": [
                    "1.4 TSI",
                    "2.0 TSI"
                ],
                "Lavida / Santana (mercados regionais)": [
                    "Lavida Comfort",
                    "Santana 1.4"
                ]
            },
            "HYUNDAI": {
                "HB20": [
                    "HB20 Sense 1.0",
                    "HB20 Platinum 1.0 Turbo"
                ],
                "HB20S (sedan)": [
                    "HB20S Vision 1.6",
                    "HB20S Platinum 1.0 Turbo"
                ],
                "Creta": [
                    "Creta Action 1.6",
                    "Creta Limited 1.0 Turbo"
                ],
                "Tucson": [
                    "Tucson GL 2.0",
                    "Tucson Limited 2.0 Turbo"
                ],
                "Santa Fe": [
                    "Santa Fe 2.4",
                    "Santa Fe Platinum"
                ],
                "Kona": [
                    "Kona 2.0",
                    "Kona Electric"
                ],
                "i30 (hatch)": [
                    "i30 2.0",
                    "i30 N (performance)"
                ],
                "ix35 (SUV antigo)": [
                    "ix35 2.0",
                    "ix35 GL"
                ],
                "Veloster (esportivo)": [
                    "Veloster 1.6 Turbo",
                    "Veloster N"
                ],
                "H-1 / Starex (vans)": [
                    "H-1 GLS",
                    "Starex Cargo"
                ],
                "Accent (antigo/importado usado)": [
                    "Accent 1.6",
                    "Accent GLS"
                ],
                "Ioniq (híbrido/elétrico)": [
                    "Ioniq Hybrid",
                    "Ioniq Electric"
                ],
                "Nexo (hidrogênio/exótico)": [
                    "Nexo FCEV",
                    "Nexo Limited"
                ],
                "Santa Cruz (pickup, mercados selecionados)": [
                    "Santa Cruz SE",
                    "Santa Cruz Limited"
                ],
                "Venue": [
                    "Venue Vision 1.6",
                    "Venue Limited"
                ],
                "Bayon (compact SUV)": [
                    "Bayon 1.0 T-GDi",
                    "Bayon Comfort"
                ],
                "Staria (van)": [
                    "Staria Touring",
                    "Staria Cargo"
                ],
                "Genesis (linha luxo da Hyundai)": [
                    "G70",
                    "G80"
                ],
                "H100 (comerciais/vans)": [
                    "H100 Cargo",
                    "H100 Passageiro"
                ],
                "Custo/edições (variações regionais)": [
                    "Versões básicas",
                    "Versões topo"
                ]
            },
            "NISSAN": {
                "Kicks": [
                    "Kicks Sense 1.6",
                    "Kicks Advance 1.6"
                ],
                "March (antigo)": [
                    "March 1.0",
                    "March 1.6"
                ],
                "Versa": [
                    "Versa Sense 1.6",
                    "Versa Exclusive 1.6"
                ],
                "Sentra": [
                    "Sentra 2.0",
                    "Sentra SR 2.0"
                ],
                "Frontier": [
                    "Frontier XE 2.3 Diesel",
                    "Frontier Platinum 2.3 Diesel"
                ],
                "Murano (importado usado)": [
                    "Murano SL",
                    "Murano Platinum"
                ],
                "X-Trail / Rogue (importado em alguns mercados)": [
                    "X-Trail 2.5",
                    "X-Trail SL"
                ],
                "Leaf (elétrico)": [
                    "Leaf S",
                    "Leaf SV"
                ],
                "Note / e-Note (regionais)": [
                    "Note 1.6",
                    "Note e-Power"
                ],
                "Juke": [
                    "Juke Texto",
                    "Juke Nismo"
                ],
                "GT-R (supercar)": [
                    "GT-R Nismo",
                    "GT-R Premium"
                ],
                "NV200 (van)": [
                    "NV200 Cargo",
                    "NV200 Passenger"
                ],
                "Almera (Mercados regionais)": [
                    "Almera 1.6",
                    "Almera Exclusive"
                ],
                "Pathfinder (importado)": [
                    "Pathfinder SV",
                    "Pathfinder Platinum"
                ],
                "Maxima (antigo/importado)": [
                    "Maxima SL",
                    "Maxima SE"
                ],
                "Armada / Patrol (importado)": [
                    "Armada SL",
                    "Armada Platinum"
                ],
                "Xterra (SUV antigo/importado usado)": [
                    "Xterra XE",
                    "Xterra SE"
                ],
                "Terrano (variantes históricas)": [
                    "Terrano 2.4",
                    "Terrano XE"
                ],
                "Qashqai (quando disponível/importado)": [
                    "Qashqai S",
                    "Qashqai SL"
                ],
                "Note e-Power / híbridos regionais": [
                    "e-Power Advance",
                    "e-Power Exclusive"
                ]
            },
            "FORD": {
                "Ka (antigo)": [
                    "Ka 1.0",
                    "Ka SE 1.5"
                ],
                "Ka Sedan / Ka+": [
                    "Ka+ SE",
                    "Ka+ SE 1.5"
                ],
                "Fiesta (antigo)": [
                    "Fiesta 1.6",
                    "Fiesta Sedan"
                ],
                "EcoSport (antigo)": [
                    "EcoSport SE 1.5",
                    "EcoSport Titanium 2.0"
                ],
                "Ranger": [
                    "Ranger XLS 2.2 Diesel",
                    "Ranger Limited 3.0 Diesel"
                ],
                "Fusion (sedan importado/antigo)": [
                    "Fusion Titanium Hybrid",
                    "Fusion SEL"
                ],
                "Mustang (importado/performance)": [
                    "Mustang GT",
                    "Mustang Mach 1"
                ],
                "Bronco Sport": [
                    "Bronco Sport Big Bend",
                    "Bronco Sport Badlands"
                ],
                "Edge (importado em alguns mercados)": [
                    "Edge SEL",
                    "Edge Titanium"
                ],
                "Focus (antigo/importado usado)": [
                    "Focus Hatch 2.0",
                    "Focus Sedan 2.0"
                ],
                "Transit (vans comerciais)": [
                    "Transit Cargo",
                    "Transit Minibus"
                ],
                "Ka Freestyle (edições / variantes)": [
                    "Ka Freestyle 1.5",
                    "Ka Active"
                ],
                "S-Max / Galaxy (importados/vans)": [
                    "S-Max Titanium",
                    "Galaxy Trend"
                ],
                "Explorer (SUV importado)": [
                    "Explorer XLT",
                    "Explorer Limited"
                ],
                "Courier (pickup pequena, mercados regionais)": [
                    "Courier 1.6",
                    "Courier 1.4"
                ],
                "Torino / Maverick (dependendo do mercado)": [
                    "Maverick Lariat",
                    "Maverick FX4"
                ],
                "Ka Trail (edições especiais)": [
                    "Ka Trail 1.0",
                    "Ka Trail 1.5"
                ],
                "F-150 / F-Series (importadas/performance)": [
                    "F-150 XL",
                    "F-150 Raptor"
                ],
                "Bronco (clássico/novo em mercados selecionados)": [
                    "Bronco Base",
                    "Bronco Sasquatch"
                ],
                "Territory (quando disponível/mercado China)": [
                    "Territory SEL",
                    "Territory Titanium"
                ]
            }
        }

        self.stdout.write('Iniciando importação da biblioteca de veículos...')
        
        marcas_criadas = 0
        modelos_criados = 0
        versoes_criadas = 0
        
        for marca_nome, modelos_dict in vehicle_library.items():
            # Criar ou obter marca
            marca, marca_created = Marca.objects.get_or_create(nome=marca_nome)
            if marca_created:
                marcas_criadas += 1
                self.stdout.write(f'✓ Marca criada: {marca_nome}')
            
            for modelo_nome, versoes_list in modelos_dict.items():
                # Criar ou obter modelo
                modelo, modelo_created = Modelo.objects.get_or_create(
                    nome=modelo_nome,
                    marca=marca
                )
                if modelo_created:
                    modelos_criados += 1
                    self.stdout.write(f'  ✓ Modelo criado: {modelo_nome}')
                
                for versao_nome in versoes_list:
                    # Criar ou obter versão
                    versao, versao_created = Versao.objects.get_or_create(
                        nome=versao_nome,
                        modelo=modelo
                    )
                    if versao_created:
                        versoes_criadas += 1
        
        # Relatório final
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('IMPORTAÇÃO CONCLUÍDA COM SUCESSO!'))
        self.stdout.write('='*60)
        self.stdout.write(f'📊 Marcas criadas: {marcas_criadas}')
        self.stdout.write(f'📊 Modelos criados: {modelos_criados}')
        self.stdout.write(f'📊 Versões criadas: {versoes_criadas}')
        self.stdout.write('\n✅ Sistema de cascata Marca → Modelo → Versão está pronto!')
        self.stdout.write('✅ Agora você pode usar os dropdowns cascatas no cadastro de veículos.')