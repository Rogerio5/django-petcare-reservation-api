from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Count
from django.contrib import messages

from rest_framework import generics, viewsets

from .models import Mensagem, Categoria, Reserva, Servico, Recurso
from .serializers import MensagemSerializer, ReservaSerializer, CategoriaSerializer


# ==============================
# Páginas HTML
# ==============================
def home(request):
    return render(request, "home.html")


def contato_view(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        email = request.POST.get("email")
        mensagem_texto = request.POST.get("mensagem")

        if nome and email and mensagem_texto:
            Mensagem.objects.create(nome=nome, email=email, mensagem=mensagem_texto)
            messages.success(request, "Mensagem enviada com sucesso!")
            return redirect("contato:contato")
        else:
            messages.error(request, "Preencha todos os campos.")

    return render(request, "contato.html")


def reserva_view(request):
    if request.method == "POST":
        nome_pet = request.POST.get("nome_pet")
        telefone = request.POST.get("telefone")
        data = request.POST.get("data")
        categoria_id = request.POST.get("categoria")
        servico_id = request.POST.get("servico")
        observacoes = request.POST.get("observacoes")

        if nome_pet and telefone and data and servico_id:
            categoria = Categoria.objects.filter(id=categoria_id).first()
            servico = Servico.objects.get(id=servico_id)
            Reserva.objects.create(
                nome_pet=nome_pet,
                telefone=telefone,
                data=data,
                categoria=categoria,
                servico=servico,
                observacoes=observacoes,
            )
            messages.success(request, "Reserva realizada com sucesso!")
            return redirect("contato:reserva")
        else:
            messages.error(request, "Preencha todos os campos obrigatórios.")

    categorias = Categoria.objects.all()
    servicos = Servico.objects.all()
    return render(request, "reserva.html", {"categorias": categorias, "servicos": servicos})


def mensagem_create(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        email = request.POST.get("email")
        mensagem_texto = request.POST.get("mensagem")

        if nome and email and mensagem_texto:
            Mensagem.objects.create(nome=nome, email=email, mensagem=mensagem_texto)
            messages.success(request, "Mensagem enviada com sucesso!")
            return redirect("contato:mensagem_create")
        else:
            messages.error(request, "Preencha todos os campos.")

    return render(request, "mensagem_form.html")


def lista_servicos(request):
    servicos = Servico.objects.prefetch_related("recursos").all()
    return render(request, "servicos.html", {"servicos": servicos})


def lista_recursos(request):
    recursos = Recurso.objects.prefetch_related("servicos").all()
    return render(request, "recursos.html", {"recursos": recursos})


# ==============================
# Dashboard Público
# ==============================
def dashboard(request):
    total_servicos = Servico.objects.count()
    total_recursos = Recurso.objects.count()
    total_categorias = Categoria.objects.count()
    total_reservas = Reserva.objects.count()

    reservas_por_servico = (
        Servico.objects.annotate(total=Count("reservas"))
        .values("nome", "total")
        .order_by("-total")
    )
    servicos_labels = [s["nome"] for s in reservas_por_servico]
    servicos_data = [s["total"] for s in reservas_por_servico]

    reservas_por_categoria = (
        Categoria.objects.annotate(total=Count("reservas"))
        .values("nome", "total")
        .order_by("-total")
    )
    categorias_labels = [c["nome"] for c in reservas_por_categoria]
    categorias_data = [c["total"] for c in reservas_por_categoria]

    reservas_por_mes = (
        Reserva.objects.values("data__month")
        .annotate(total=Count("id"))
        .order_by("data__month")
    )
    meses_labels = [f"Mês {r['data__month']}" for r in reservas_por_mes]
    meses_data = [r["total"] for r in reservas_por_mes]

    context = {
        "total_servicos": total_servicos,
        "total_recursos": total_recursos,
        "total_categorias": total_categorias,
        "total_reservas": total_reservas,
        "servicos_labels": servicos_labels,
        "servicos_data": servicos_data,
        "categorias_labels": categorias_labels,
        "categorias_data": categorias_data,
        "meses_labels": meses_labels,
        "meses_data": meses_data,
    }
    return render(request, "dashboard.html", context)


# ==============================
# Dashboard Admin
# ==============================
def dashboard_admin(request):
    # Reaproveita a mesma lógica do público
    context = dashboard(request).context_data if hasattr(dashboard(request), "context_data") else dashboard(request).context_data
    return render(request, "admin/dashboard_admin.html", context)


# ==============================
# APIs (Django REST Framework)
# ==============================
class ContatoListCreate(generics.ListCreateAPIView):
    queryset = Mensagem.objects.all()
    serializer_class = MensagemSerializer


class ContatoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Mensagem.objects.all()
    serializer_class = MensagemSerializer


class ReservaListCreate(generics.ListCreateAPIView):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer


class ReservaRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
