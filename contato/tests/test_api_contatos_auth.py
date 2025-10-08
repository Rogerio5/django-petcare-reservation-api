import pytest
from django.urls import reverse
from contato.models import Mensagem, Reserva, Categoria, Servico
from datetime import date


@pytest.mark.django_db
def test_homepage_status(client):
    url = reverse("home")
    response = client.get(url)
    assert response.status_code == 200


# -----------------------------
# Mensagem
# -----------------------------
@pytest.mark.django_db
def test_envio_mensagem_valida(client):
    url = reverse("mensagem_create")
    data = {"nome": "Rogerio", "email": "teste@teste.com", "mensagem": "Olá!"}
    response = client.post(url, data)
    assert response.status_code in (301, 302)
    assert Mensagem.objects.count() == 1


@pytest.mark.django_db
def test_envio_mensagem_invalida(client):
    url = reverse("mensagem_create")
    data = {"nome": "", "email": "email_invalido", "mensagem": ""}
    response = client.post(url, data)
    assert response.status_code == 200
    assert not response.context["form"].is_valid()
    assert Mensagem.objects.count() == 0


# -----------------------------
# Reserva
# -----------------------------
@pytest.mark.django_db
def test_envio_reserva_valida(client):
    categoria = Categoria.objects.create(nome="Banho")
    servico = Servico.objects.create(nome="Banho e Tosa", categoria=categoria)
    url = reverse("reserva")
    data = {
        "nome_pet": "Rex",
        "telefone": "+5511999999999",
        "data": str(date.today()),
        "categoria": categoria.id,
        "servico": servico.id,
    }
    response = client.post(url, data)
    assert response.status_code in (301, 302)
    assert Reserva.objects.count() == 1


@pytest.mark.django_db
def test_envio_reserva_invalida(client):
    categoria = Categoria.objects.create(nome="Banho")
    servico = Servico.objects.create(nome="Banho e Tosa", categoria=categoria)
    url = reverse("reserva")
    data = {"nome_pet": "", "telefone": "", "data": "", "categoria": categoria.id, "servico": servico.id}
    response = client.post(url, data)
    assert response.status_code == 200
    assert not response.context["form"].is_valid()
    assert Reserva.objects.count() == 0
