from django.db import models
from django.core.validators import RegexValidator


class Mensagem(models.Model):
    nome = models.CharField("Nome", max_length=100)
    email = models.EmailField("E-mail")
    mensagem = models.TextField("Mensagem")
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)

    class Meta:
        verbose_name = "Mensagem"
        verbose_name_plural = "Mensagens"
        ordering = ["-criado_em"]

    def __str__(self):
        return f"{self.nome} ({self.email})"


class Categoria(models.Model):
    nome = models.CharField(
        "Categoria",
        max_length=100,
        unique=True,
        help_text="Nome único da categoria (ex.: Banho, Tosa, Hospedagem).",
    )

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Recurso(models.Model):
    nome = models.CharField(
        "Nome",
        max_length=100,
        help_text="Nome do recurso ou estrutura (ex.: Canil, Consultório, Secador).",
    )

    class Meta:
        verbose_name = "Recurso"
        verbose_name_plural = "Recursos"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Servico(models.Model):
    nome = models.CharField("Nome", max_length=100)
    descricao = models.TextField("Descrição", blank=True)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="servicos",
        verbose_name="Categoria",
        help_text="Categoria à qual o serviço pertence.",
    )
    recursos = models.ManyToManyField(
        Recurso,
        blank=True,
        related_name="servicos",
        verbose_name="Recursos",
        help_text="Recursos necessários para este serviço.",
    )
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)
    atualizado_em = models.DateTimeField("Atualizado em", auto_now=True)

    class Meta:
        verbose_name = "Serviço"
        verbose_name_plural = "Serviços"
        ordering = ["-criado_em"]
        indexes = [
            models.Index(fields=["nome"]),
            models.Index(fields=["-criado_em"]),
        ]

    def __str__(self):
        return self.nome

    def get_categoria(self):
        return self.categoria.nome

    def get_recursos(self):
        return ", ".join(r.nome for r in self.recursos.all())


class Reserva(models.Model):
    nome_pet = models.CharField(
        "Nome do Pet",
        max_length=100,
        help_text="Informe o nome do animal de estimação."
    )
    telefone = models.CharField(
        "Telefone",
        max_length=20,
        validators=[RegexValidator(r"^\+?\d{8,15}$", "Informe um telefone válido.")],
        help_text="Exemplo: +5511999999999"
    )
    data = models.DateField(
        "Data da Reserva",
        help_text="Selecione a data desejada para a reserva."
    )
    observacoes = models.TextField(
        "Observações",
        blank=True,
        null=True,
        help_text="Informações adicionais sobre a reserva (opcional)."
    )
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name="reservas",
        null=True,
        blank=True,
        verbose_name="Categoria",
        help_text="Selecione a categoria do serviço."
    )

    servico = models.ForeignKey(
        Servico,
        on_delete=models.PROTECT,
        related_name="reservas",
        verbose_name="Serviço",
        help_text="Selecione o serviço desejado."
    )

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        ordering = ["-data"]
        get_latest_by = "data"
        indexes = [
            models.Index(fields=["data"]),
            models.Index(fields=["telefone"]),
        ]

    def __str__(self):
        return f"{self.nome_pet} - {self.servico.nome} em {self.data}"
