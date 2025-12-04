from django.contrib import admin
from .models import Aluno, Curso, Matricula

admin.site.register(Aluno)
admin.site.register(Curso)
admin.site.register(Matricula)