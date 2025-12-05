from django.urls import path
from ..views.views_html import historico_aluno, dashboard

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("aluno/<int:aluno_id>/historico/", historico_aluno, name="historico_aluno"),
]
