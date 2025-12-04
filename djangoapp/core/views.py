from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.db.models import Count, F, Sum
from .models import Aluno, Curso, Matricula
from .serializers import AlunoSerializer, CursoSerializer, MatriculaSerializer


@api_view(["GET"])
def total_de_pagamentos_pendentes(request):
    total = Matricula.objects.filter(status__iexact="pendente")
    quantidade_pendente = total.count()
    valor_total_pendente = (
        total.aggregate(total_em_reais=Sum(F("curso__valor_inscricao")))[
            "total_em_reais"
        ]
        or 0
    )
    return Response(
        {
            "quantidade_pendente": quantidade_pendente,
            "valor_total_pendente": valor_total_pendente,
        }
    )

@api_view(["GET"])
def total_pago_por_aluno(request):
    dados = (
        Matricula.objects.filter(status__iexact="pago").values(
            nome_aluno=F("aluno__nome")
        )
    ).annotate(total_pago=Sum(F("curso__valor_inscricao")))
    return Response(list(dados))

@api_view(["GET"])
def total_devido_por_aluno(request):
    dados = (
        Matricula.objects.filter(status__iexact="pendente").values(
            nome_aluno=F("aluno__nome")
        )
    ).annotate(total_devido=Sum(F("curso__valor_inscricao")))
    return Response(list(dados))


@api_view(["GET"])
def relatorio_matriculas_por_curso(request):
    dados = (Matricula.objects.values(nome_curso=F("curso__nome"))).annotate(
        total_matriculas=Count("id")
    )
    return Response(list(dados))


class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer


class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer


class MatriculaViewSet(viewsets.ModelViewSet):
    queryset = Matricula.objects.all()
    serializer_class = MatriculaSerializer

    @action(detail=False, methods=["get"], url_path="por-aluno/(?P<aluno_id>[^/.]+)")
    def listar_por_aluno(self, request, aluno_id=None):
        matriculas = Matricula.objects.filter(aluno_id=aluno_id)
        serializer = MatriculaSerializer(matriculas, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def marcar_como_paga(self, request, pk=None):
        matricula = self.get_object()
        matricula.status = "pago"
        matricula.save()
        serializer = MatriculaSerializer(matricula)
        return Response(serializer.data)
