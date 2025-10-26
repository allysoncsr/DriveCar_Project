from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from drivecar.models import Veiculo, Peca, RegistroManutencao, Marca, Modelo, Versao
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Testa o novo sistema inteligente de alertas com cálculos por KM e tempo'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔧 TESTANDO NOVO SISTEMA INTELIGENTE DE ALERTAS'))
        self.stdout.write('=' * 70)
        
        # Usar dados existentes do usuário atual
        self.stdout.write('\n📊 ANALISANDO VEÍCULOS EXISTENTES...')
        
        usuarios = User.objects.all()
        for usuario in usuarios:
            veiculos = Veiculo.objects.filter(usuario=usuario)
            if veiculos.exists():
                self.stdout.write(f'\n👤 USUÁRIO: {usuario.username}')
                self.stdout.write('-' * 50)
                
                for veiculo in veiculos:
                    self.stdout.write(f'\n🚗 {veiculo} (KM atual: {veiculo.km_atual:,})')
                    
                    # Mostrar registros existentes
                    registros = veiculo.registromanutencao_set.order_by('-km', '-data')[:5]
                    if registros:
                        self.stdout.write('   📋 Últimos registros:')
                        for reg in registros:
                            self.stdout.write(f'   • {reg.peca.nome}: {reg.km:,} km ({reg.data.strftime("%d/%m/%Y")})')
                    
                    # Testar novo sistema de alertas
                    alertas = veiculo.get_alertas_ativos()
                    estatisticas = veiculo.get_estatisticas_manutencao()
                    
                    self.stdout.write(f'\n   🔔 ALERTAS DETECTADOS: {len(alertas)}')
                    self.stdout.write(f'   🔴 Urgentes: {estatisticas["urgentes"]}')
                    self.stdout.write(f'   🟡 Atenção: {estatisticas["atencao"]}')
                    self.stdout.write(f'   📊 Por KM: {estatisticas["alertas_km"]} | Por Tempo: {estatisticas["alertas_tempo"]}')
                    
                    if alertas:
                        self.stdout.write('\n   📝 DETALHES DOS ALERTAS:')
                        for i, alerta in enumerate(alertas[:3], 1):  # Mostrar apenas os 3 primeiros
                            tipo_icon = '⏰' if alerta['tipo_alerta'] == 'tempo' else '🛣️'
                            self.stdout.write(f'   {i}. {alerta["cor"]} {alerta["item"]}:')
                            self.stdout.write(f'      Status: {alerta["status"]}')
                            self.stdout.write(f'      Tipo: {tipo_icon} {alerta["tipo_alerta"].title()}')
                            self.stdout.write(f'      Última troca: {alerta["ultima_troca_km"]:,} km ({alerta["ultima_troca_data"]})')
                    else:
                        self.stdout.write('   ✅ Nenhum alerta ativo - veículo em dia!')
        
        # Sugestão de dados de teste  
        self.stdout.write('\n' + '=' * 70)
        self.stdout.write(self.style.SUCCESS('💡 COMO TESTAR O SISTEMA:'))
        self.stdout.write('\n1. CENÁRIO ÓLEO VENCIDO:')
        self.stdout.write('   📅 Data: 15/03/2025 (7 meses atrás)')
        self.stdout.write('   🛣️ KM: [KM_atual - 10.500] (ex: se tem 38000, use 27500)')
        self.stdout.write('   🔧 Peça: Óleo do motor')
        self.stdout.write('   💰 Preço: R$ 89,90')
        
        self.stdout.write('\n2. CENÁRIO FILTRO URGENTE:')
        self.stdout.write('   📅 Data: 15/10/2025 (11 dias atrás)')
        self.stdout.write('   🛣️ KM: [KM_atual - 500] (ex: se tem 38000, use 37500)')  
        self.stdout.write('   🔧 Peça: Filtro de ar')
        self.stdout.write('   💰 Preço: R$ 45,50')
        
        self.stdout.write('\n3. CENÁRIO BATERIA POR TEMPO:')
        self.stdout.write('   📅 Data: 15/11/2022 (3 anos atrás)')
        self.stdout.write('   🛣️ KM: [KM_atual - 15000] (para não vencer por KM)')
        self.stdout.write('   🔧 Peça: Bateria')
        self.stdout.write('   💰 Preço: R$ 280,00')
        
        self.stdout.write('\n' + '=' * 70)
        self.stdout.write(self.style.SUCCESS('🎯 SISTEMA INTELIGENTE ATIVO!'))
        self.stdout.write('• Calcula por KM E por tempo de durabilidade')
        self.stdout.write('• Mostra o critério mais crítico')
        self.stdout.write('• Base de dados com 15+ tipos de peças')
        self.stdout.write('• Alertas automáticos conforme você registra manutenções')
        self.stdout.write('=' * 70)