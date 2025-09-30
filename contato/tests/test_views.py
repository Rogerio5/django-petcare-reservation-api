import pytest
from django.urls import reverse
from contato.models import Mensagem, Reserva, Categoria
from datetime import date


@pytest.mark.django_db
def test_homepage_status(client):
    """A homepage deve responder com status 200"""
    url = reverse("home")
    response = client.get(url)
    assert response.status_code == 200


# -----------------------------
# Mensagem
# -----------------------------
@pytest.mark.django_db
def test_envio_mensagem_valida(client):
    """Formulário de mensagem válido deve salvar e redirecionar"""
    url = reverse("mensagem_create")
    data = {"nome": "Rogerio", "email": "teste@teste.com", "mensagem": "Olá!"}
    response = client.post(url, data)
    assert response.status_code in (301, 302)
    assert Mensagem.objects.count() == 1
    msg = Mensagem.objects.first()
    assert msg.nome == "Rogerio"
    assert msg.email == "teste@teste.com"
    assert msg.mensagem == "Olá!"


@pytest.mark.django_db
def test_envio_mensagem_invalida(client):
    """Formulário de mensagem inválido deve reexibir a página"""
    url = reverse("mensagem_create")
    data = {"nome": "", "email": "email_invalido", "mensagem": ""}
    response = client.post(url, data)
    assert response.status_code == 200
    assert "form" in response.context
    assert not response.context["form"].is_valid()
    assert Mensagem.objects.count() == 0


@pytest.mark.django_db
def test_mensagem_get(client):
    """GET em mensagem_create deve exibir o formulário vazio"""
    url = reverse("mensagem_create")
    response = client.get(url)
    assert response.status_code == 200
    assert "form" in response.context


# -----------------------------
# Reserva
# -----------------------------
@pytest.mark.django_db
def test_envio_reserva_valida(client):
    """Formulário de reserva válido deve salvar e redirecionar"""
    categoria = Categoria.objects.create(nome="Banho")
    url = reverse("reserva")
    data = {
        "nome_pet": "Rex",
        "telefone": "+5511999999999",
        "data": str(date.today()),
        "categoria": categoria.id,
    }
    response = client.post(url, data)
    assert response.status_code in (301, 302)
    assert Reserva.objects.count() == 1
    reserva = Reserva.objects.first()
    assert reserva.nome_pet == "Rex"
    assert reserva.telefone == "+5511999999999"
    assert reserva.categoria == categoria


@pytest.mark.django_db
def test_envio_reserva_invalida(client):
    """Formulário de reserva inválido deve reexibir a página"""
    categoria = Categoria.objects.create(nome="Banho")
    url = reverse("reserva")
    data = {"nome_pet": "", "telefone": "", "data": "", "categoria": categoria.id}
    response = client.post(url, data)
    assert response.status_code == 200
    assert "form" in response.context
    assert not response.context["form"].is_valid()
    assert Reserva.objects.count() == 0


@pytest.mark.django_db
def test_reserva_get(client):
    """GET em reserva_view deve exibir o formulário vazio"""
    url = reverse("reserva")
    response = client.get(url)
    assert response.status_code == 200
    assert "form" in response.context
