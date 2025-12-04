from django.db import models


class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=11, unique=True)
    data_de_ingresso = models.DateField()

    def __str__(self) -> str:
        return f"{self.nome} ({self.cpf})"


class Curso(models.Model):
    STATUS_CHOICES = [
        ("ativo", "Ativo"),
        ("inativo", "Inativo"),
    ]

    nome = models.CharField(max_length=100)
    carga_horaria = models.IntegerField()
    valor_inscricao = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)


    def __str__(self) -> str:
        return self.nome
    
class Matricula(models.Model):
    STATUS_CHOICES = [
        ("pago", "Pago"),
        ("pendente", "Pendente")
    ]

    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="matriculas")
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    data_de_matricula = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pendente")

    def __str__(self) -> str:
        return f"{self.aluno.nome} -> {self.curso.nome}"