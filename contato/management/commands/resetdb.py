import os
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings

class Command(BaseCommand):
    help = "Reseta o banco de dados: apaga, recria, aplica migrações e roda o seed."

    def handle(self, *args, **kwargs):
        db_path = settings.DATABASES['default']['NAME']

        # ==============================
        # Apagar banco de dados
        # ==============================
        if os.path.exists(db_path):
            os.remove(db_path)
            self.stdout.write(self.style.WARNING(f"Banco de dados {db_path} apagado."))

        # ==============================
        # Apagar migrações antigas
        # ==============================
        for app in settings.INSTALLED_APPS:
            if app.startswith("django."):
                continue
            migrations_path = os.path.join(settings.BASE_DIR, app, "migrations")
            if os.path.exists(migrations_path):
                for file in os.listdir(migrations_path):
                    if file != "__init__.py" and file.endswith(".py"):
                        os.remove(os.path.join(migrations_path, file))
                self.stdout.write(self.style.WARNING(f"Migrações limpas em {app}."))

        # ==============================
        # Apagar credenciais antigas
        # ==============================
        cred_file = os.path.join(settings.BASE_DIR, "credenciais.txt")
        if os.path.exists(cred_file):
            os.remove(cred_file)
            self.stdout.write(self.style.WARNING("Arquivo credenciais.txt apagado."))

        # ==============================
        # Recriar banco e aplicar migrações
        # ==============================
        call_command("makemigrations")
        call_command("migrate")

        # ==============================
        # Rodar seed
        # ==============================
        call_command("seed")

        self.stdout.write(self.style.SUCCESS("✅ Banco resetado e populado com sucesso!"))
