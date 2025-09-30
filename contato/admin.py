from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html
from django.urls import reverse, path
from django.utils.translation import gettext_lazy as _
from django.contrib.admin import SimpleListFilter
from django.http import HttpResponse
from django.template.response import TemplateResponse
import csv

from .models import Mensagem, Categoria, Reserva, Servico, Recurso
from . import views


# ==============================
# Action para exportar reservas
# ==============================
def exportar_reservas(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=reservas.csv"
    writer = csv.writer(response)
    writer.writerow(["Pet", "Telefone", "Data", "Categoria", "Serviço"])
    for r in queryset:
        writer.writerow([
            r.nome_pet,
            r.telefone,
            r.data,
            r.categoria.nome if r.categoria else "",
            r.servico.nome if r.servico else ""
        ])
    return response

exportar_reservas.short_description = "Exportar reservas selecionadas para CSV"


# ==============================
# Filtro personalizado por mês
# ==============================
class MesReservaFilter(SimpleListFilter):
    title = _("Mês da Reserva")
    parameter_name = "mes"

    def lookups(self, request, model_admin):
        return [(i, f"Mês {i}") for i in range(1, 13)]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(data__month=self.value())
        return queryset


# ==============================
# Admins
# ==============================
@admin.register(Mensagem)
class MensagemAdmin(admin.ModelAdmin):
    list_display = ("nome", "email", "criado_em")
    search_fields = ("nome", "email")
    list_filter = ("criado_em",)
    list_per_page = 20
    readonly_fields = ("criado_em",)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome", "total_servicos", "total_reservas")
    search_fields = ("nome",)
    ordering = ("nome",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            servicos_count=Count("servicos", distinct=True),
            reservas_count=Count("reservas", distinct=True)
        )

    def total_servicos(self, obj):
        return obj.servicos_count
    total_servicos.short_description = "Qtd. Serviços"

    def total_reservas(self, obj):
        return obj.reservas_count
    total_reservas.short_description = "Qtd. Reservas"


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ("nome_pet", "telefone", "data", "link_categoria", "link_servico", "criado_em")
    search_fields = ("nome_pet", "telefone", "categoria__nome", "servico__nome")
    list_filter = ("data", "criado_em", "categoria", "servico", MesReservaFilter)
    ordering = ("-data",)
    list_per_page = 20
    readonly_fields = ("criado_em",)
    actions = [exportar_reservas]

    fieldsets = (
        ("Informações do Pet", {
            "fields": ("nome_pet", "categoria", "servico")
        }),
        ("Contato", {
            "fields": ("telefone",)
        }),
        ("Agendamento", {
            "fields": ("data", "observacoes")
        }),
        ("Controle do Sistema", {
            "fields": ("criado_em",),
            "classes": ("collapse",)
        }),
    )

    # Links clicáveis
    def link_categoria(self, obj):
        if obj.categoria:
            url = reverse("admin:contato_categoria_change", args=[obj.categoria.id])
            return format_html('<a href="{}">{}</a>', url, obj.categoria.nome)
        return "-"
    link_categoria.short_description = "Categoria"

    def link_servico(self, obj):
        if obj.servico:
            url = reverse("admin:contato_servico_change", args=[obj.servico.id])
            return format_html('<a href="{}">{}</a>', url, obj.servico.nome)
        return "-"
    link_servico.short_description = "Serviço"


@admin.register(Recurso)
class RecursoAdmin(admin.ModelAdmin):
    list_display = ("nome", "total_servicos")
    search_fields = ("nome",)
    ordering = ("nome",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(servicos_count=Count("servicos"))

    def total_servicos(self, obj):
        return obj.servicos_count
    total_servicos.short_description = "Qtd. Serviços"


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ("nome", "link_categoria", "total_reservas", "criado_em", "atualizado_em")
    search_fields = ("nome", "descricao", "categoria__nome")
    list_filter = ("categoria", "criado_em", "atualizado_em")
    ordering = ("-criado_em",)
    filter_horizontal = ("recursos",)
    readonly_fields = ("criado_em", "atualizado_em")

    fieldsets = (
        ("Informações do Serviço", {
            "fields": ("nome", "descricao", "categoria", "recursos")
        }),
        ("Controle do Sistema", {
            "fields": ("criado_em", "atualizado_em"),
            "classes": ("collapse",)
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(reservas_count=Count("reservas"))

    def total_reservas(self, obj):
        return obj.reservas_count
    total_reservas.short_description = "Qtd. Reservas"

    def link_categoria(self, obj):
        if obj.categoria:
            url = reverse("admin:contato_categoria_change", args=[obj.categoria.id])
            return format_html('<a href="{}">{}</a>', url, obj.categoria.nome)
        return "-"
    link_categoria.short_description = "Categoria"


# ==============================
# Custom AdminSite (com Dashboard)
# ==============================
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
        # Reaproveita a lógica da view pública
        response = views.dashboard(request)
        context = getattr(response, "context_data", response.context_data if hasattr(response, "context_data") else {})
        return TemplateResponse(request, "admin/dashboard_admin.html", context)
