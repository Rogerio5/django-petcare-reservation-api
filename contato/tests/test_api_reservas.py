import pytest
from datetime import date
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from contato.models import Reserva, Categoria, Servico


# -------------------------------
# FIXTURES
# -------------------------------

@pytest.fixture
def api_client():
    """Cria um usuário autenticado para acessar a API"""
    user = User.objects.create_user(username="teste", password="123")
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def categoria():
    """Cria uma categoria padrão"""
    return Categoria.objects.create(nome="Banho")


@pytest.fixture
def servico(categoria):
    """Cria um serviço padrão vinculado a uma categoria"""
    return Servico.objects.create(nome="Banho e Tosa", categoria=categoria)


@pytest.fixture
def reserva(categoria, servico):
    """Cria uma reserva inicial"""
    return Reserva.objects.create(
        nome_pet="Rex",
        telefone="+551199999999",
        data=date.today(),
        categoria=categoria,
        servico=servico,
        observacoes="Primeira reserva"
    )


# -------------------------------
# CRUD DE RESERVAS
# -------------------------------

@pytest.mark.django_db
def test_criar_reserva(api_client, categoria, servico):
    """Deve criar uma reserva com sucesso"""
    payload = {
        "nome_pet": "Bidu",
        "telefone": "+551199999998",
        "data": str(date.today()),
        "categoria": categoria.id,
        "servico": servico.id,
        "observacoes": "Banho simples"
    }
    response = api_client.post("/api/reservas/", payload, format="json")
    assert response.status_code == 201
    assert Reserva.objects.count() == 1
    assert Reserva.objects.first().nome_pet == "Bidu"


@pytest.mark.django_db
def test_listar_reservas(api_client, reserva):
    """Deve listar reservas existentes (com paginação)"""
    response = api_client.get("/api/reservas/")
    assert response.status_code == 200
    assert response.data["count"] >= 1
    assert response.data["results"][0]["nome_pet"] == "Rex"


@pytest.mark.django_db
def test_detalhe_reserva(api_client, reserva):
    """Deve retornar os detalhes de uma reserva específica"""
    response = api_client.get(f"/api/reservas/{reserva.id}/")
    assert response.status_code == 200
    assert response.data["id"] == reserva.id
    assert response.data["nome_pet"] == "Rex"


@pytest.mark.django_db
def test_atualizar_reserva(api_client, reserva, categoria, servico):
    """Deve atualizar uma reserva existente"""
    payload = {
        "nome_pet": "Rex Atualizado",
        "telefone": reserva.telefone,
        "data": str(reserva.data),
        "categoria": categoria.id,
        "servico": servico.id,
        "observacoes": "Atualização de teste"
    }
    response = api_client.put(f"/api/reservas/{reserva.id}/", payload, format="json")
    assert response.status_code == 200
    reserva.refresh_from_db()
    assert reserva.nome_pet == "Rex Atualizado"


@pytest.mark.django_db
def test_remover_reserva(api_client, reserva):
    """Deve remover uma reserva existente"""
    response = api_client.delete(f"/api/reservas/{reserva.id}/")
    assert response.status_code == 204
    assert not Reserva.objects.filter(id=reserva.id).exists()


# -------------------------------
# REGRA DE NEGÓCIO
# -------------------------------

@pytest.mark.django_db
def test_limite_maximo_reservas_por_dia(api_client, categoria, servico):
    """Não deve permitir criar mais de 4 reservas no mesmo dia"""
    data_reserva = date.today()

    # Cria 4 reservas válidas
    for i in range(4):
        Reserva.objects.create(
            nome_pet=f"Pet {i}",
            telefone=f"+55119999999{i}",
            data=data_reserva,
            categoria=categoria,
            servico=servico
        )

    # Tenta criar a 5ª reserva via API
    payload = {
        "nome_pet": "Pet Extra",
        "telefone": "+551199999995",
        "data": str(data_reserva),
        "categoria": categoria.id,
        "servico": servico.id,
        "observacoes": "Teste de limite via API"
    }
    response = api_client.post("/api/reservas/", payload, format="json")

    # Deve falhar com erro 400 (Bad Request)
    assert response.status_code == 400
    assert "non_field_errors" in response.data
    assert response.data["non_field_errors"][0] == "Não é possível agendar mais de 4 reservas para este dia."
