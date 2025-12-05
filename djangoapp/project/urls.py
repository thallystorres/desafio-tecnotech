"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views.viewsets import AlunoViewSet, CursoViewSet, MatriculaViewSet
from core.views.views_html import historico_aluno
from core.views.views_api import (
    total_de_pagamentos_pendentes,
    total_pago_por_aluno,
    total_devido_por_aluno,
    relatorio_matriculas_por_curso,
)

router = DefaultRouter()
router.register("alunos", AlunoViewSet)
router.register("cursos", CursoViewSet)
router.register("matriculas", MatriculaViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("aluno/<int:aluno_id>/historico/", historico_aluno, name="historico_aluno"),
    path("api/", include(router.urls)),
    path("api/relatorios/matriculas-por-curso/", relatorio_matriculas_por_curso),
    path("api/relatorios/total-devido-aluno/", total_devido_por_aluno),
    path("api/relatorios/total-pago-aluno/", total_pago_por_aluno),
    path("api/relatorios/total-pagamentos-pendentes/", total_de_pagamentos_pendentes),
]
