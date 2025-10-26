from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from drivecar.models import Veiculo, Peca, RegistroManutencao, Marca, Modelo, Versao
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Cria dados de teste para demonstrar o sistema de alertas'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚗 Iniciando criação de dados de teste para alertas...'))
        
        # 1. Criar usuário de teste (se não existir)
        user, created = User.objects.get_or_create(
            username='teste_alertas',
            defaults={
                'first_name': 'Teste',
                'email': 'teste@alertas.com'
            }
        )
        if created:
            user.set_password('123456')
            user.save()
            self.stdout.write(f'✅ Usuário criado: {user.username}')
        else:
            self.stdout.write(f'👤 Usuário já existe: {user.username}')

        # 2. Verificar se temos marcas/modelos
        marca_ford = Marca.objects.filter(nome__icontains='FORD').first()
        if not marca_ford:
            self.stdout.write(self.style.ERROR('❌ Marca FORD não encontrada. Execute o comando de importação de veículos primeiro.'))
            return

        modelo_ka = Modelo.objects.filter(marca=marca_ford, nome__icontains='Ka').first()
        if not modelo_ka:
            self.stdout.write(self.style.ERROR('❌ Modelo Ka não encontrado.'))
            return

        # 3. Criar veículo de teste com situação crítica
        veiculo_teste = Veiculo.objects.filter(usuario=user, marca=marca_ford).first()
        if not veiculo_teste:
            veiculo_teste = Veiculo.objects.create(
                usuario=user,
                marca=marca_ford,
                modelo=modelo_ka,
                ano=2020,
                placa='TST-1234',
                km_atual=45000,  # KM alto para gerar alertas
                combustivel='FLEX'
            )
            self.stdout.write(f'🚗 Veículo criado: {veiculo_teste}')
        else:
            # Atualizar KM para cenário de teste
            veiculo_teste.km_atual = 45000
            veiculo_teste.save()
            self.stdout.write(f'🔄 Veículo atualizado: {veiculo_teste}')

        # 4. Obter peças para criar registros
        peca_oleo = Peca.objects.filter(nome__icontains='Óleo').first()
        peca_filtro_ar = Peca.objects.filter(nome__icontains='Filtro de ar').first()
        peca_filtro_combustivel = Peca.objects.filter(nome__icontains='Filtro de combustível').first()
        peca_velas = Peca.objects.filter(nome__icontains='Vela').first()

        if not all([peca_oleo, peca_filtro_ar, peca_filtro_combustivel, peca_velas]):
            self.stdout.write(self.style.ERROR('❌ Algumas peças não foram encontradas. Verifique se o banco está populado.'))
            return

        # 5. Limpar registros antigos deste veículo
        RegistroManutencao.objects.filter(veiculo=veiculo_teste).delete()
        self.stdout.write('🧹 Registros antigos limpos')

        # 6. Criar cenários de teste específicos
        self.stdout.write('\n📋 Criando cenários de teste...')

        # CENÁRIO 1: Óleo VENCIDO (última troca há mais de 10.000 km)
        if peca_oleo:
            registro_oleo = RegistroManutencao.objects.create(
                veiculo=veiculo_teste,
                peca=peca_oleo,
                data=datetime.now() - timedelta(days=120),
                km=34000,  # 11.000 km atrás (45000 - 34000 = 11000)
                preco=89.90,
                troca=True,
                garantia_meses=3,
                observacoes='Última troca de óleo - CENÁRIO TESTE: VENCIDO'
            )
            self.stdout.write('🔴 URGENTE: Óleo vencido há 1.000 km (última: 34.000 km)')

        # CENÁRIO 2: Filtro de ar ATENÇÃO (próximo do vencimento)
        if peca_filtro_ar:
            registro_filtro = RegistroManutencao.objects.create(
                veiculo=veiculo_teste,
                peca=peca_filtro_ar,
                data=datetime.now() - timedelta(days=90),
                km=43000,  # 2.000 km atrás, próximo dos 15.000 km
                preco=45.50,
                troca=True,
                garantia_meses=6,
                observacoes='Última troca filtro ar - CENÁRIO TESTE: ATENÇÃO'
            )
            self.stdout.write('🟡 ATENÇÃO: Filtro de ar em 2.000 km (próxima: 58.000 km)')

        # CENÁRIO 3: Filtro combustível URGENTE (quase vencido)
        if peca_filtro_combustivel:
            registro_combustivel = RegistroManutencao.objects.create(
                veiculo=veiculo_teste,
                peca=peca_filtro_combustivel,
                data=datetime.now() - timedelta(days=200),
                km=44500,  # 500 km atrás, muito próximo
                preco=78.00,
                troca=True,
                garantia_meses=12,
                observacoes='Última troca filtro combustível - CENÁRIO TESTE: URGENTE'
            )
            self.stdout.write('🔴 URGENTE: Filtro combustível em 500 km (próxima: 64.500 km)')

        # CENÁRIO 4: Velas OK (não deve aparecer nos alertas)
        if peca_velas:
            registro_velas = RegistroManutencao.objects.create(
                veiculo=veiculo_teste,
                peca=peca_velas,
                data=datetime.now() - timedelta(days=60),
                km=42000,  # 3.000 km atrás, ainda tem 27.000 km
                preco=120.00,
                troca=True,
                garantia_meses=24,
                observacoes='Última troca velas - CENÁRIO TESTE: OK'
            )
            self.stdout.write('🟢 OK: Velas com 27.000 km restantes')

        # 7. Criar segundo veículo para mostrar múltiplos alertas
        marca_citroen = Marca.objects.filter(nome__icontains='CITROËN').first()
        if marca_citroen:
            modelo_c3 = Modelo.objects.filter(marca=marca_citroen, nome__icontains='C3').first()
            if modelo_c3:
                veiculo2 = Veiculo.objects.filter(usuario=user, marca=marca_citroen).first()
                if not veiculo2:
                    veiculo2 = Veiculo.objects.create(
                        usuario=user,
                        marca=marca_citroen,
                        modelo=modelo_c3,
                        ano=2023,
                        placa='TST-5678',
                        km_atual=38000,
                        combustivel='FLEX'
                    )
                    self.stdout.write(f'🚗 Segundo veículo criado: {veiculo2}')
                else:
                    veiculo2.km_atual = 38000
                    veiculo2.save()

                # Limpar registros antigos
                RegistroManutencao.objects.filter(veiculo=veiculo2).delete()

                # Criar alerta de atenção para o segundo veículo
                if peca_oleo:
                    RegistroManutencao.objects.create(
                        veiculo=veiculo2,
                        peca=peca_oleo,
                        data=datetime.now() - timedelta(days=80),
                        km=36000,  # 2.000 km atrás
                        preco=95.00,
                        troca=True,
                        garantia_meses=3,
                        observacoes='Óleo segundo veículo - CENÁRIO TESTE'
                    )
                    self.stdout.write('🟡 Segundo veículo: Óleo em 8.000 km')

        # 8. Testar o sistema de alertas
        self.stdout.write('\n🔍 Testando sistema de alertas...')
        alertas = veiculo_teste.get_alertas_ativos()
        
        self.stdout.write(f'\n📊 RESULTADO DOS ALERTAS - {veiculo_teste}:')
        self.stdout.write(f'   KM Atual: {veiculo_teste.km_atual:,} km')
        self.stdout.write(f'   Total de alertas: {len(alertas)}')
        
        for i, alerta in enumerate(alertas, 1):
            cor_texto = '🔴' if alerta['urgencia'] == 'urgente' else '🟡'
            self.stdout.write(f'   {i}. {cor_texto} {alerta["item"]}: {alerta["status"]}')

        # 9. Instruções para o usuário
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('✅ DADOS DE TESTE CRIADOS COM SUCESSO!'))
        self.stdout.write('\n📋 COMO VISUALIZAR OS ALERTAS:')
        self.stdout.write('   1. Inicie o servidor: python manage.py runserver')
        self.stdout.write('   2. Acesse: http://127.0.0.1:8000/')
        self.stdout.write('   3. Faça login com:')
        self.stdout.write('      👤 Usuário: teste_alertas')
        self.stdout.write('      🔑 Senha: 123456')
        self.stdout.write('\n🎯 VOCÊ DEVE VER:')
        self.stdout.write('   • Painel de alertas na tela principal')
        self.stdout.write('   • Cards vermelhos e amarelos com alertas')
        self.stdout.write('   • Detalhes específicos ao entrar na manutenção')
        
        self.stdout.write('\n💡 CENÁRIOS CRIADOS:')
        self.stdout.write('   🔴 Óleo do motor: VENCIDO')
        self.stdout.write('   🔴 Filtro combustível: 500 km restantes')
        self.stdout.write('   🟡 Filtro de ar: 2.000 km restantes')
        self.stdout.write('   🟢 Velas: OK (não aparece nos alertas)')
        
        self.stdout.write('\n' + '='*60)