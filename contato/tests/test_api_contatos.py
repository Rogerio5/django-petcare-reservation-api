import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from contato.models import Mensagem


@pytest.fixture
def api_client():
    """Cria um usuário e retorna um client autenticado"""
    user = User.objects.create_user(username="teste", password="123")
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.mark.django_db
def test_listar_contatos(api_client):
    """Deve listar mensagens já existentes"""
    Mensagem.objects.create(nome="Rogerio", email="teste@teste.com", mensagem="Olá!")
    response = api_client.get("/api/contatos/")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 1
    assert data["results"][0]["nome"] == "Rogerio"
    assert data["results"][0]["email"] == "teste@teste.com"


@pytest.mark.django_db
def test_criar_contato(api_client):
    """Deve criar uma nova mensagem via API"""
    payload = {
        "nome": "Maria",
        "email": "maria@teste.com",
        "mensagem": "Preciso de informações"
    }
    response = api_client.post("/api/contatos/", payload, format="json")
    assert response.status_code in (200, 201)
    assert Mensagem.objects.count() == 1
    msg = Mensagem.objects.first()
    assert msg.nome == "Maria"
    assert msg.email == "maria@teste.com"
    assert msg.mensagem == "Preciso de informações"
