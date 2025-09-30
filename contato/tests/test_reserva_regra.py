import pytest
from datetime import date
from contato.models import Reserva, Categoria
from contato.forms import ReservaForm

@pytest.mark.django_db
def test_limite_maximo_reservas_por_dia():
    """Não deve permitir mais de 4 reservas no mesmo dia"""
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

    # Tenta criar a 5ª reserva no mesmo dia via formulário
    form = ReservaForm(data={
        "nome_pet": "Pet Extra",
        "telefone": "+551199999995",
        "data": data_reserva,
        "categoria": categoria.id,
        "observacoes": "Teste de limite"
    })

    assert not form.is_valid()
    assert "data" in form.errors
    assert "não é possível agendar mais de 4 reservas" in str(form.errors["data"])
