# Guia Docker - CSDiff-Web

Este guia mostra como usar o CSDiff-Web com Docker.

## Pré-requisitos

- Docker instalado (versão 20.10+)
- Docker Compose instalado (versão 1.29+)

## Build da Imagem

```bash
# Build da imagem
docker build -t csdiff-web:latest .

# Ou usando docker-compose
docker-compose build
```

## Uso Básico

### Modo Interativo

```bash
# Iniciar container interativo
docker-compose run --rm csdiff-web

# Dentro do container
python3 -c "from src.core.csdiff_web import CSDiffWeb; print('OK')"
```

### Executar Testes

```bash
# Rodar todos os testes
docker-compose run --rm csdiff-web-test

# Ou manualmente
docker-compose run --rm csdiff-web pytest tests/ -v
```

### Executar Exemplos

```bash
# Exemplo simples
docker-compose run --rm csdiff-web python3 examples/simple_experiments.py

# Análise completa
docker-compose run --rm csdiff-web python3 examples/simple_analysis.py
```

## Pipeline Completo

### 1. Mineração

```bash
docker-compose run --rm csdiff-web \
    python3 scripts/mine_repositories.py \
    --max-triplets 50 \
    --extensions .ts .tsx
```

### 2. Experimentos

```bash
docker-compose run --rm csdiff-web \
    python3 scripts/run_experiments.py \
    --max-triplets 50 \
    --tools csdiff-web diff3
```

### 3. Análise

```bash
docker-compose run --rm csdiff-web \
    python3 scripts/analyze_results.py \
    data/results/results_*.csv
```

## Persistência de Dados

Os dados são persistidos no diretório `./data` do host:

```
./data/
├── triplets/    # Triplas mineradas
├── results/     # CSVs de experimentos
└── reports/     # Relatórios gerados
```

Para limpar os dados:

```bash
rm -rf ./data/*
```

## Desenvolvimento

### Modo Watch (código fonte montado)

O docker-compose.yml já monta o código fonte como volume. Mudanças no código do host são refletidas no container imediatamente:

```bash
# Iniciar container
docker-compose run --rm csdiff-web bash

# Editar código no host (VSCode, vim, etc.)
# Testar mudanças no container
pytest tests/ -v
```

### Verificar slow-diff3

```bash
docker-compose run --rm csdiff-web \
    node /opt/slow-diff3/src/index.js -h
```

### Debug do slow-diff3

```bash
docker-compose run --rm csdiff-web bash

# Dentro do container
cat > /tmp/base.txt << 'EOF'
linha1
linha2
EOF

cat > /tmp/left.txt << 'EOF'
linha1
linha2
linha3
EOF

cat > /tmp/right.txt << 'EOF'
linha1
linha2
linha4
EOF

# Modo merge
node /opt/slow-diff3/src/index.js /tmp/left.txt /tmp/base.txt /tmp/right.txt -m

# Modo debug
node /opt/slow-diff3/src/index.js /tmp/left.txt /tmp/base.txt /tmp/right.txt -d
```

## Variáveis de Ambiente

Configure no `docker-compose.yml` ou passe via CLI:

```bash
docker-compose run --rm \
    -e SLOW_DIFF3_PATH=/custom/path/index.js \
    csdiff-web python3 script.py
```

Variáveis disponíveis:
- `SLOW_DIFF3_PATH`: Caminho para o slow-diff3 (padrão: `/opt/slow-diff3/src/index.js`)
- `PYTHONUNBUFFERED`: Desabilita buffer do Python (padrão: `1`)

## Troubleshooting

### Build falha no npm install

```bash
# Limpar cache do Docker
docker system prune -a

# Build sem cache
docker build --no-cache -t csdiff-web:latest .
```

### slow-diff3 não encontrado

```bash
# Verificar instalação
docker-compose run --rm csdiff-web \
    ls -la /opt/slow-diff3/src/index.js

# Verificar variável de ambiente
docker-compose run --rm csdiff-web \
    echo $SLOW_DIFF3_PATH
```

### Testes falhando

```bash
# Rodar teste específico
docker-compose run --rm csdiff-web \
    pytest tests/test_csdiff_integration.py::TestBasicMerge -v

# Com output verboso
docker-compose run --rm csdiff-web \
    pytest tests/ -vv -s
```

### Permissões em ./data

```bash
# Ajustar permissões (Linux)
sudo chown -R $USER:$USER ./data

# Ou executar container como usuário atual
docker-compose run --rm --user $(id -u):$(id -g) csdiff-web bash
```

## Comandos Úteis

```bash
# Listar imagens
docker images | grep csdiff-web

# Remover imagem
docker rmi csdiff-web:latest

# Logs do container
docker-compose logs csdiff-web

# Parar todos os containers
docker-compose down

# Rebuild completo
docker-compose build --no-cache

# Shell no container
docker-compose run --rm csdiff-web bash

# Executar comando único
docker-compose run --rm csdiff-web python3 --version
```

## Produção

Para uso em produção, considere:

1. **Multi-stage build** para reduzir tamanho da imagem
2. **Security scanning** com Trivy ou Snyk
3. **Health checks** para monitoring
4. **Resource limits** no docker-compose.yml

Exemplo de resource limits:

```yaml
services:
  csdiff-web:
    # ...
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G
```

## Integração CI/CD

### GitHub Actions

```yaml
name: Docker Build

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build image
        run: docker build -t csdiff-web:latest .
      - name: Run tests
        run: docker run csdiff-web:latest pytest tests/ -v
```

### GitLab CI

```yaml
docker-build:
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t csdiff-web:latest .
    - docker run csdiff-web:latest pytest tests/ -v
```

---

**Última atualização**: 2025-12-13
**Versão Docker**: 1.0.0 (com slow-diff3)
