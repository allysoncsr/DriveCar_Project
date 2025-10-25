from django.db import models
from django.utils.translation import gettext_lazy as _

class Veiculo(models.Model):
    marca = models.CharField(_("marca"), max_length=50)
    modelo = models.CharField(_("modelo"), max_length=50)
    ano = models.PositiveIntegerField(_("ano"))
    placa = models.CharField(_("placa"), max_length=10, blank=True)
    km_atual = models.PositiveIntegerField(_("quilometragem atual"), default=0)
    combustivel = models.CharField(_("combustível"), max_length=20, blank=True)

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.ano})"

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

