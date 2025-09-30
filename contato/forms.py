from django import forms
from .models import Mensagem, Reserva


class MensagemForm(forms.ModelForm):
    """Formulário baseado no model Mensagem"""

    class Meta:
        model = Mensagem
        fields = ["nome", "email", "mensagem"]
        widgets = {
            "nome": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Digite seu nome"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Digite seu e-mail"}
            ),
            "mensagem": forms.Textarea(
                attrs={"rows": 4, "class": "form-control", "placeholder": "Escreva sua mensagem"}
            ),
        }


class ReservaForm(forms.ModelForm):
    """Formulário baseado no model Reserva, com validação de limite diário"""

    class Meta:
        model = Reserva
        fields = ["nome_pet", "telefone", "data", "categoria", "servico", "observacoes"]
        widgets = {
            "nome_pet": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Digite o nome do pet"}
            ),
            "telefone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "(xx) xxxxx-xxxx"}
            ),
            "data": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "categoria": forms.Select(
                attrs={"class": "form-control"}
            ),
            "servico": forms.Select(
                attrs={"class": "form-control"}
            ),
            "observacoes": forms.Textarea(
                attrs={"rows": 3, "class": "form-control", "placeholder": "Alguma observação?"}
            ),
        }

    def clean_data(self):
        """Valida se já existem 4 reservas no mesmo dia"""
        data = self.cleaned_data.get("data")
        if data:
            reservas_no_dia = Reserva.objects.filter(data=data).count()
            if reservas_no_dia >= 4:
                raise forms.ValidationError(
                    "Limite atingido: não é possível agendar mais de 4 reservas para este dia."
                )
        return data
