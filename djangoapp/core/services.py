from django.db.models import Sum, F, QuerySet, Count
from .models import Aluno, Curso, Matricula


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

def gerar_dashboard():
    total_alunos = Aluno.objects.count()
    total_cursos = Curso.objects.count()
    total_matriculas = Matricula.objects.count()

    dados_pagas = calcular_total_matriculas_por_filtro(Matricula.objects.all(), "pago")
    dados_pendentes = calcular_total_matriculas_por_filtro(Matricula.objects.all(), "pendente")

    qtd_pagas = dados_pagas["quantidade_pago"]
    qtd_pendentes = dados_pendentes["quantidade_pendente"]

    total_registros = qtd_pagas + qtd_pendentes
    perc_pagas = (qtd_pagas / total_registros * 100) if total_registros else 0
    perc_pendentes = 100 - perc_pagas

    matriculas_por_curso = (Matricula.objects.values(nome=F("curso__nome")).annotate(total=Count("id")).order_by("nome"))

    return {
        "total_alunos": total_alunos,
        "total_cursos": total_cursos,
        "total_matriculas": total_matriculas,
        "total_pago": dados_pagas["valor_total_pago"],
        "total_pendente": dados_pendentes["valor_total_pendente"],
        "qtd_pagas": qtd_pagas,
        "qtd_pendentes": qtd_pendentes,
        "perc_pagas": perc_pagas,
        "perc_pendentes": perc_pendentes,
        "matriculas_por_curso": matriculas_por_curso,
    }
