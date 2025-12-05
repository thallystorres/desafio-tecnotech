from django.db.models import Sum, F, QuerySet
from .models import Matricula

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
