from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError

from .models import Aluno, Curso, Matricula, StatusCurso, StatusMatricula
from .services import MatriculaService, DashboardService


class AlunoModelTest(TestCase):
    def setUp(self):
        self.aluno = Aluno.objects.create(
            nome="João Silva",
            email="joao@example.com",
            cpf="11144477735",
        )

    def test_criar_aluno(self):
        self.assertEqual(self.aluno.nome, "João Silva")
        self.assertEqual(self.aluno.email, "joao@example.com")

    def test_str_aluno(self):
        self.assertEqual(str(self.aluno), "João Silva (11144477735)")

    def test_email_unico(self):
        with self.assertRaises(Exception):
            Aluno.objects.create(
                nome="Maria",
                email="joao@example.com",
                cpf="22255588844",
            )

    def test_cpf_unico(self):
        with self.assertRaises(Exception):
            Aluno.objects.create(
                nome="Maria",
                email="maria@example.com",
                cpf="11144477735",
            )

    def test_cpf_invalido_tamanho(self):
        with self.assertRaises(ValidationError):
            aluno = Aluno(
                nome="Pedro",
                email="pedro@example.com",
                cpf="123",
            )
            aluno.full_clean()

    def test_cpf_invalido_digito_continuo(self):
        with self.assertRaises(ValidationError):
            aluno = Aluno(
                nome="Pedro",
                email="pedro@example.com",
                cpf="11111111111",
            )
            aluno.full_clean()


class CursoModelTest(TestCase):
    def setUp(self):
        self.curso_ativo = Curso.objects.create(
            nome="Django Avançado",
            carga_horaria=40,
            valor_inscricao=Decimal("299.90"),
            status=StatusCurso.ATIVO,
        )
        self.curso_inativo = Curso.objects.create(
            nome="Python Legado",
            carga_horaria=30,
            valor_inscricao=Decimal("199.90"),
            status=StatusCurso.INATIVO,
        )

    def test_criar_curso_ativo(self):
        self.assertEqual(self.curso_ativo.status, StatusCurso.ATIVO)
        self.assertEqual(self.curso_ativo.valor_inscricao, Decimal("299.90"))

    def test_str_curso(self):
        self.assertEqual(str(self.curso_ativo), "Django Avançado")

    def test_curso_inativo(self):
        self.assertEqual(self.curso_inativo.status, StatusCurso.INATIVO)


class MatriculaModelTest(TestCase):
    def setUp(self):
        self.aluno = Aluno.objects.create(
            nome="João Silva",
            email="joao@example.com",
            cpf="11144477735",
        )
        self.curso_ativo = Curso.objects.create(
            nome="Django",
            carga_horaria=40,
            valor_inscricao=Decimal("299.90"),
            status=StatusCurso.ATIVO,
        )
        self.curso_inativo = Curso.objects.create(
            nome="Python",
            carga_horaria=30,
            valor_inscricao=Decimal("199.90"),
            status=StatusCurso.INATIVO,
        )

    def test_criar_matricula_curso_ativo(self):
        matricula = Matricula.objects.create(
            aluno=self.aluno,
            curso=self.curso_ativo,
            status=StatusMatricula.PENDENTE,
        )
        self.assertEqual(matricula.aluno, self.aluno)
        self.assertEqual(matricula.curso, self.curso_ativo)

    def test_str_matricula(self):
        matricula = Matricula.objects.create(
            aluno=self.aluno,
            curso=self.curso_ativo,
        )
        self.assertEqual(str(matricula), "João Silva -> Django")

    def test_validacao_curso_inativo(self):
        matricula = Matricula(
            aluno=self.aluno,
            curso=self.curso_inativo,
        )
        with self.assertRaises(ValidationError):
            matricula.full_clean()

    def test_matricula_duplicada(self):
        Matricula.objects.create(
            aluno=self.aluno,
            curso=self.curso_ativo,
        )
        with self.assertRaises(Exception):
            Matricula.objects.create(
                aluno=self.aluno,
                curso=self.curso_ativo,
            )


class MatriculaServiceTest(TestCase):
    def setUp(self):
        self.aluno = Aluno.objects.create(
            nome="João Silva",
            email="joao@example.com",
            cpf="11144477735",
        )
        self.curso1 = Curso.objects.create(
            nome="Django",
            carga_horaria=40,
            valor_inscricao=Decimal("100.00"),
        )
        self.curso2 = Curso.objects.create(
            nome="Python",
            carga_horaria=30,
            valor_inscricao=Decimal("80.00"),
        )

    def test_calcular_total_por_status(self):
        Matricula.objects.create(
            aluno=self.aluno,
            curso=self.curso1,
            status=StatusMatricula.PAGO,
        )
        Matricula.objects.create(
            aluno=self.aluno,
            curso=self.curso2,
            status=StatusMatricula.PENDENTE,
        )

        dados = MatriculaService.calcular_total_por_status(
            Matricula.objects.all(),
            StatusMatricula.PAGO,
        )

        self.assertEqual(dados["quantidade_pago"], 1)
        self.assertEqual(dados["valor_total_pago"], Decimal("100.00"))

    def test_calcular_total_por_aluno(self):
        Matricula.objects.create(
            aluno=self.aluno,
            curso=self.curso1,
            status=StatusMatricula.PAGO,
        )
        Matricula.objects.create(
            aluno=self.aluno,
            curso=self.curso2,
            status=StatusMatricula.PENDENTE,
        )

        dados = MatriculaService.calcular_total_por_aluno(self.aluno)

        self.assertEqual(dados["total_matriculas"], 2)
        self.assertEqual(dados["total_pago"], Decimal("100.00"))
        self.assertEqual(dados["total_pendente"], Decimal("80.00"))

    def test_listar_matriculas_por_status(self):
        Matricula.objects.create(
            aluno=self.aluno,
            curso=self.curso1,
            status=StatusMatricula.PAGO,
        )

        dados = MatriculaService.listar_matriculas_por_status(
            Matricula.objects.all(),
            StatusMatricula.PAGO,
        )

        self.assertEqual(len(dados), 1)
        self.assertEqual(dados[0]["nome_aluno"], "João Silva")


class DashboardServiceTest(TestCase):
    def setUp(self):
        self.aluno = Aluno.objects.create(
            nome="João",
            email="joao@example.com",
            cpf="11144477735",
        )
        self.curso = Curso.objects.create(
            nome="Django",
            carga_horaria=40,
            valor_inscricao=Decimal("100.00"),
        )

    def test_gerar_dashboard_vazio(self):
        dados = DashboardService.gerar_dashboard()

        self.assertEqual(dados["total_alunos"], 1)
        self.assertEqual(dados["total_cursos"], 1)
        self.assertEqual(dados["total_matriculas"], 0)

    def test_gerar_dashboard_com_dados(self):
        Matricula.objects.create(
            aluno=self.aluno,
            curso=self.curso,
            status=StatusMatricula.PAGO,
        )

        dados = DashboardService.gerar_dashboard()

        self.assertEqual(dados["total_matriculas"], 1)
        self.assertEqual(dados["qtd_pagas"], 1)
        self.assertEqual(dados["perc_pagas"], 100.0)
