import json
from django.core.management.base import BaseCommand
from drivecar.models import Marca, Modelo, Versao


class Command(BaseCommand):
    help = 'Adiciona Citroën à biblioteca de veículos'

    def handle(self, *args, **options):
        # Dados da Citroën
        citroen_data = {
            "Citroën": {
                "C3": [
                    "C3 Live 1.0 Flex",
                    "C3 Feel 1.6 Flex",
                    "C3 First Edition 1.6 AT"
                ],
                "C3 Aircross": [
                    "C3 Aircross Feel 1.0 Turbo",
                    "C3 Aircross Shine 1.0 Turbo CVT"
                ],
                "Basalt": [
                    "Basalt Turbo 200 1.0",
                    "Basalt Turbo 200 CVT"
                ],
                "C4 Cactus": [
                    "C4 Cactus Live 1.6 Flex",
                    "C4 Cactus Shine 1.6 Flex AT",
                    "C4 Cactus Shine Pack 1.6 AT"
                ],
                "Jumpy": [
                    "Jumpy Furgão Business 1.6 Diesel",
                    "Jumpy Furgão Pack 1.6 Diesel"
                ],
                "Jumper": [
                    "Jumper Furgão 2.2 Diesel",
                    "Jumper Minibus 2.2 Diesel"
                ]
            }
        }

        self.stdout.write('🚗 Adicionando Citroën à biblioteca de veículos...')
        
        marcas_criadas = 0
        modelos_criados = 0
        versoes_criadas = 0
        
        for marca_nome, modelos_dict in citroen_data.items():
            # Verificar se a marca já existe
            marca, marca_created = Marca.objects.get_or_create(nome=marca_nome)
            if marca_created:
                marcas_criadas += 1
                self.stdout.write(f'✅ Nova marca criada: {marca_nome}')
            else:
                self.stdout.write(f'ℹ️  Marca já existe: {marca_nome}')
            
            for modelo_nome, versoes_list in modelos_dict.items():
                # Verificar se o modelo já existe
                modelo, modelo_created = Modelo.objects.get_or_create(
                    nome=modelo_nome,
                    marca=marca
                )
                if modelo_created:
                    modelos_criados += 1
                    self.stdout.write(f'  ✅ Novo modelo: {modelo_nome}')
                else:
                    self.stdout.write(f'  ℹ️  Modelo já existe: {modelo_nome}')
                
                for versao_nome in versoes_list:
                    # Verificar se a versão já existe
                    versao, versao_created = Versao.objects.get_or_create(
                        nome=versao_nome,
                        modelo=modelo
                    )
                    if versao_created:
                        versoes_criadas += 1
                        self.stdout.write(f'    ✅ Nova versão: {versao_nome}')
                    else:
                        self.stdout.write(f'    ℹ️  Versão já existe: {versao_nome}')
        
        # Relatório final
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('🎉 CITROËN ADICIONADA COM SUCESSO!'))
        self.stdout.write('='*60)
        self.stdout.write(f'📊 Marcas criadas: {marcas_criadas}')
        self.stdout.write(f'📊 Modelos criados: {modelos_criados}')
        self.stdout.write(f'📊 Versões criadas: {versoes_criadas}')
        
        # Estatísticas gerais atualizadas
        total_marcas = Marca.objects.filter(ativo=True).count()
        total_modelos = Modelo.objects.filter(ativo=True).count()
        total_versoes = Versao.objects.filter(ativo=True).count()
        
        self.stdout.write(f'\n📈 ESTATÍSTICAS ATUALIZADAS:')
        self.stdout.write(f'   🏷️  Total de marcas: {total_marcas}')
        self.stdout.write(f'   🚙 Total de modelos: {total_modelos}')
        self.stdout.write(f'   ⚙️  Total de versões: {total_versoes}')
        
        self.stdout.write('\n✅ Sistema de cascata atualizado com Citroën!')
        self.stdout.write('🌐 Teste em: http://127.0.0.1:8000/veiculos/cadastrar/')