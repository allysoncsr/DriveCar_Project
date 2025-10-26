from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Cria usuários de teste para o DriveCar'

    def handle(self, *args, **options):
        # Usuário administrador
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_user(
                username='admin',
                password='admin123',
                email='admin@drivecar.com',
                first_name='Administrador',
                is_staff=True,
                is_superuser=True
            )
            self.stdout.write(
                self.style.SUCCESS(f'✅ Usuário admin criado com sucesso!')
            )
        else:
            self.stdout.write(
                self.style.WARNING('⚠️ Usuário admin já existe')
            )

        # Usuário comum
        if not User.objects.filter(username='usuario').exists():
            user = User.objects.create_user(
                username='usuario',
                password='123456',
                email='usuario@drivecar.com',
                first_name='Usuário',
            )
            self.stdout.write(
                self.style.SUCCESS(f'✅ Usuário comum criado com sucesso!')
            )
        else:
            self.stdout.write(
                self.style.WARNING('⚠️ Usuário comum já existe')
            )

        self.stdout.write(
            self.style.SUCCESS('\n🚗 Usuários de teste do DriveCar:')
        )
        self.stdout.write('   👨‍💼 Admin: admin / admin123')
        self.stdout.write('   👤 Usuário: usuario / 123456')