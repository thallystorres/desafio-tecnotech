# Academia Dev Python - Desafio Técnico


> Sistema de gestão acadêmica para cadastro de alunos, cursos e matrículas, com relatórios financeiros e dashboards integrados.


**Desenvolvido por:** [Thallys Torres](https://github.com/thallystorres)


---


## 📋 Pré-requisitos


Antes de executar o projeto, certifique-se de ter instalado:


- [Docker](https://docs.docker.com/get-docker/)

- [Docker Compose](https://docs.docker.com/compose/install/)


---


## ⚙️ Configuração do .env


Antes de executar a aplicação, crie um arquivo `.env` na raiz do projeto semelhante ao arquivo `.env-example`:


**Notas importantes:**

- `DJANGO_SECRET_KEY`: Use uma chave segura em produção. Pode gerar com: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`

- `DJANGO_DEBUG=True`: Use apenas em desenvolvimento. Em produção, altere para `False`

- `POSTGRES_PASSWORD`: Defina uma senha forte para o banco de dados

- `DJANGO_ALLOWED_HOSTS`: Liste os hosts permitidos separados por vírgula


---


## 🚀 Como Rodar a Aplicação


A aplicação está totalmente containerizada. Execute o comando abaixo na raiz do projeto para construir a imagem, instalar dependências, aplicar migrações e iniciar o servidor:


```bash

docker compose up --build

```


Aguarde até que o log exiba `Starting development server at http://0.0.0.0:8000/`.


---


## 🔗 Acessando o Sistema


Após os containers estarem rodando, acesse as seguintes interfaces:


### Frontend - Dashboard

- **URL:** http://localhost:8000/

- Visualização de métricas e listagens gerais

- Histórico do aluno: http://localhost:8000/aluno/{id}/historico/


### API REST

- **URL:** http://localhost:8000/api/

- Interface navegável do Django Rest Framework


### Administração Django

- **URL:** http://localhost:8000/admin/


---


## 👤 Criando um Usuário Administrador

Para acessar o painel de administração (`/admin`), você precisa criar um superusuário. Com os containers rodando, execute:

```bash
docker compose exec web python manage.py createsuperuser
```

O sistema solicitará:
- **Username:** Digite um nome de usuário
- **Email:** Digite um endereço de email (pode ser fictício ou pode até deixar em branco)
- **Password:** Digite uma senha segura
- **Password (again):** Confirme a senha

Após criar o superusuário, faça login em http://localhost:8000/admin/ com as credenciais fornecidas.


---


## 📡 Endpoints da API


### Alunos

- `GET/POST` `/api/alunos/` - Listar e criar alunos

- `PUT/DELETE` `/api/alunos/{id}/` - Atualizar e remover alunos


### Cursos

- `GET/POST` `/api/cursos/` - Listar e criar cursos

- `PUT/DELETE` `/api/cursos/{id}/` - Atualizar e remover cursos


### Matrículas

- `GET` `/api/matriculas/` - Listar matrículas

- `GET` `/api/matriculas/por-aluno/{aluno_id}/` - Matrículas de um aluno específico

- `POST` `/api/matriculas/{id}/marcar-como-paga/` - Marcar matrícula como paga


### Relatórios

- `GET` `/api/relatorios/matriculas-por-curso/` - Matrículas por curso

- `GET` `/api/relatorios/total-devido-aluno/` - Total devido por aluno (SQL Puro)

- `GET` `/api/relatorios/total-pago-aluno/` - Total pago por aluno

- `GET` `/api/relatorios/total-pagamentos-pendentes/` - Total de pagamentos pendentes


---


## 🧪 Executando os Testes


⚠️ **Por padrão os testes rodam antes mesmo da aplicação ser rodada** ⚠️


A suíte de testes valida os models e services do projeto:


```bash

docker compose run --rm web run_tests.sh

```


---


## 🛠 Tecnologias Utilizadas


| Componente              | Versão |
| ----------------------- | ------ |
| Python                  | 3.14   |
| Django                  | 5.2.8  |
| Django Rest Framework   | 3.16.1 |
| PostgreSQL              | 18     |
| Docker & Docker Compose | Latest |


---


## 📂 Estrutura do Projeto


```

tecnotech/

├── djangoapp/              # Aplicação Django

│   ├── core/              # App principal com models, views e serializers

│   ├── project/           # Configurações do Django

│   └── manage.py

├── scripts/               # Scripts de utilitários

├── docker-compose.yml     # Orquestração dos serviços

├── Dockerfile            # Imagem Docker da aplicação

├── meu_database.sql      # Schema do banco de dados

└── README.md

```


---


## 📄 Licença


Este projeto está sob a licença definida no arquivo [LICENSE](./LICENSE).