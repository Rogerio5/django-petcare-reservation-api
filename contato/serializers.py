from rest_framework import serializers
from .models import Mensagem, Reserva, Categoria, Servico, Recurso


# ==============================
# Serializers básicos
# ==============================
class MensagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mensagem
        fields = ["id", "nome", "email", "mensagem", "criado_em"]


class ReservaSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.CharField(source="categoria.nome", read_only=True)
    servico_nome = serializers.CharField(source="servico.nome", read_only=True)

    class Meta:
        model = Reserva
        fields = [
            "id",
            "nome_pet",
            "telefone",
            "data",
            "observacoes",
            "criado_em",
            "categoria",
            "categoria_nome",
            "servico",
            "servico_nome",
        ]


class RecursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recurso
        fields = ["id", "nome"]


class ServicoSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.CharField(source="categoria.nome", read_only=True)
    recursos = RecursoSerializer(many=True, read_only=True)

    class Meta:
        model = Servico
        fields = [
            "id",
            "nome",
            "descricao",
            "categoria",
            "categoria_nome",
            "recursos",
            "criado_em",
            "atualizado_em",
        ]


class CategoriaSerializer(serializers.ModelSerializer):
    servicos = ServicoSerializer(many=True, read_only=True)

    class Meta:
        model = Categoria
        fields = ["id", "nome", "servicos"]
