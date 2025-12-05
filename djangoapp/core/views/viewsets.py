from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models import Aluno, Curso, Matricula
from ..serializers import AlunoSerializer, CursoSerializer, MatriculaSerializer


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
        serializer = self.get_serializer(matriculas, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="marcar-como-paga")
    def marcar_como_paga(self, request, pk=None):
        matricula = self.get_object()
        matricula.status = "pago"
        matricula.save()
        return Response(self.get_serializer(matricula).data)
