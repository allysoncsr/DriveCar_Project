from django.core.management.base import BaseCommand
from drivecar.models import Servico


class Command(BaseCommand):
    help = 'Popula a tabela de serviços com serviços mecânicos comuns'

    def handle(self, *args, **options):
        servicos_data = [
            # Motor e Sistema de Injeção
            ("motor", "Troca de óleo e filtro", "Troca do óleo lubrificante e filtro de óleo"),
            ("motor", "Limpeza de bicos injetores", "Limpeza e teste dos bicos injetores"),
            ("motor", "Regulagem de motor", "Ajuste da ignição e carburação"),
            ("motor", "Retífica de motor", "Retífica completa do motor"),
            ("motor", "Troca de velas de ignição", "Substituição das velas de ignição"),
            ("motor", "Limpeza do sistema de injeção", "Limpeza completa do sistema de combustível"),
            ("motor", "Teste de compressão", "Verificação da compressão dos cilindros"),
            ("motor", "Troca de correia dentada", "Substituição da correia dentada e tensor"),

            # Transmissão e Embreagem
            ("transmissao", "Troca de óleo do câmbio", "Substituição do óleo da transmissão"),
            ("transmissao", "Regulagem de embreagem", "Ajuste do sistema de embreagem"),
            ("transmissao", "Troca do kit embreagem", "Substituição completa do conjunto de embreagem"),
            ("transmissao", "Reparo de câmbio automático", "Manutenção e reparo da transmissão automática"),
            ("transmissao", "Sangria do sistema hidráulico", "Renovação do fluido hidráulico"),

            # Suspensão e Direção
            ("suspensao", "Alinhamento e balanceamento", "Alinhamento das rodas e balanceamento"),
            ("suspensao", "Troca de amortecedores", "Substituição dos amortecedores"),
            ("suspensao", "Regulagem da geometria", "Ajuste da geometria da suspensão"),
            ("suspensao", "Troca de molas", "Substituição das molas da suspensão"),
            ("suspensao", "Reparo da direção hidráulica", "Manutenção do sistema de direção"),
            ("suspensao", "Troca de buchas e pivôs", "Substituição de componentes da suspensão"),

            # Sistema de Freios
            ("freios", "Troca de pastilhas de freio", "Substituição das pastilhas dianteiras e/ou traseiras"),
            ("freios", "Troca de disco de freio", "Substituição dos discos de freio"),
            ("freios", "Sangria do sistema de freios", "Renovação do fluido de freio"),
            ("freios", "Regulagem de freio de mão", "Ajuste do freio de estacionamento"),
            ("freios", "Retífica de tambor/disco", "Usinagem de componentes de freio"),

            # Sistema Elétrico e Eletrônico
            ("eletrica", "Teste de bateria e alternador", "Verificação do sistema de carga"),
            ("eletrica", "Reparo de sistema elétrico", "Diagnóstico e reparo de problemas elétricos"),
            ("eletrica", "Instalação de acessórios", "Instalação de som, alarme, etc."),
            ("eletrica", "Scanner automotivo", "Diagnóstico eletrônico computadorizado"),
            ("eletrica", "Troca de lâmpadas", "Substituição do sistema de iluminação"),

            # Ar-condicionado e Climatização
            ("ar_condicionado", "Limpeza do sistema de ar", "Higienização completa do ar-condicionado"),
            ("ar_condicionado", "Carga de gás refrigerante", "Recarga do sistema de refrigeração"),
            ("ar_condicionado", "Troca do filtro do ar", "Substituição do filtro de cabine"),
            ("ar_condicionado", "Reparo do compressor", "Manutenção do compressor do ar-condicionado"),

            # Funilaria e Pintura
            ("carroceria", "Funilaria e pintura", "Reparo de lataria e pintura"),
            ("carroceria", "Polimento e enceramento", "Tratamento da pintura do veículo"),
            ("carroceria", "Reparo de para-choque", "Conserto e pintura de para-choques"),
            ("carroceria", "Troca de vidros", "Substituição de vidros automotivos"),

            # Pneus e Rodas
            ("pneus_rodas", "Montagem e desmontagem", "Serviço de montagem de pneus"),
            ("pneus_rodas", "Conserto de pneus", "Reparo de furos e remendos"),
            ("pneus_rodas", "Reforma de rodas", "Restauração de rodas de liga leve"),

            # Manutenção Geral
            ("manutencao_geral", "Revisão geral", "Inspeção completa do veículo"),
            ("manutencao_geral", "Preparação para viagem", "Check-up completo antes de viagens"),
            ("manutencao_geral", "Lavagem completa", "Lavagem externa e interna"),
            ("manutencao_geral", "Troca de filtros", "Substituição de filtros diversos"),
        ]

        created_count = 0
        for categoria, nome, descricao in servicos_data:
            servico, created = Servico.objects.get_or_create(
                categoria=categoria,
                nome=nome,
                defaults={'descricao': descricao}
            )
            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Criados {created_count} novos serviços. Total: {Servico.objects.count()}')
        )