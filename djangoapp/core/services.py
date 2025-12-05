from django.db.models import Sum, F, QuerySet
from .models import Matricula, Aluno


def calcular_total_por_aluno(aluno: Aluno):
    matriculas = Matricula.objects.filter(aluno=aluno)

    dados_pagos = calcular_total_matriculas_por_filtro(matriculas, "pago")
    dados_pendentes = calcular_total_matriculas_por_filtro(matriculas, "pendente")

    return {
        "total_pago": dados_pagos["valor_total_pago"],
        "total_pendente": dados_pendentes["valor_total_pendente"],
        "total_matriculas_pagas": dados_pagos["quantidade_pago"],
        "total_matriculas_pendentes": dados_pendentes["quantidade_pendente"],
        "total_matriculas": matriculas.count(),
        "matriculas": matriculas,
    }


def calcular_total_matriculas_por_filtro(matriculas: QuerySet[Matricula], filtro: str):
    matriculas_calculadas = matriculas.filter(status__iexact=filtro)
    total_matriculas = matriculas_calculadas.count()
    valor_total = (
        matriculas_calculadas.aggregate(
            total_em_reais=Sum(F("curso__valor_inscricao"))
        )["total_em_reais"]
        or 0
    )
    return {
        f"quantidade_{filtro}": total_matriculas,
        f"valor_total_{filtro}": valor_total,
    }


def selecionar_matriculas_por_filtro(matriculas: QuerySet[Matricula], filtro: str):
    dados = (
        matriculas.filter(status__iexact=filtro)
        .values(nome_aluno=F("aluno__nome"))
        .annotate(total_pago=Sum(F("curso__valor_inscricao")))
    )

    return list(dados)
