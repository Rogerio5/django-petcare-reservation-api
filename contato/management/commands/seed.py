import secrets
import string
import random
from datetime import timedelta, date
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from contato.models import Categoria, Servico, Recurso, Reserva


def gerar_senha(tamanho=10):
    """Gera uma senha aleatória segura"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(tamanho))


class Command(BaseCommand):
    help = "Popula o banco com dados iniciais (categorias, serviços, recursos, usuários admin e reservas de exemplo)"

    def handle(self, *args, **kwargs):
        # ==============================
        # Categorias
        # ==============================
        categorias = {
            "Banho & Tosa": ["Banho", "Tosa"],
            "Veterinário": ["Consulta Veterinária"],
            "Hotelzinho": ["Hospedagem"],
            "Adestramento": []
        }

        categoria_objs = {}
        for nome in categorias.keys():
            cat, _ = Categoria.objects.get_or_create(nome=nome)
            categoria_objs[nome] = cat
        self.stdout.write(self.style.SUCCESS("Categorias criadas."))

        # ==============================
        # Serviços
        # ==============================
        servicos = {
            "Banho": ("Banho completo para pets", "Banho & Tosa"),
            "Tosa": ("Tosa higiênica e estilizada", "Banho & Tosa"),
            "Consulta Veterinária": ("Atendimento clínico geral", "Veterinário"),
            "Hospedagem": ("Hotelzinho para pets", "Hotelzinho"),
        }

        servico_objs = {}
        for nome, (desc, cat_nome) in servicos.items():
            obj, _ = Servico.objects.get_or_create(
                nome=nome,
                descricao=desc,
                categoria=categoria_objs[cat_nome]
            )
            servico_objs[nome] = obj
        self.stdout.write(self.style.SUCCESS("Serviços criados."))

        # ==============================
        # Recursos
        # ==============================
        recursos = ["Sala de Banho", "Sala de Tosa", "Consultório", "Canil", "Playground"]
        for nome in recursos:
            Recurso.objects.get_or_create(nome=nome)
        self.stdout.write(self.style.SUCCESS("Recursos criados."))

        # ==============================
        # Arquivo de credenciais
        # ==============================
        cred_file = "credenciais.txt"
        with open(cred_file, "a", encoding="utf-8") as f:

            # Usuário admin genérico
            if not User.objects.filter(username="admin").exists():
                senha_admin = gerar_senha()
                User.objects.create_superuser(
                    username="admin",
                    email="admin@example.com",
                    password=senha_admin
                )
                msg = f"Usuário admin criado (login: admin / senha: {senha_admin})"
                self.stdout.write(self.style.SUCCESS(msg))
                f.write(msg + "\n")
            else:
                self.stdout.write(self.style.WARNING("Usuário admin já existe."))

            # Usuário admin personalizado (Rogerio)
            if not User.objects.filter(username="Rogerio").exists():
                senha_rogerio = gerar_senha()
                User.objects.create_superuser(
                    username="Rogerio",
                    email="rogerio@example.com",  # 👈 troque para seu email real
                    password=senha_rogerio
                )
                msg = f"Usuário Rogerio criado (login: Rogerio / senha: {senha_rogerio})"
                self.stdout.write(self.style.SUCCESS(msg))
                f.write(msg + "\n")
            else:
                self.stdout.write(self.style.WARNING("Usuário Rogerio já existe."))

        # ==============================
        # Reservas de exemplo
        # ==============================
        hoje = date.today()
        for i in range(10):
            data_reserva = hoje + timedelta(days=random.randint(-10, 10))
            servico = random.choice(list(servico_objs.values()))
            Reserva.objects.get_or_create(
                nome_pet=f"Pet {i+1}",
                telefone=f"(11) 9{random.randint(1000,9999)}-{random.randint(1000,9999)}",
                categoria=servico.categoria,
                servico=servico,
                data=data_reserva,
                observacoes="Reserva de teste gerada automaticamente"
            )
        self.stdout.write(self.style.SUCCESS("Reservas de exemplo criadas."))

        # ==============================
        # Finalização
        # ==============================
        self.stdout.write(self.style.SUCCESS("✅ Banco populado com sucesso!"))
        self.stdout.write(self.style.SUCCESS(f"🔑 Credenciais salvas em {cred_file}"))
