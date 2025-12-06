from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count, F
from django.db import connection
from ..models import Matricula
from ..services import MatriculaService


@api_view(["GET"])
def total_de_pagamentos_pendentes(request):
    dados = MatriculaService.calcular_total_por_status(Matricula.objects.all(), "pendente")
    return Response(dados)


@api_view(["GET"])
def total_pago_por_aluno(request):
    dados = MatriculaService.listar_matriculas_por_status(Matricula.objects.all(), "pago")
    return Response(dados)


@api_view(["GET"])
def total_devido_por_aluno(request):
    query = """
        SELECT
            a.id,
            a.nome as aluno,
            COALESCE(SUM(c.valor_inscricao), 0) as total_pendente
        from core_matricula as m
        INNER JOIN core_aluno as a on a.id = m.aluno_id
        INNER JOIN core_curso as c on c.id = m.curso_id
        WHERE m.status = 'pendente'
        GROUP BY a.id, a.nome
        ORDER BY total_pendente DESC;
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    resultados = [
        {
            "id": row[0],
            "aluno": row[1],
            "total_pendente": float(row[2]),
        }
        for row in rows
    ]

    return Response(resultados)


@api_view(["GET"])
def relatorio_matriculas_por_curso(request):
    dados = (Matricula.objects.values(nome_curso=F("curso__nome"))).annotate(
        total_matriculas=Count("id")
    )
    return Response(list(dados))
