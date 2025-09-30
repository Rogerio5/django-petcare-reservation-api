"""
URL configuration for contato_django project.

O `urlpatterns` define as rotas principais do projeto.
"""

from django.urls import path, include
from contato.admin import CustomAdminSite
from contato import admin as contato_admin

# ==============================
# Instância do Admin customizado
# ==============================
admin_site = CustomAdminSite(name="custom_admin")

# Registra os modelos no novo admin
# (importados de contato/admin.py, onde já estão configurados)
admin_site.register(contato_admin.Mensagem)
admin_site.register(contato_admin.Categoria)
admin_site.register(contato_admin.Servico)
admin_site.register(contato_admin.Recurso)
admin_site.register(contato_admin.Reserva)

# ==============================
# Rotas principais
# ==============================
urlpatterns = [
    path("admin/", admin_site.urls),   # Admin customizado
    path("", include("contato.urls")), # Rotas públicas do app contato
]

