import pytest
from datetime import date
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from contato.models import Reserva, Categoria


@pytest.fixture
def api_client():
    """Cria um usuário autenticado para acessar a API"""
    user = User.objects.create_user(username="teste", password="123")
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.mark.django_db
def test_limite_maximo_reservas_por_dia_api(api_client):
    """Não deve permitir criar mais de 4 reservas no mesmo dia via API"""
    categoria = Categoria.objects.create(nome="Banho")
    data_reserva = date.today()

    # Cria 4 reservas válidas
    for i in range(4):
        Reserva.objects.create(
            nome_pet=f"Pet {i}",
            telefone=f"+55119999999{i}",
            data=data_reserva,
            categoria=categoria
        )

    # Tenta criar a 5ª reserva via API
    payload = {
        "nome_pet": "Pet Extra",
        "telefone": "+551199999995",
        "data": str(data_reserva),
        "categoria": categoria.id,
        "observacoes": "Teste de limite via API"
    }
    response = api_client.post("/api/reservas/", payload, format="json")

    # Deve falhar com erro 400 (Bad Request)
    assert response.status_code == 400
    assert "non_field_errors" in response.data
    assert response.data["non_field_errors"][0] == "Não é possível agendar mais de 4 reservas para este dia."
