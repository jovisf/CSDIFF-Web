# Guia Rápido - CSDiff-Web

Este guia mostra como começar a usar o CSDiff-Web em 5 minutos.

## Instalação Rápida

```bash
# 1. Clonar repositório
git clone https://github.com/YOUR_USERNAME/csdiff-web.git
cd csdiff-web

# 2. Instalar dependências
pip3 install -r requirements.txt

# 3. Verificar instalação
python3 -c "from src.core.csdiff_web import CSDiffWeb; print('✓ OK')"
pytest tests/ -v
```

## Uso Básico

### Exemplo 1: Merge Simples

```python
from src.core.csdiff_web import CSDiffWeb

merger = CSDiffWeb()

base = "function foo() { return 1; }"
left = "function foo() { console.log('A'); return 1; }"
right = "function foo() { return 2; }"

result, has_conflict, num_conflicts = merger.merge(base, left, right, "example.ts")
print(result)
# Output: function foo() { console.log('A'); return 2; }
```

### Exemplo 2: Pipeline Completo

```bash
# 1. Minerar triplas (cria data/triplets/)
python3 scripts/mine_repositories.py --max-triplets 20

# 2. Executar experimentos (cria data/results/*.csv)
python3 scripts/run_experiments.py --max-triplets 20

# 3. Analisar resultados (cria data/reports/*.md)
python3 scripts/analyze_results.py data/results/results_*.csv
```

### Exemplo 3: Demo Sintético

```bash
# Executa exemplo completo com triplas sintéticas
python3 examples/simple_experiments.py

# Executa análise completa
python3 examples/simple_analysis.py
```

## Comandos Úteis

```bash
# Testes
pytest tests/ -v                          # Todos os testes
pytest tests/test_core/ -v                # Apenas Core

# Mineração
python3 scripts/mine_repositories.py \
    --max-triplets 50 \
    --extensions .ts .tsx

# Experimentos
python3 scripts/run_experiments.py \
    --max-triplets 50 \
    --tools csdiff-web diff3 \
    --timeout 60

# Análise
python3 scripts/analyze_results.py \
    data/results/results_*.csv \
    --output data/reports
```

## Estrutura de Dados

### Tripla Minerada
```
data/triplets/triplet_001/
├── base.ts          # Versão ancestral
├── left.ts          # Parent 0
├── right.ts         # Parent 1
└── metadata.txt     # Informações
```

### Resultado CSV
```csv
triplet_id,extension,
csdiff_web_success,csdiff_web_num_conflicts,csdiff_web_time,
diff3_success,diff3_num_conflicts,diff3_time
triplet_001,.ts,True,0,0.005,True,1,0.003
```

### Relatório Gerado
```
data/reports/
├── analysis_TIMESTAMP.md    # Relatório científico
└── table_TIMESTAMP.tex      # Tabela LaTeX
```

## Documentação Completa

- **README.md** - Visão geral do projeto
- **docs/ARCHITECTURE.md** - Arquitetura técnica detalhada
- **docs/USAGE_GUIDE.md** - Guia completo de uso
- **docs/PROJECT_SUMMARY.md** - Resumo executivo
- **CHANGELOG.md** - Histórico de versões

## Troubleshooting

**diff3 não encontrado**:
```bash
# Linux
sudo apt-get install diffutils

# macOS
brew install diffutils
```

**Triplas não encontradas**:
```bash
# Minerar triplas primeiro
python3 scripts/mine_repositories.py --max-triplets 10
```

**Mergiraf não disponível** (OPCIONAL):
```bash
pip3 install mergiraf
```

## Próximos Passos

1. Leia [ARCHITECTURE.md](docs/ARCHITECTURE.md) para entender o design
2. Siga [USAGE_GUIDE.md](docs/USAGE_GUIDE.md) para casos avançados
3. Execute experimentos em escala (100+ triplas)
4. Gere visualizações dos resultados

## Suporte

- **Bugs**: Abra uma issue no GitHub
- **Dúvidas**: Consulte a documentação em `docs/`
- **Contato**: Prof. Paulo Borba (UFPE)

---

**Status**: ✅ Pronto para uso (v1.0.0)
**TCC**: UFPE/CIn 2025
