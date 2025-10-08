import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from contato.models import Categoria, Servico, Reserva
from datetime import date


@pytest.fixture
def api_client():
    """Client autenticado"""
    user = User.objects.create_user(username="teste", password="123")
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.mark.django_db
def test_criar_reserva_sem_autenticacao():
    """Usuário não autenticado deve receber 401"""
    client = APIClient()  # sem autenticação
    cat = Categoria.objects.create(nome="Banho")
    serv = Servico.objects.create(nome="Banho e Tosa", categoria=cat)

    payload = {
        "nome_pet": "Rex",
        "telefone": "+5511999999999",
        "data": str(date.today()),
        "categoria": cat.id,
        "servico": serv.id,
    }

    response = client.post("/api/reservas/", payload, format="json")
    assert response.status_code == 401


@pytest.mark.django_db
def test_criar_reserva_com_autenticacao(api_client):
    """Usuário autenticado deve conseguir criar reserva"""
    cat = Categoria.objects.create(nome="Banho")
    serv = Servico.objects.create(nome="Banho e Tosa", categoria=cat)

    payload = {
        "nome_pet": "Rex",
        "telefone": "+5511999999999",
        "data": str(date.today()),
        "categoria": cat.id,
        "servico": serv.id,
    }

    response = api_client.post("/api/reservas/", payload, format="json")
    assert response.status_code in (200, 201)
    assert Reserva.objects.count() == 1
