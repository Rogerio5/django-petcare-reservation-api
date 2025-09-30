import pytest
from contato.forms import MensagemForm, ReservaForm
from contato.models import Categoria
from datetime import date

@pytest.mark.django_db
def test_mensagem_form_valido():
    """Formulário de mensagem deve ser válido com dados corretos"""
    form = MensagemForm(data={
        "nome": "Rogerio",
        "email": "teste@teste.com",
        "mensagem": "Olá, tudo bem?"
    })
    assert form.is_valid()


@pytest.mark.django_db
def test_mensagem_form_invalido():
    """Formulário de mensagem deve ser inválido sem email"""
    form = MensagemForm(data={
        "nome": "Rogerio",
        "email": "",  # faltando email
        "mensagem": "Mensagem sem email"
    })
    assert not form.is_valid()
    assert "email" in form.errors


@pytest.mark.django_db
def test_reserva_form_valido():
    """Formulário de reserva deve ser válido com dados corretos"""
    categoria = Categoria.objects.create(nome="Banho")
    form = ReservaForm(data={
        "nome_pet": "Rex",
        "telefone": "+5511999999999",
        "data": date.today(),
        "categoria": categoria.id
    })
    assert form.is_valid()


@pytest.mark.django_db
def test_reserva_form_invalido():
    """Formulário de reserva deve ser inválido sem nome do pet"""
    categoria = Categoria.objects.create(nome="Banho")
    form = ReservaForm(data={
        "nome_pet": "",  # faltando nome
        "telefone": "+5511999999999",
        "data": date.today(),
        "categoria": categoria.id
    })
    assert not form.is_valid()
    assert "nome_pet" in form.errors
