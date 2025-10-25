from django.core.management.base import BaseCommand
from drivecar.models import Peca

class Command(BaseCommand):
    help = "Popula o banco com categorias e peças iniciais"

    categorias_e_pecas = {
        "Motor": [
            "Correia dentada",
            "Correia do alternador / correia de acessórios",
            "Velas de ignição",
            "Cabos de vela",
            "Filtro de ar do motor",
            "Filtro de combustível",
            "Bomba de combustível",
            "Radiador",
            "Mangueiras do radiador",
            "Termostato",
            "Óleo do motor",
            "Filtro de óleo",
            "Junta do cabeçote",
            "Pistão",
            "Anéis de pistão",
            "Biela",
            "Válvulas",
            "Cabeçote",
            "Cárter",
            "Sensor de temperatura",
            "Sensor de oxigênio (sonda lambda)",
        ],
        "Transmissão e Embreagem": [
            "Embreagem (kit: platô, disco e rolamento)",
            "Fluido de embreagem",
            "Câmbio (manual ou automático)",
            "Fluido de transmissão",
            "Semieixo / homocinética",
            "Retentores",
            "Cabo de embreagem",
        ],
        "Suspensão e Direção": [
            "Amortecedores",
            "Molas helicoidais",
            "Coxins",
            "Buchas de bandeja",
            "Pivôs",
            "Terminal de direção",
            "Braço axial",
            "Junta homocinética",
            "Rolamentos das rodas",
            "Alinhamento / balanceamento (serviço)",
            "Fluido da direção hidráulica",
        ],
        "Freios": [
            "Pastilhas de freio",
            "Discos de freio",
            "Tambor de freio",
            "Lonas de freio",
            "Fluido de freio",
            "Cilindro mestre",
            "Servo-freio",
            "Pinça de freio",
            "Sensor de ABS",
        ],
        "Sistema Elétrico": [
            "Bateria",
            "Alternador",
            "Motor de partida",
            "Fusíveis",
            "Relés",
            "Chicote elétrico",
            "Faróis / lanternas",
            "Lâmpadas (farol, freio, ré, seta)",
            "Painel de instrumentos",
            "Sensor de marcha lenta",
        ],
        "Ar-condicionado e Climatização": [
            "Filtro de cabine",
            "Compressor do ar-condicionado",
            "Condensador",
            "Evaporador",
            "Gás do ar-condicionado",
            "Mangueiras do sistema",
            "Válvula de expansão",
        ],
        "Carroceria e Itens Externos": [
            "Parachoques",
            "Retrovisores",
            "Para-brisa",
            "Palhetas do limpador",
            "Reservatório de água do limpador",
            "Capô / portas / tampa traseira",
            "Travas e fechaduras",
        ],
        "Fluidos e Manutenções Gerais": [
            "Óleo do motor",
            "Fluido de freio",
            "Fluido da direção hidráulica",
            "Fluido da transmissão",
            "Água do radiador (aditivo)",
            "Limpeza de bicos injetores (serviço)",
        ],
    }

    # Map human-readable category to internal choice key in Peca.CATEGORIAS
    CATEGORY_MAP = {label: key for key, label in Peca.CATEGORIAS}

    def handle(self, *args, **options):
        created = 0
        for categoria_label, pecas in self.categorias_e_pecas.items():
            if categoria_label not in self.CATEGORY_MAP:
                self.stdout.write(self.style.WARNING(f"Categoria não mapeada: {categoria_label} -- pulando"))
                continue
            categoria_key = self.CATEGORY_MAP[categoria_label]
            for nome in pecas:
                obj, was_created = Peca.objects.get_or_create(categoria=categoria_key, nome=nome)
                if was_created:
                    created += 1
                    self.stdout.write(self.style.SUCCESS(f"Criada peça: {obj.nome} ({categoria_label})"))
        self.stdout.write(self.style.SUCCESS(f"Processo finalizado. Total criadas: {created}"))
