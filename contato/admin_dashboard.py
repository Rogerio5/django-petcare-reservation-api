from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.utils.safestring import mark_safe
import json

from .models import Reserva, Servico, Categoria, Recurso

class CustomAdminSite(admin.AdminSite):
    site_header = "Painel de Gestão"
    site_title = "Administração"
    index_title = "Bem-vindo ao Painel"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("dashboard/", self.admin_view(self.dashboard_view), name="dashboard"),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        # Totais
        total_servicos = Servico.objects.count()
        total_recursos = Recurso.objects.count()
        total_categorias = Categoria.objects.count()
        total_reservas = Reserva.objects.count()

        # Reservas por serviço
        reservas_por_servico = (
            Servico.objects.annotate(total=Count("reservas"))
            .order_by("-total")[:5]
        )
        servicos_labels = [s.nome for s in reservas_por_servico]
        servicos_data = [s.total for s in reservas_por_servico]

        # Reservas por categoria
        reservas_por_categoria = (
            Categoria.objects.annotate(total=Count("reservas"))
            .order_by("-total")[:5]
        )
        categorias_labels = [c.nome for c in reservas_por_categoria]
        categorias_data = [c.total for c in reservas_por_categoria]

        # Reservas por mês
        reservas_por_mes = (
            Reserva.objects.annotate(mes=TruncMonth("data"))
            .values("mes")
            .annotate(total=Count("id"))
            .order_by("mes")
        )
        meses_labels = [r["mes"].strftime("%b/%Y") for r in reservas_por_mes]
        meses_data = [r["total"] for r in reservas_por_mes]

        context = dict(
            self.each_context(request),
            total_servicos=total_servicos,
            total_recursos=total_recursos,
            total_categorias=total_categorias,
            total_reservas=total_reservas,
            servicos_labels=mark_safe(json.dumps(servicos_labels)),
            servicos_data=mark_safe(json.dumps(servicos_data)),
            categorias_labels=mark_safe(json.dumps(categorias_labels)),
            categorias_data=mark_safe(json.dumps(categorias_data)),
            meses_labels=mark_safe(json.dumps(meses_labels)),
            meses_data=mark_safe(json.dumps(meses_data)),
        )
        return TemplateResponse(request, "admin/dashboard_admin.html", context)
