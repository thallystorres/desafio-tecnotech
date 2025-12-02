#!/bin/sh
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  echo "🟡 Esperando inicialização do banco de dados ($POSTGRES_HOST $POSTGRES_PORT) ..."
  sleep 2
done

echo "✅ Banco de dados inicializado com sucesso ($POSTGRES_HOST:$POSTGRES_PORT)"
