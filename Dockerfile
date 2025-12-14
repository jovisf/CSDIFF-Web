# Dockerfile para CSDiff-Web
# Inclui Python 3.11, Node.js e slow-diff3

FROM ubuntu:22.04

# Evitar prompts interativos durante instalação
ENV DEBIAN_FRONTEND=noninteractive

# Atualizar repositórios e instalar dependências base
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3-pip \
    git \
    curl \
    nodejs \
    npm \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Criar diretório de trabalho
WORKDIR /app

# Copiar requirements primeiro (para cache de camadas)
COPY requirements.txt /app/

# Instalar dependências Python
RUN pip3 install --no-cache-dir -r requirements.txt

# Clonar e instalar slow-diff3
RUN git clone https://github.com/leonardoAnjos16/slow-diff3.git /opt/slow-diff3 \
    && cd /opt/slow-diff3 \
    && npm install

# Definir variável de ambiente para slow-diff3
ENV SLOW_DIFF3_PATH=/opt/slow-diff3/src/index.js

# Copiar código do projeto
COPY src/ /app/src/
COPY tests/ /app/tests/
COPY scripts/ /app/scripts/
COPY examples/ /app/examples/
COPY config/ /app/config/

# Verificar instalações
RUN python3 --version && \
    node --version && \
    npm --version && \
    node /opt/slow-diff3/src/index.js -h

# Criar diretórios de dados
RUN mkdir -p /app/data/triplets /app/data/results /app/data/reports

# Comando padrão
CMD ["/bin/bash"]
