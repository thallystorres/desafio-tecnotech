from django.shortcuts import render
from rest_framework import viewsets
from .models import Aluno, Curso, Matricula
from .serializers import AlunoSerializer, CursoSerializer, MatriculaSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

    @action(detail=False, methods=['get'], url_path='por-aluno/(?P<aluno_id>[^/.]+)')
    def listar_por_aluno(self, request, aluno_id=None):
        matriculas = Matricula.objects.filter(aluno_id=aluno_id)
        serializer = MatriculaSerializer(matriculas, many=True)
        return Response(serializer.data)

class MatriculaViewSet(viewsets.ModelViewSet):
    queryset = Matricula.objects.all()
    serializer_class = MatriculaSerializer
