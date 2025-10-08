import pytest
from datetime import date
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from contato.models import Categoria, Servico, Reserva


@pytest.fixture
def api_client():
    user = User.objects.create_user(username="teste", password="123")
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def categoria():
    return Categoria.objects.create(nome="Banho")


@pytest.fixture
def servico(categoria):
    return Servico.objects.create(nome="Banho e Tosa", categoria=categoria)


@pytest.fixture
def reserva(categoria, servico):
    return Reserva.objects.create(
        nome_pet="Rex",
        telefone="+551199999999",
        data=date.today(),
        categoria=categoria,
        servico=servico,
        observacoes="Reserva de teste"
    )


@pytest.mark.django_db
def test_criar_categoria(api_client):
    payload = {"nome": "Tosa"}
    response = api_client.post("/api/categorias/", payload, format="json")
    assert response.status_code == 201
    assert Categoria.objects.count() == 1


@pytest.mark.django_db
def test_listar_categorias(api_client, categoria):
    response = api_client.get("/api/categorias/")
    assert response.status_code == 200
    assert response.data["count"] >= 1
    assert response.data["results"][0]["nome"] == "Banho"


@pytest.mark.django_db
def test_detalhe_categoria(api_client, categoria):
    response = api_client.get(f"/api/categorias/{categoria.id}/")
    assert response.status_code == 200
    assert response.data["id"] == categoria.id


@pytest.mark.django_db
def test_atualizar_categoria(api_client, categoria):
    payload = {"nome": "Banho Atualizado"}
    response = api_client.put(f"/api/categorias/{categoria.id}/", payload, format="json")
    assert response.status_code == 200
    categoria.refresh_from_db()
    assert categoria.nome == "Banho Atualizado"


@pytest.mark.django_db
def test_remover_categoria(api_client, categoria):
    response = api_client.delete(f"/api/categorias/{categoria.id}/")
    assert response.status_code == 204
    assert not Categoria.objects.filter(id=categoria.id).exists()


@pytest.mark.django_db
def test_listar_reservas_de_categoria(api_client, categoria, reserva):
    response = api_client.get(f"/api/categorias/{categoria.id}/reservas/")
    assert response.status_code == 200
    # se endpoint for paginado:
    if "results" in response.data:
        assert response.data["results"][0]["nome_pet"] == "Rex"
    else:
        assert response.data[0]["nome_pet"] == "Rex"
