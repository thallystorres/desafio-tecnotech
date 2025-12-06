from django.db.models import Sum, F, QuerySet, Count
from decimal import Decimal
from .models import Aluno, Curso, Matricula, StatusMatricula
from django.db.models.functions import Coalesce
class MatriculaService:

    @staticmethod
    def calcular_total_por_status(matriculas: QuerySet[Matricula], status: str) -> dict:
        matriculas_filtradas = matriculas.filter(status=status)
        qtd = matriculas_filtradas.count()
        valor_total = (
            matriculas_filtradas.aggregate(total=Coalesce(Sum(F("curso__valor_inscricao")), Decimal("0")))["total"] or Decimal("0")
        )
        return {
            f"quantidade_{status}": qtd,
            f"valor_total_{status}": valor_total,
        }

    @staticmethod
    def calcular_total_por_aluno(aluno: Aluno) -> dict:
        matriculas = Matricula.objects.filter(aluno=aluno)
        dados_pagos = MatriculaService.calcular_total_por_status(
            matriculas, StatusMatricula.PAGO
        )
        dados_pendentes = MatriculaService.calcular_total_por_status(
            matriculas, StatusMatricula.PENDENTE
        )
        return {
            "total_pago": dados_pagos[f"valor_total_{StatusMatricula.PAGO}"],
            "total_pendente": dados_pendentes[f"valor_total_{StatusMatricula.PENDENTE}"],
            "total_matriculas_pagas": dados_pagos[f"quantidade_{StatusMatricula.PAGO}"],
            "total_matriculas_pendentes": dados_pendentes[f"quantidade_{StatusMatricula.PENDENTE}"],
            "total_matriculas": matriculas.count(),
            "matriculas": matriculas,
        }

    @staticmethod
    def listar_matriculas_por_status(matriculas: QuerySet[Matricula], filtro: str):
        dados = (
            matriculas.filter(status__iexact=filtro)
            .values(nome_aluno=F("aluno__nome"))
            .annotate(total_pago=Sum(F("curso__valor_inscricao")))
        )
    
        return list(dados)

class DashboardService:

    @staticmethod
    def gerar_dashboard() -> dict:
        total_alunos = Aluno.objects.count()
        total_cursos = Curso.objects.count()
        total_matriculas = Matricula.objects.count()

        todas_matriculas = Matricula.objects.all()
        dados_pagas = MatriculaService.calcular_total_por_status(
            todas_matriculas, StatusMatricula.PAGO
        )
        dados_pendentes = MatriculaService.calcular_total_por_status(
            todas_matriculas, StatusMatricula.PENDENTE
        )

        qtd_pagas = dados_pagas[f"quantidade_{StatusMatricula.PAGO}"]
        qtd_pendentes = dados_pendentes[f"quantidade_{StatusMatricula.PENDENTE}"]

        total_registros = qtd_pagas + qtd_pendentes
        perc_pagas = (qtd_pagas / total_registros * 100) if total_registros else 100
        perc_pendentes = 100 - perc_pagas

        matriculas_por_curso = (
            Matricula.objects.values(nome=F("curso__nome"))
            .annotate(total=Count("id"))
            .order_by("-total")
        )

        return {
            "total_alunos": total_alunos,
            "total_cursos": total_cursos,
            "total_matriculas": total_matriculas,
            "total_pago": dados_pagas[f"valor_total_{StatusMatricula.PAGO}"],
            "total_pendente": dados_pendentes[f"valor_total_{StatusMatricula.PENDENTE}"],
            "qtd_pagas": qtd_pagas,
            "qtd_pendentes": qtd_pendentes,
            "perc_pagas": perc_pagas,
            "perc_pendentes": perc_pendentes,
            "matriculas_por_curso": matriculas_por_curso,
        }
