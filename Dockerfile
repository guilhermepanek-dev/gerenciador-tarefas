# Gerenciador de Tarefas (CLI) — imagem Docker
# Baseado no guia oficial do Docker para Python:
# https://docs.docker.com/language/python/

# 1) Imagem base enxuta do Python 3.11
FROM python:3.11-slim

# 2) Evita buffers de saída do Python (logs aparecem na hora)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3) Diretório de trabalho dentro do container
WORKDIR /app

# 4) Instala o pacote do projeto (a base slim já inclui setuptools/wheel,
#    então o build é feito sem isolamento e sem downloads externos)
COPY pyproject.toml README.md ./
COPY gerenciador.py main.py ./
RUN pip install --no-cache-dir --no-build-isolation --no-deps .

# 5) Diretório de dados persistido em volume (montado em /app/data)
ENV TAREFAS_ARQUIVO=/app/data/tarefas.json
RUN useradd --create-home appuser \
    && mkdir -p /app/data \
    && chown -R appuser:appuser /app/data
VOLUME /app/data

# 6) Usuário não privilegiado para executar a aplicação
USER appuser

# 7) Entrypoint: CLI do gerenciador
ENTRYPOINT ["gerenciador"]
CMD ["--help"]
