import pytest
from contato.models import Mensagem, Categoria, Reserva, Servico, Recurso
from datetime import date


# -----------------------------
# Mensagem
# -----------------------------
@pytest.mark.django_db
def test_mensagem_str():
    msg = Mensagem.objects.create(
        nome="Rogerio",
        email="teste@teste.com",
        mensagem="Olá!"
    )
    assert "Rogerio" in str(msg)
    assert "teste@teste.com" in str(msg)


# -----------------------------
# Categoria
# -----------------------------
@pytest.mark.django_db
def test_categoria_str():
    cat = Categoria.objects.create(nome="Tosa")
    assert str(cat) == "Tosa"


# -----------------------------
# Reserva
# -----------------------------
@pytest.mark.django_db
def test_criacao_reserva():
    categoria = Categoria.objects.create(nome="Banho")
    reserva = Reserva.objects.create(
        nome_pet="Rex",
        telefone="+5511999999999",
        data=date.today(),
        categoria=categoria
    )
    assert reserva.nome_pet == "Rex"
    assert reserva.categoria.nome == "Banho"
    # __str__ deve incluir nome do pet e categoria
    assert "Rex" in str(reserva)
    assert "Banho" in str(reserva)


# -----------------------------
# Recurso
# -----------------------------
@pytest.mark.django_db
def test_recurso_str():
    rec = Recurso.objects.create(nome="Secador")
    assert str(rec) == "Secador"


# -----------------------------
# Servico
# -----------------------------
@pytest.mark.django_db
def test_servico_helpers():
    cat = Categoria.objects.create(nome="Banho")
    rec1 = Recurso.objects.create(nome="Shampoo")
    rec2 = Recurso.objects.create(nome="Toalha")
    serv = Servico.objects.create(nome="Banho Completo", categoria=cat)
    serv.recursos.add(rec1, rec2)

    # __str__
    assert str(serv) == "Banho Completo"
    # get_categoria
    assert serv.get_categoria() == "Banho"
    # get_recursos
    recursos = serv.get_recursos()
    assert "Shampoo" in recursos
    assert "Toalha" in recursos
