from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count, F
from ..models import Matricula
from ..services import (
    calcular_total_matriculas_por_filtro,
    selecionar_matriculas_por_filtro,
)


@api_view(["GET"])
def total_de_pagamentos_pendentes(request):
    dados = calcular_total_matriculas_por_filtro(Matricula.objects.all(), "pendente")
    return Response(dados)


@api_view(["GET"])
def total_pago_por_aluno(request):
    dados = selecionar_matriculas_por_filtro(Matricula.objects.all(), "pago")
    return Response(dados)


@api_view(["GET"])
def total_devido_por_aluno(request):
    dados = selecionar_matriculas_por_filtro(Matricula.objects.all(), "pendente")
    return Response(dados)


@api_view(["GET"])
def relatorio_matriculas_por_curso(request):
    dados = (Matricula.objects.values(nome_curso=F("curso__nome"))).annotate(
        total_matriculas=Count("id")
    )
    return Response(list(dados))
