from drivecar.models import *
from django.contrib.auth.models import User
from datetime import datetime

# Buscar usuário admin
u = User.objects.get(username='admin')
v = u.veiculo_set.first()

print(f'🚗 Veículo: {v.modelo} - KM atual: {v.km_atual}')

# Criar registro de bateria vencida por tempo (3+ anos)
r = RegistroManutencao.objects.create(
    veiculo=v,
    data_servico=datetime(2021, 11, 15).date(),
    km_atual=v.km_atual-15000,
    peca_servico='Bateria',
    preco_pago=280.00
)

print(f'📝 Registro criado: {r.peca_servico} em {r.data_servico}')

# Verificar alertas
alertas = v.get_alertas_ativos()
print(f'\n🔔 ALERTAS DETECTADOS: {len(alertas)}')

for alerta in alertas:
    print(f'• {alerta["tipo"]}: {alerta["descricao"]}')
    print(f'  Status: {alerta["status"]}')
    print(f'  Tipo alerta: {alerta["tipo_alerta"]}')