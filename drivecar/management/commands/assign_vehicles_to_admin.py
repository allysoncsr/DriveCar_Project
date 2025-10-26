from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from drivecar.models import Veiculo


class Command(BaseCommand):
    help = 'Associa todos os veículos existentes ao usuário admin'

    def handle(self, *args, **options):
        try:
            # Pegar o usuário admin (ID 3)
            admin_user = User.objects.get(id=3)  # admin
            self.stdout.write(f"Usuário admin encontrado: {admin_user.username}")
            
            # Pegar todos os veículos que não têm usuário (None)
            veiculos_sem_usuario = Veiculo.objects.filter(usuario_id=3)
            count = veiculos_sem_usuario.count()
            
            self.stdout.write(f"Encontrados {count} veículos já associados ao admin")
            
            # Verificar se há veículos
            todos_veiculos = Veiculo.objects.all()
            self.stdout.write(f"Total de veículos no sistema: {todos_veiculos.count()}")
            
            for veiculo in todos_veiculos:
                self.stdout.write(f"- {veiculo.marca} {veiculo.modelo} (ID: {veiculo.id}) - Usuário: {veiculo.usuario_id}")
            
            self.stdout.write(
                self.style.SUCCESS(f'✓ Verificação completa. Veículos associados ao admin: {count}')
            )
            
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('Usuário admin (ID=3) não encontrado')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erro: {str(e)}')
            )