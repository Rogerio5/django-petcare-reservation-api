from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Namespace do app
app_name = "contato"

# -------------------------------
# Router para API de Categorias
# -------------------------------
router = DefaultRouter()
router.register(r'categorias', views.CategoriaViewSet, basename='categoria')

urlpatterns = [
    # -------------------------------
    # Rotas HTML (templates)
    # -------------------------------
    path("", views.home, name="home"),
    path("contato/", views.contato_view, name="contato"),
    path("reserva/", views.reserva_view, name="reserva"),
    path("mensagem/nova/", views.mensagem_create, name="mensagem_create"),
    path("servicos/", views.lista_servicos, name="lista_servicos"),
    path("recursos/", views.lista_recursos, name="lista_recursos"),
    path("dashboard/", views.dashboard, name="dashboard"),  # Dashboard público

    # -------------------------------
    # Rotas API - Mensagens
    # -------------------------------
    path("api/mensagens/", views.ContatoListCreate.as_view(), name="mensagem-list"),
    path("api/mensagens/<int:pk>/", views.ContatoRetrieveUpdateDestroy.as_view(), name="mensagem-detail"),

    # -------------------------------
    # Rotas API - Reservas
    # -------------------------------
    path("api/reservas/", views.ReservaListCreate.as_view(), name="reserva-list"),
    path("api/reservas/<int:pk>/", views.ReservaRetrieveUpdateDestroy.as_view(), name="reserva-detail"),

    # -------------------------------
    # Rotas API - Categorias (via Router)
    # -------------------------------
    path("api/", include(router.urls)),
]

