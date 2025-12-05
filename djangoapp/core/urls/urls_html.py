from django.urls import path
from ..views.views_html import historico_aluno

urlpatterns = [
    path("aluno/<int:aluno_id>/historico/", historico_aluno, name="historico_aluno"),
]
