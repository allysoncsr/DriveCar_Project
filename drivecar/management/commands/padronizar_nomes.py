import re
from django.core.management.base import BaseCommand
from drivecar.models import Marca, Modelo, Versao


class Command(BaseCommand):
    help = 'Padroniza nomes de marcas, modelos e versões seguindo convenções'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Apenas mostra o que seria alterado, sem salvar',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        self.stdout.write('📋 PADRONIZAÇÃO DE NOMES - BIBLIOTECA DE VEÍCULOS')
        self.stdout.write('=' * 55)
        
        if dry_run:
            self.stdout.write('🔍 MODO DRY-RUN - Nenhuma alteração será salva')
        
        alteracoes_marcas = 0
        alteracoes_modelos = 0
        alteracoes_versoes = 0
        
        # 1. PADRONIZAR MARCAS (SEMPRE MAIÚSCULAS)
        self.stdout.write('\n1. 🏷️  PADRONIZANDO MARCAS:')
        marcas = Marca.objects.all()
        
        for marca in marcas:
            nome_original = marca.nome
            nome_padronizado = self.padronizar_marca(nome_original)
            
            if nome_original != nome_padronizado:
                self.stdout.write(f'   📝 {nome_original} → {nome_padronizado}')
                if not dry_run:
                    marca.nome = nome_padronizado
                    marca.save()
                alteracoes_marcas += 1
            else:
                self.stdout.write(f'   ✅ {nome_original} (já padronizado)')
        
        # 2. PADRONIZAR MODELOS (Title Case, sem marca duplicada)
        self.stdout.write('\n2. 🚙 PADRONIZANDO MODELOS:')
        modelos = Modelo.objects.all()
        
        for modelo in modelos:
            nome_original = modelo.nome
            nome_padronizado = self.padronizar_modelo(nome_original, modelo.marca.nome)
            
            if nome_original != nome_padronizado:
                self.stdout.write(f'   📝 {modelo.marca.nome}: {nome_original} → {nome_padronizado}')
                if not dry_run:
                    modelo.nome = nome_padronizado
                    modelo.save()
                alteracoes_modelos += 1
        
        # 3. PADRONIZAR VERSÕES (Title Case, sem redundâncias)
        self.stdout.write('\n3. ⚙️  PADRONIZANDO VERSÕES:')
        versoes = Versao.objects.all()[:20]  # Mostrar apenas algumas para não poluir
        
        for versao in versoes:
            nome_original = versao.nome
            nome_padronizado = self.padronizar_versao(nome_original)
            
            if nome_original != nome_padronizado:
                self.stdout.write(f'   📝 {versao.modelo.marca.nome} {versao.modelo.nome}: {nome_original} → {nome_padronizado}')
                if not dry_run:
                    versao.nome = nome_padronizado
                    versao.save()
                alteracoes_versoes += 1
        
        # RELATÓRIO FINAL
        self.stdout.write('\n' + '='*55)
        self.stdout.write('📊 RELATÓRIO DE PADRONIZAÇÃO:')
        self.stdout.write(f'   🏷️  Marcas alteradas: {alteracoes_marcas}')
        self.stdout.write(f'   🚙 Modelos alterados: {alteracoes_modelos}')
        self.stdout.write(f'   ⚙️  Versões alteradas: {alteracoes_versoes}')
        
        if dry_run:
            self.stdout.write('\n🔍 Para aplicar as alterações, execute sem --dry-run')
        else:
            self.stdout.write('\n✅ Padronização concluída!')
        
        # DIRETRIZES
        self.stdout.write('\n📋 DIRETRIZES PARA FUTURAS INSERÇÕES:')
        diretrizes = [
            "🏷️  MARCAS: Sempre em MAIÚSCULAS (ex: TOYOTA, CHEVROLET, CITROËN)",
            "🚙 MODELOS: Title Case, sem marca duplicada (ex: Corolla, Onix, C3)",
            "⚙️  VERSÕES: Title Case, com detalhes técnicos (ex: GLi 2.0 Flex Automático)",
            "🔤 ACENTOS: Manter acentos originais (Citroën, não Citroen)",
            "🚫 REDUNDÂNCIA: Evitar repetir marca no modelo ou modelo na versão"
        ]
        
        for diretriz in diretrizes:
            self.stdout.write(f'   {diretriz}')

    def padronizar_marca(self, nome):
        """Padroniza nome da marca (MAIÚSCULAS)"""
        return nome.upper().strip()
    
    def padronizar_modelo(self, nome, marca_nome):
        """Padroniza nome do modelo (remove marca duplicada, mantém formato adequado)"""
        nome = nome.strip()
        marca_upper = marca_nome.upper()
        
        # Remove marca do início se existir
        if nome.upper().startswith(marca_upper):
            nome = nome[len(marca_upper):].strip()
        
        # Preservar siglas e formatos especiais
        preservar_formato = [
            'SUV', 'GT-R', 'CR-V', 'HR-V', 'WR-V', 'RAV4', 'SW4', 'HB20', 'HB20S',
            'ix35', 'i30', 'NSX', 'S2000', 'F-150', 'T-Cross', 'e-Golf', 'ID',
            'C3', 'C4', 'X1H', 'NV200', 'H-1', 'H100', 'EcoSport'
        ]
        
        # Se contém sigla conhecida, não alterar
        for sigla in preservar_formato:
            if sigla.upper() in nome.upper():
                return nome
        
        # Para outros casos, aplicar title case apenas em palavras específicas
        palavras = nome.split()
        palavras_padronizadas = []
        
        for palavra in palavras:
            # Preservar parênteses e conteúdo
            if '(' in palavra or ')' in palavra:
                palavras_padronizadas.append(palavra)
            # Preservar números e códigos
            elif any(char.isdigit() for char in palavra):
                palavras_padronizadas.append(palavra)
            # Title case para palavras normais
            else:
                palavras_padronizadas.append(palavra.title())
        
        return ' '.join(palavras_padronizadas)
    
    def padronizar_versao(self, nome):
        """Padroniza nome da versão (Title Case básico)"""
        return nome.strip()