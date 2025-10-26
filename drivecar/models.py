from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timedelta


class Marca(models.Model):
    nome = models.CharField(_("nome da marca"), max_length=50, unique=True)
    logo = models.CharField(_("logo/imagem"), max_length=200, blank=True)
    ativo = models.BooleanField(_("ativo"), default=True)
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = _("Marca")
        verbose_name_plural = _("Marcas")
        ordering = ["nome"]


class Modelo(models.Model):
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, verbose_name=_("marca"))
    nome = models.CharField(_("nome do modelo"), max_length=100)
    ano_inicio = models.PositiveIntegerField(_("ano de início"), null=True, blank=True)
    ano_fim = models.PositiveIntegerField(_("ano de fim"), null=True, blank=True)
    ativo = models.BooleanField(_("ativo"), default=True)
    
    def __str__(self):
        return f"{self.marca.nome} {self.nome}"
    
    class Meta:
        verbose_name = _("Modelo")
        verbose_name_plural = _("Modelos")
        ordering = ["marca__nome", "nome"]
        unique_together = ["marca", "nome"]


class Versao(models.Model):
    modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE, verbose_name=_("modelo"))
    nome = models.CharField(_("nome da versão"), max_length=100)
    motor = models.CharField(_("motor"), max_length=50, blank=True)
    combustivel = models.CharField(_("combustível"), max_length=20, blank=True)
    transmissao = models.CharField(_("transmissão"), max_length=20, blank=True)
    ano_inicio = models.PositiveIntegerField(_("ano de início"), null=True, blank=True)
    ano_fim = models.PositiveIntegerField(_("ano de fim"), null=True, blank=True)
    ativo = models.BooleanField(_("ativo"), default=True)
    
    def __str__(self):
        return f"{self.modelo} {self.nome}"
    
    class Meta:
        verbose_name = _("Versão")
        verbose_name_plural = _("Versões")
        ordering = ["modelo__marca__nome", "modelo__nome", "nome"]
        unique_together = ["modelo", "nome"]

class Veiculo(models.Model):
    TIPO_COMBUSTIVEL_CHOICES = [
        ('GASOLINA', 'Gasolina'),
        ('ALCOOL', 'Álcool / Etanol'),
        ('FLEX', 'Flex (Gasolina/Etanol)'),
        ('DIESEL', 'Diesel'),
        ('GNV', 'GNV (Gás Natural Veicular)'),
        ('HIBRIDO', 'Híbrido'),
        ('ELETRICO', 'Elétrico'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("usuário"))
    # Novos campos com ForeignKey
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT, verbose_name=_("marca"), null=True, blank=True)
    modelo = models.ForeignKey(Modelo, on_delete=models.PROTECT, verbose_name=_("modelo"), null=True, blank=True)
    versao = models.ForeignKey(Versao, on_delete=models.PROTECT, verbose_name=_("versão"), null=True, blank=True)
    # Campos antigos mantidos temporariamente para compatibilidade
    marca_legado = models.CharField(_("marca (legado)"), max_length=50, blank=True)
    modelo_legado = models.CharField(_("modelo (legado)"), max_length=50, blank=True)
    
    ano = models.PositiveIntegerField(_("ano"))
    placa = models.CharField(_("placa"), max_length=10, blank=True)
    km_atual = models.PositiveIntegerField(_("quilometragem atual"), default=0)
    combustivel = models.CharField(_("combustível"), max_length=20, choices=TIPO_COMBUSTIVEL_CHOICES, blank=True)

    def __str__(self):
        # Usar novos campos se disponíveis, senão usar legado
        marca_nome = self.marca.nome if self.marca else self.marca_legado
        modelo_nome = self.modelo.nome if self.modelo else self.modelo_legado
        versao_nome = f" {self.versao.nome}" if self.versao else ""
        return f"{marca_nome} {modelo_nome}{versao_nome} ({self.ano})"
    
    @property
    def marca_display(self):
        return self.marca.nome if self.marca else self.marca_legado
    
    @property 
    def modelo_display(self):
        return self.modelo.nome if self.modelo else self.modelo_legado
    
    @property
    def titulo_limpo(self):
        """Retorna título sem duplicação de marca"""
        marca_nome = self.marca.nome if self.marca else self.marca_legado
        modelo_nome = self.modelo.nome if self.modelo else self.modelo_legado
        
        if marca_nome and modelo_nome:
            # Se o nome do modelo já contém a marca, usar apenas o modelo
            if marca_nome.upper() in modelo_nome.upper():
                return modelo_nome
            else:
                return f"{marca_nome} {modelo_nome}"
        elif modelo_nome:
            return modelo_nome
        elif marca_nome:
            return marca_nome
        else:
            return "Veículo sem identificação"

    def total_gasto_manutencao(self):
        """Calcula o valor total gasto em manutenção deste veículo"""
        from django.db.models import Sum
        total = self.registromanutencao_set.aggregate(
            total=Sum('preco')
        )['total']
        return total or 0
    
    def total_gasto_manutencao_formatado(self):
        """Retorna o valor total formatado como moeda brasileira"""
        total = self.total_gasto_manutencao()
        
        # Formatação brasileira simples
        valor_str = f"{total:.2f}"
        partes = valor_str.split('.')
        parte_inteira = partes[0]
        parte_decimal = partes[1]
        
        # Adicionar pontos nos milhares
        if len(parte_inteira) > 3:
            # Formatar com pontos a cada 3 dígitos
            parte_inteira_formatada = ""
            for i, digit in enumerate(parte_inteira[::-1]):
                if i > 0 and i % 3 == 0:
                    parte_inteira_formatada = "." + parte_inteira_formatada
                parte_inteira_formatada = digit + parte_inteira_formatada
            parte_inteira = parte_inteira_formatada
        
        return f"R$ {parte_inteira},{parte_decimal}"
    
    def get_alertas_ativos(self):
        """Retorna alertas ativos baseados na quilometragem, histórico e durabilidade das peças"""
        from datetime import datetime, timedelta
        
        alertas = []
        
        # Base de dados completa de peças com intervalos por KM e tempo
        pecas_intervalos = {
            # MOTOR
            'Óleo': {'km': 10000, 'meses': 6, 'categoria': 'motor'},
            'Filtro de óleo': {'km': 10000, 'meses': 6, 'categoria': 'motor'},
            'Filtro de ar': {'km': 15000, 'meses': 12, 'categoria': 'motor'},
            'Filtro de combustível': {'km': 20000, 'meses': 24, 'categoria': 'motor'},
            'Vela': {'km': 30000, 'meses': 24, 'categoria': 'motor'},
            'Correia': {'km': 60000, 'meses': 48, 'categoria': 'motor'},
            
            # FREIOS
            'Pastilha': {'km': 25000, 'meses': 18, 'categoria': 'freios'},
            'Disco': {'km': 50000, 'meses': 36, 'categoria': 'freios'},
            'Fluido de freio': {'km': 30000, 'meses': 24, 'categoria': 'freios'},
            
            # SUSPENSÃO  
            'Amortecedor': {'km': 80000, 'meses': 60, 'categoria': 'suspensao'},
            'Mola': {'km': 100000, 'meses': 72, 'categoria': 'suspensao'},
            
            # PNEUS
            'Pneu': {'km': 40000, 'meses': 60, 'categoria': 'pneus'},
            
            # ELÉTRICA
            'Bateria': {'km': 50000, 'meses': 36, 'categoria': 'eletrica'},
            
            # TRANSMISSÃO
            'Embreagem': {'km': 80000, 'meses': 60, 'categoria': 'transmissao'},
            'Óleo cambio': {'km': 60000, 'meses': 48, 'categoria': 'transmissao'},
        }
        
        # Pegar KM atual (maior KM entre km_atual e último registro)
        ultimo_registro = self.registromanutencao_set.order_by('-km').first()
        km_atual = max(self.km_atual, ultimo_registro.km if ultimo_registro else 0)
        
        # Data atual para cálculos de tempo
        hoje = datetime.now().date()
        
        # Analisar cada peça cadastrada no sistema
        for peca_nome, dados in pecas_intervalos.items():
            # Buscar último registro desta peça (busca inteligente por palavras-chave)
            ultimo_item = self.registromanutencao_set.filter(
                peca__nome__icontains=peca_nome
            ).order_by('-km', '-data').first()
            
            if ultimo_item:
                # CÁLCULO POR QUILOMETRAGEM
                km_ultima_troca = ultimo_item.km
                km_proxima_troca = km_ultima_troca + dados['km']
                km_restante = km_proxima_troca - km_atual
                
                # CÁLCULO POR TEMPO (durabilidade)
                data_ultima_troca = ultimo_item.data
                data_proxima_troca = data_ultima_troca + timedelta(days=dados['meses'] * 30)
                dias_restantes = (data_proxima_troca - hoje).days
                
                # DETERMINAR QUAL CRITÉRIO É MAIS CRÍTICO
                km_vencido = km_restante <= 0
                tempo_vencido = dias_restantes <= 0
                
                km_urgente = km_restante <= 1000
                tempo_urgente = dias_restantes <= 30
                
                km_atencao = km_restante <= 3000  
                tempo_atencao = dias_restantes <= 90
                
                # LÓGICA DE PRIORIDADE (o que vencer primeiro)
                if km_vencido or tempo_vencido:
                    urgencia = 'urgente'
                    if km_vencido and tempo_vencido:
                        status = 'VENCIDO por KM e tempo'
                    elif km_vencido:
                        status = f'VENCIDO há {abs(km_restante)} km'
                    else:
                        status = f'VENCIDO há {abs(dias_restantes)} dias'
                    cor = '🔴'
                    
                elif km_urgente or tempo_urgente:
                    urgencia = 'urgente'
                    if km_urgente and tempo_urgente:
                        status = f'{km_restante} km ou {dias_restantes} dias'
                    elif km_restante < dias_restantes * 10:  # Se KM é mais crítico
                        status = f'{km_restante} km restantes'
                    else:
                        status = f'{dias_restantes} dias restantes'
                    cor = '🔴'
                    
                elif km_atencao or tempo_atencao:
                    urgencia = 'atencao'
                    if km_restante < dias_restantes * 10:  # KM mais próximo
                        status = f'{km_restante} km restantes'
                    else:
                        status = f'{dias_restantes} dias restantes'
                    cor = '🟡'
                    
                else:
                    urgencia = 'ok'
                    # Mostrar o que vence primeiro
                    if km_restante < dias_restantes * 10:
                        status = f'{km_restante} km restantes'
                    else:
                        status = f'{dias_restantes} dias restantes'
                    cor = '🟢'
                
                # Adicionar apenas alertas que precisam de atenção
                if urgencia in ['urgente', 'atencao']:
                    alertas.append({
                        'item': peca_nome,
                        'peca_completa': ultimo_item.peca.nome,
                        'status': status,
                        'urgencia': urgencia,
                        'cor': cor,
                        'km_restante': km_restante,
                        'dias_restantes': dias_restantes,
                        'km_proxima': km_proxima_troca,
                        'data_proxima': data_proxima_troca.strftime('%d/%m/%Y'),
                        'ultima_troca_km': km_ultima_troca,
                        'ultima_troca_data': data_ultima_troca.strftime('%d/%m/%Y'),
                        'tipo_alerta': 'km' if km_restante < dias_restantes * 10 else 'tempo'
                    })
        
        # Ordenar por urgência (urgente primeiro) e depois pelo critério mais crítico
        alertas.sort(key=lambda x: (
            x['urgencia'] != 'urgente',  # Urgente primeiro
            x['urgencia'] != 'atencao',  # Depois atenção
            min(x['km_restante'] if x['km_restante'] > 0 else 999999, 
                x['dias_restantes'] if x['dias_restantes'] > 0 else 999999)  # Menor tempo/km
        ))
        
        return alertas
    
    def get_proximas_manutencoes(self):
        """Retorna próximas manutenções recomendadas (não urgentes)"""
        from datetime import datetime, timedelta
        
        alertas_todos = []
        hoje = datetime.now().date()
        
        # Base de dados de peças (mesma do método anterior)
        pecas_intervalos = {
            'Óleo': {'km': 10000, 'meses': 6},
            'Filtro de ar': {'km': 15000, 'meses': 12},
            'Filtro de combustível': {'km': 20000, 'meses': 24},
            'Vela': {'km': 30000, 'meses': 24},
            'Pastilha': {'km': 25000, 'meses': 18},
            'Bateria': {'km': 50000, 'meses': 36},
        }
        
        ultimo_registro = self.registromanutencao_set.order_by('-km').first()
        km_atual = max(self.km_atual, ultimo_registro.km if ultimo_registro else 0)
        
        for peca_nome, dados in pecas_intervalos.items():
            ultimo_item = self.registromanutencao_set.filter(
                peca__nome__icontains=peca_nome
            ).order_by('-km', '-data').first()
            
            if ultimo_item:
                km_proxima = ultimo_item.km + dados['km']
                data_proxima = ultimo_item.data + timedelta(days=dados['meses'] * 30)
                
                alertas_todos.append({
                    'item': peca_nome,
                    'km_proxima': km_proxima,
                    'data_proxima': data_proxima,
                    'km_restante': km_proxima - km_atual,
                    'dias_restantes': (data_proxima - hoje).days
                })
        
        return alertas_todos
    
    def get_estatisticas_manutencao(self):
        """Retorna estatísticas completas de manutenção"""
        alertas = self.get_alertas_ativos()
        
        return {
            'total_alertas': len(alertas),
            'urgentes': len([a for a in alertas if a['urgencia'] == 'urgente']),
            'atencao': len([a for a in alertas if a['urgencia'] == 'atencao']),
            'alertas_km': len([a for a in alertas if a['tipo_alerta'] == 'km']),
            'alertas_tempo': len([a for a in alertas if a['tipo_alerta'] == 'tempo']),
            'proximo_vencimento': min([
                min(a['km_restante'] if a['km_restante'] > 0 else 999999,
                    a['dias_restantes'] if a['dias_restantes'] > 0 else 999999)
                for a in alertas
            ]) if alertas else None
        }

    class Meta:
        verbose_name = _("Veículo")
        verbose_name_plural = _("Veículos")


class Peca(models.Model):
    CATEGORIAS = [
        ("motor", "Motor"),
        ("transmissao", "Transmissão e Embreagem"),
        ("suspensao", "Suspensão e Direção"),
        ("freios", "Freios"),
        ("eletrica", "Sistema Elétrico"),
        ("ar_condicionado", "Ar-condicionado e Climatização"),
        ("carroceria", "Carroceria e Itens Externos"),
        ("fluidos", "Fluidos e Manutenções Gerais"),
    ]
    categoria = models.CharField(_("categoria"), max_length=30, choices=CATEGORIAS)
    nome = models.CharField(_("nome da peça"), max_length=100)

    def __str__(self):
        return f"{self.nome} - {self.get_categoria_display()}"

    class Meta:
        verbose_name = _("Peça")
        verbose_name_plural = _("Peças")
        ordering = ["categoria", "nome"]


class RegistroManutencao(models.Model):
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, verbose_name=_("veículo"))
    peca = models.ForeignKey(Peca, on_delete=models.CASCADE, verbose_name=_("peça"))
    data = models.DateField(_("data"))
    km = models.PositiveIntegerField(_("quilometragem"))
    preco = models.DecimalField(_("preço (R$)"), max_digits=10, decimal_places=2)
    troca = models.BooleanField(_("troca (sim/não)"), default=False)
    garantia_meses = models.PositiveIntegerField(_("tempo de garantia (meses)"), null=True, blank=True)
    observacoes = models.TextField(_("observações"), blank=True)
    # Campo remanescente do sistema de alertas removido - mantido para compatibilidade
    alerta_ativo = models.BooleanField(_("alerta ativo"), default=False)

    def __str__(self):
        return f"{self.veiculo} - {self.peca.nome} @ {self.km} km"

    class Meta:
        verbose_name = _("Registro de Manutenção")
        verbose_name_plural = _("Registros de Manutenção")
        ordering = ["-data", "-km"]


class Alerta(models.Model):
    TIPO_CHOICES = [
        ("km", "Por quilometragem"),
        ("tempo", "Por tempo"),
    ]
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, verbose_name=_("veículo"))
    descricao = models.CharField(_("descrição"), max_length=150)
    tipo = models.CharField(_("tipo"), choices=TIPO_CHOICES, max_length=10)
    km_previsto = models.PositiveIntegerField(_("quilometragem prevista"), null=True, blank=True)
    data_prevista = models.DateField(_("data prevista"), null=True, blank=True)
    ativo = models.BooleanField(_("ativo"), default=True)
    criado_em = models.DateTimeField(_("criado em"), auto_now_add=True)

    def __str__(self):
        return f"{self.descricao} ({self.get_tipo_display()})"

    class Meta:
        verbose_name = _("Alerta")
        verbose_name_plural = _("Alertas")

