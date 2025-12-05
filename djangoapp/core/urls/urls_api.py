from django.urls import path, include
from rest_framework.routers import DefaultRouter

from ..views.viewsets import (
    AlunoViewSet,
    CursoViewSet,
    MatriculaViewSet
)

from ..views.views_api import (
    total_de_pagamentos_pendentes,
    total_devido_por_aluno,
    total_pago_por_aluno,
    relatorio_matriculas_por_curso
)

router = DefaultRouter()
router.register("alunos", AlunoViewSet)
router.register("cursos", CursoViewSet)
router.register("matriculas", MatriculaViewSet)

urlpatterns = [
    # Rotas do ViewSet
    path("", include(router.urls)),

    # Rotas de relatórios customizados
    path("relatorios/matriculas-por-curso/", relatorio_matriculas_por_curso),
    path("relatorios/total-devido-aluno/", total_devido_por_aluno),
    path("relatorios/total-pago-aluno/", total_pago_por_aluno),
    path("relatorios/total-pagamentos-pendentes/", total_de_pagamentos_pendentes),
]
