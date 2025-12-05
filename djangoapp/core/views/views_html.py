from django.shortcuts import get_object_or_404, render
from ..models import Aluno
from ..services import calcular_total_por_aluno


def historico_aluno(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)

    dados = calcular_total_por_aluno(aluno)

    return render(request, "core/historico_aluno.html", {"aluno": aluno, **dados})
