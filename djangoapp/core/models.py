from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class StatusCurso(models.TextChoices):
    ATIVO = "ativo", _("Ativo")
    INATIVO = "inativo", _("Inativo")


class StatusMatricula(models.TextChoices):
    PAGO = "pago", _("Pago")
    PENDENTE = "pendente", _("Pendente")


def validar_numero_caracter_cpf(value):
    if not value.isdigit() or len(value) != 11:
        raise ValidationError(
            _("CPF deve conter exatamente 11 dígitos."),
            code="invalid_cpf",
        )


def validar_cpf_com_digito_continuo(value):
    if value == value[0] * 11:
        raise ValidationError("CPF de dígito contínuo não é válido,")


def validar_cpf_calculo(value):
    for i in range(9, 11):
        soma = sum(int(value[num]) * ((i + 1) - num) for num in range(0, i))
        digito = ((soma * 10) % 11) % 10
        if digito != int(value[i]):
            raise ValidationError("CPF inválido")


def validar_cpf(value):
    validar_numero_caracter_cpf(value)
    validar_cpf_com_digito_continuo(value)
    validar_cpf_calculo(value)


class Aluno(models.Model):
    nome = models.CharField(max_length=100, db_index=True)
    email = models.EmailField(unique=True, db_index=True)
    cpf = models.CharField(
        max_length=11,
        unique=True,
        validators=[validar_cpf],
        db_index=True,
    )
    data_de_ingresso = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.nome} ({self.cpf})"
    
    class Meta:
        ordering = ["-data_de_ingresso"]
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"
        indexes = [
            models.Index(fields=["nome", "-data_de_ingresso"]),
        ]


class Curso(models.Model):
    nome = models.CharField(max_length=100, db_index=True)
    carga_horaria = models.PositiveIntegerField()
    valor_inscricao = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=10,
        choices=StatusCurso.choices,
        default=StatusCurso.ATIVO,
        db_index=True
        )

    def __str__(self) -> str:
        return self.nome
    
    class Meta:
        ordering = ["nome"]
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        indexes = [
            models.Index(fields=["status", "nome"]),
        ]


class Matricula(models.Model):
    aluno = models.ForeignKey(
        Aluno, on_delete=models.CASCADE,
        related_name="matriculas",
        db_index=True
    )
    curso = models.ForeignKey(
        Curso,
        on_delete=models.CASCADE,
        related_name="matriculas",
        db_index=True)
    data_de_matricula = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=StatusMatricula.choices,
        default=StatusMatricula.PENDENTE,
        db_index=True,
    )

    def __str__(self) -> str:
        return f"{self.aluno.nome} -> {self.curso.nome}"
    
    class Meta:
        ordering = ["-data_de_matricula"]
        verbose_name = "Matrícula"
        verbose_name_plural = "Matrículas"
        unique_together = [["aluno", "curso"]]
        indexes = [
            models.Index(fields=["aluno", "status"]),
            models.Index(fields=["curso", "status"]),
        ]
