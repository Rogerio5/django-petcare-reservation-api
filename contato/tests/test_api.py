import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from contato.models import Categoria, Servico, Reserva
from datetime import date


@pytest.fixture
def api_client():
    user = User.objects.create_user(username="teste", password="123")
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.mark.django_db
def test_listar_categorias(api_client):
    Categoria.objects.create(nome="Banho")
    response = api_client.get("/api/categorias/")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 1
    assert data["results"][0]["nome"] == "Banho"


@pytest.mark.django_db
def test_criar_reserva(api_client):
    cat = Categoria.objects.create(nome="Banho")
    serv = Servico.objects.create(nome="Banho e Tosa", categoria=cat)
    data = {
        "nome_pet": "Rex",
        "telefone": "+5511999999999",
        "data": str(date.today()),
        "categoria": cat.id,
        "servico": serv.id,
    }
    response = api_client.post("/api/reservas/", data, format="json")
    assert response.status_code in (200, 201)
    assert Reserva.objects.count() == 1
