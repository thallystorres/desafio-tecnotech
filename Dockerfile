FROM python:3.14-slim-trixie

LABEL maintainer="https://www.github.com/thallystorres"

# Não criar .pyc
ENV PYTHONDONTWRITEBYTECODE=1

# Logs sem buffer
ENV PYTHONUNBUFFERED=1

# Diretório de trabalho
WORKDIR /app
COPY djangoapp/ .
COPY scripts /scripts

# Porta usada pelo Django
EXPOSE 8000

# Instala dependências do sistema e configurando permissões dos scripts de inicialização
RUN apt-get update && apt-get install -y \
    build-essential \ 
    curl \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/* \
    && chmod -R +x /scripts 

# Copiando uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY djangoapp/requirements.txt .

RUN uv pip install -r requirements.txt --system

# Exportando scripts para o path
ENV PATH="/scripts:$PATH"

# Comando padrão
CMD ["commands.sh"]

