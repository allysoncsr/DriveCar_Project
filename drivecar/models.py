from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


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

