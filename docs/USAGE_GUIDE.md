# Guia de Uso Completo - CSDiff-Web

Este guia contém exemplos práticos de uso do CSDiff-Web, desde casos simples até pipelines completos de pesquisa.

## Índice

- [Instalação](#instalação)
- [Uso Básico](#uso-básico)
- [Mineração de Repositórios](#mineração-de-repositórios)
- [Execução de Experimentos](#execução-de-experimentos)
- [Análise de Resultados](#análise-de-resultados)
- [Integração em Código](#integração-em-código)
- [Casos de Uso Avançados](#casos-de-uso-avançados)
- [Troubleshooting](#troubleshooting)

---

## Instalação

### 1. Clonar Repositório

```bash
git clone https://github.com/YOUR_USERNAME/csdiff-web.git
cd csdiff-web
```

### 2. Instalar Dependências

```bash
# Criar ambiente virtual (recomendado)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip3 install -r requirements.txt
```

### 3. Verificar Instalação

```bash
# Verificar diff3
diff3 --version

# Verificar Python
python3 --version  # Deve ser 3.8+

# Testar CSDiff-Web
python3 -c "from src.core.csdiff_web import CSDiffWeb; print('✓ CSDiff-Web OK')"

# Rodar testes
pytest tests/ -v
```

---

## Uso Básico

### Exemplo 1: Merge Simples (TypeScript)

```python
from src.core.csdiff_web import CSDiffWeb

# Criar instância
merger = CSDiffWeb()

# Versões do código
base = "function foo() { return 1; }"
left = "function foo() { console.log('A'); return 1; }"
right = "function foo() { return 2; }"

# Executar merge
result, has_conflict, num_conflicts = merger.merge(
    base=base,
    left=left,
    right=right,
    filename="example.ts"
)

print("Resultado:")
print(result)
print(f"\nConflitos: {num_conflicts}")
```

**Saída esperada**:
```typescript
function foo() { console.log('A'); return 2; }

Conflitos: 0
```

### Exemplo 2: Merge com Conflito

```python
from src.core.csdiff_web import CSDiffWeb

merger = CSDiffWeb()

base = """function calculate(x) {
    return x * 2;
}"""

left = """function calculate(x) {
    return x * 3;
}"""

right = """function calculate(x) {
    return x * 5;
}"""

result, has_conflict, num_conflicts = merger.merge(base, left, right, "calc.ts")

print(result)
print(f"Tem conflito: {has_conflict}")
print(f"Número de conflitos: {num_conflicts}")
```

**Saída esperada**:
```typescript
function calculate(x) {
<<<<<<< left
    return x * 3;
=======
    return x * 5;
>>>>>>> right
}

Tem conflito: True
Número de conflitos: 1
```

### Exemplo 3: Merge de JSX

```python
from src.core.csdiff_web import CSDiffWeb

merger = CSDiffWeb()

base = """function Button() {
    return <button>Click</button>;
}"""

left = """function Button() {
    return <button className="btn">Click</button>;
}"""

right = """function Button() {
    return <button onClick={handleClick}>Click</button>;
}"""

result, has_conflict, num_conflicts = merger.merge(base, left, right, "Button.jsx")

print(result)
```

**Saída esperada**:
```jsx
function Button() {
    return <button className="btn" onClick={handleClick}>Click</button>;
}
```

---

## Mineração de Repositórios

### Configuração de Repositórios

Edite `config/repositories.yaml`:

```yaml
repositories:
  - name: "vscode"
    url: "https://github.com/microsoft/vscode.git"
    language: "typescript"
    stars: 162000
    description: "Visual Studio Code"

  - name: "react"
    url: "https://github.com/facebook/react.git"
    language: "jsx"
    stars: 220000
    description: "React library"
```

### Mineração Básica

```bash
# Minerar 50 triplas de todos os repositórios
python3 scripts/mine_repositories.py --max-triplets 50

# Minerar apenas TypeScript
python3 scripts/mine_repositories.py \
    --max-triplets 100 \
    --extensions .ts

# Minerar repositório específico
python3 scripts/mine_repositories.py \
    --repositories config/repositories.yaml \
    --repo-name vscode \
    --max-triplets 30

# Modo verboso (debug)
python3 scripts/mine_repositories.py \
    --max-triplets 20 \
    --verbose
```

### Estrutura de Saída

```
data/triplets/
├── triplet_001/
│   ├── base.ts          # Versão ancestral comum
│   ├── left.ts          # Parent 0 (primeira branch)
│   ├── right.ts         # Parent 1 (segunda branch)
│   └── metadata.txt     # Metadados (repo, commit, arquivo)
├── triplet_002/
│   ├── base.tsx
│   ├── left.tsx
│   ├── right.tsx
│   └── metadata.txt
...
```

**Exemplo de metadata.txt**:
```
Triplet ID: 1
Repository: vscode
Commit SHA: a1b2c3d4e5f6
Original File: src/vs/editor/common/model.ts
Extension: .ts
Base SHA: x1x2x3x4
Left SHA: y1y2y3y4
Right SHA: z1z2z3z4
```

### Validação de Triplas

```bash
# Verificar triplas mineradas
ls -l data/triplets/ | wc -l

# Verificar metadados
head data/triplets/triplet_001/metadata.txt

# Validar estrutura
python3 -c "
from pathlib import Path
triplets_dir = Path('data/triplets')
for triplet in triplets_dir.glob('triplet_*'):
    files = list(triplet.glob('*'))
    if len(files) != 4:
        print(f'❌ {triplet.name}: {len(files)} arquivos (esperado: 4)')
    else:
        print(f'✓ {triplet.name}')
"
```

---

## Execução de Experimentos

### Experimentos Básicos

```bash
# Executar em todas as triplas
python3 scripts/run_experiments.py

# Limitar número de triplas
python3 scripts/run_experiments.py --max-triplets 50

# Especificar ferramentas
python3 scripts/run_experiments.py \
    --tools csdiff-web diff3

# Com timeout customizado
python3 scripts/run_experiments.py \
    --timeout 120 \
    --max-triplets 100

# Especificar diretórios
python3 scripts/run_experiments.py \
    --triplets-dir data/triplets \
    --results-dir data/results

# Modo verboso
python3 scripts/run_experiments.py \
    --max-triplets 10 \
    --verbose
```

### Interpretando Saídas

**Console output**:
```
============================================================
EXECUTANDO EXPERIMENTOS
============================================================
Triplas: 50
Ferramentas: csdiff-web, diff3, mergiraf
Timeout: 60s
Resultados: data/results
============================================================

Executando experimentos: 100%|██████████| 50/50 [00:02<00:00, 21.45it/s]

============================================================
EXPERIMENTOS CONCLUÍDOS
============================================================
Triplas processadas: 50

Relatórios gerados:
  CSV:    data/results/results_20251213_120000.csv
  Resumo: data/results/summary_20251213_120000.txt
============================================================

MÉTRICAS RESUMIDAS:
------------------------------------------------------------

CSDIFF-WEB:
  Execuções bem-sucedidas: 48/50
  Taxa de sucesso:         96.0%
  Total de conflitos:      12
  Média de conflitos:      0.25
  Tempo médio:             0.006s

DIFF3:
  Execuções bem-sucedidas: 50/50
  Taxa de sucesso:         100.0%
  Total de conflitos:      18
  Média de conflitos:      0.36
  Tempo médio:             0.004s

============================================================
COMPARAÇÃO: CSDiff-Web vs diff3
============================================================
diff3:      18 conflitos
CSDiff-Web: 12 conflitos
Redução:    6 conflitos (33.3%)
============================================================
```

**Arquivo CSV** (`data/results/results_*.csv`):
```csv
triplet_id,filepath,extension,commit_sha,
csdiff_web_success,csdiff_web_has_conflict,csdiff_web_num_conflicts,csdiff_web_time,
diff3_success,diff3_has_conflict,diff3_num_conflicts,diff3_time
triplet_001,src/model.ts,.ts,a1b2c3d4,True,False,0,0.0052,True,False,0,0.0038
triplet_002,src/view.tsx,.tsx,e5f6g7h8,True,True,1,0.0067,True,True,1,0.0041
...
```

### Experimentos Programáticos

```python
from pathlib import Path
from src.runner.experiment_runner import ExperimentRunner

# Criar runner
runner = ExperimentRunner(
    triplets_dir=Path('data/triplets'),
    results_dir=Path('data/results'),
    timeout=60
)

# Executar
results = runner.run_experiments(
    max_triplets=50,
    tools=['csdiff-web', 'diff3']
)

# Acessar resultados
print(f"Triplas processadas: {results['triplets_processed']}")
print(f"CSV gerado: {results['csv_path']}")

# Métricas por ferramenta
for tool, metrics in results['metrics'].items():
    print(f"\n{tool.upper()}:")
    print(f"  Sucesso: {metrics['successful_executions']}/{metrics['total_executions']}")
    print(f"  Conflitos: {metrics['total_conflicts']}")
    print(f"  Tempo médio: {metrics['avg_time']:.3f}s")
```

---

## Análise de Resultados

### Análise Básica

```bash
# Analisar último CSV gerado
python3 scripts/analyze_results.py data/results/results_*.csv

# Especificar diretório de saída
python3 scripts/analyze_results.py \
    data/results/results_20251213_120000.csv \
    --output data/reports
```

### Interpretando Relatórios

**Console output**:
```
============================================================
ANÁLISE ESTATÍSTICA - CSDiff-Web
============================================================
Total de triplas: 50

============================================================
FALSE POSITIVES / FALSE NEGATIVES
============================================================

CSDIFF-WEB (baseline: diff3):
  True Positives:  10
  False Positives: 2
  True Negatives:  36
  False Negatives: 2

  Precision: 0.833
  Recall:    0.833
  F1-Score:  0.833
  Accuracy:  0.920

============================================================
COMPARAÇÃO DE CONFLITOS
============================================================

CSDIFF-WEB:
  Total de triplas:     50
  Com conflito:         12 (24.0%)
  Sem conflito:         38

DIFF3:
  Total de triplas:     50
  Com conflito:         18 (36.0%)
  Sem conflito:         32

REDUÇÃO (CSDiff-Web vs diff3):
  Absoluta: 6 conflitos
  Relativa: 33.3%

============================================================
TEMPO DE EXECUÇÃO
============================================================

CSDIFF-WEB:
  Média:   0.0063s
  Mediana: 0.0061s
  Min/Max: 0.0048s / 0.0092s

DIFF3:
  Média:   0.0041s
  Mediana: 0.0040s
  Min/Max: 0.0035s / 0.0051s
============================================================
```

**Relatório Markdown** (`data/reports/analysis_*.md`):
```markdown
# Análise Comparativa - CSDiff-Web vs diff3

**Data:** 2025-12-13 12:00:00
**Dataset:** 50 triplas

## 1. Análise de False Positives / False Negatives

| Métrica | Valor |
|---------|-------|
| Precision | 0.833 |
| Recall | 0.833 |
| F1-Score | 0.833 |
| Accuracy | 0.920 |

## 2. Redução de Conflitos

- **Redução absoluta:** 6 conflitos
- **Redução relativa:** 33.3%

➡️ CSDiff-Web apresentou redução significativa de conflitos.

## 5. Conclusões

1. CSDiff-Web reduziu conflitos em 33.3% comparado ao diff3.
2. Alta precisão (83.3%) indica poucos falsos positivos.
3. Overhead de performance aceitável (+53.7%).
```

**Tabela LaTeX** (`data/reports/table_*.tex`):
```latex
\begin{table}[htbp]
\centering
\caption{Comparação de Conflitos entre Ferramentas}
\label{tab:conflict_comparison}
\begin{tabular}{lrrr}
\hline
\textbf{Ferramenta} & \textbf{Total} & \textbf{Com Conflito} & \textbf{Taxa (\%)} \\
\hline
csdiff-web & 50 & 12 & 24.0 \\
diff3 & 50 & 18 & 36.0 \\
\hline
\end{tabular}
\end{table}
```

### Análise Programática

```python
from pathlib import Path
from src.analyzer.metrics_analyzer import MetricsAnalyzer
from src.analyzer.report_generator import ReportGenerator

# Carregar CSV
analyzer = MetricsAnalyzer(Path('data/results/results_20251213_120000.csv'))

# Gerar análise
summary = analyzer.generate_summary_report()

# Acessar métricas
fp_fn = summary['fp_fn_analysis']['csdiff-web']
print(f"Precision: {fp_fn['precision']:.2%}")
print(f"Recall: {fp_fn['recall']:.2%}")
print(f"F1-Score: {fp_fn['f1_score']:.2%}")

# Comparação de conflitos
conflicts = summary['conflict_comparison']
reduction = conflicts['reduction']
print(f"Redução: {reduction['absolute']} ({reduction['relative']:.1f}%)")

# Gerar relatórios
generator = ReportGenerator(Path('data/reports'))
md_report = generator.generate_markdown_report(summary)
latex_table = generator.generate_latex_table(summary)

print(f"Markdown: {md_report}")
print(f"LaTeX: {latex_table}")
```

---

## Integração em Código

### Caso 1: API de Merge

```python
from src.core.csdiff_web import CSDiffWeb

def merge_files(base_path, left_path, right_path):
    """Merge três arquivos usando CSDiff-Web."""
    merger = CSDiffWeb()

    # Ler arquivos
    base = open(base_path).read()
    left = open(left_path).read()
    right = open(right_path).read()

    # Merge
    result, has_conflict, num_conflicts = merger.merge(
        base, left, right,
        filename=base_path
    )

    if has_conflict:
        print(f"⚠ {num_conflicts} conflito(s) encontrado(s)")
    else:
        print(f"✓ Merge bem-sucedido sem conflitos")

    return result

# Uso
result = merge_files('base.ts', 'left.ts', 'right.ts')
print(result)
```

### Caso 2: Pipeline Completo

```python
from pathlib import Path
from src.miner.github_miner import GitHubMiner
from src.runner.experiment_runner import ExperimentRunner
from src.analyzer.metrics_analyzer import MetricsAnalyzer

def run_full_pipeline(repo_url, max_triplets=50):
    """Pipeline completo: Minerar → Experimentar → Analisar."""

    # FASE 1: Mineração
    print("FASE 1: Minerando repositório...")
    miner = GitHubMiner()
    mining_results = miner.mine_repository(
        repo_url=repo_url,
        output_dir=Path('data/triplets'),
        max_triplets=max_triplets
    )
    print(f"✓ {mining_results['triplets_extracted']} triplas extraídas")

    # FASE 2: Experimentos
    print("\nFASE 2: Executando experimentos...")
    runner = ExperimentRunner(
        triplets_dir=Path('data/triplets'),
        results_dir=Path('data/results')
    )
    exp_results = runner.run_experiments(
        max_triplets=max_triplets,
        tools=['csdiff-web', 'diff3']
    )
    print(f"✓ {exp_results['triplets_processed']} triplas processadas")

    # FASE 3: Análise
    print("\nFASE 3: Analisando resultados...")
    analyzer = MetricsAnalyzer(exp_results['csv_path'])
    summary = analyzer.generate_summary_report()

    # Imprimir resultados
    conflicts = summary['conflict_comparison']
    reduction = conflicts['reduction']

    print("\nRESULTADOS:")
    print(f"  diff3: {conflicts['diff3']['with_conflict']} conflitos")
    print(f"  CSDiff-Web: {conflicts['csdiff-web']['with_conflict']} conflitos")
    print(f"  Redução: {reduction['absolute']} ({reduction['relative']:.1f}%)")

    return summary

# Uso
summary = run_full_pipeline(
    'https://github.com/facebook/react.git',
    max_triplets=30
)
```

---

## Casos de Uso Avançados

### 1. Benchmark Customizado

```python
import time
from src.core.csdiff_web import CSDiffWeb
import subprocess

def benchmark_merge_tools(base, left, right, filename, iterations=100):
    """Compara performance de CSDiff-Web vs diff3."""

    # Benchmark CSDiff-Web
    csdiff = CSDiffWeb()
    start = time.time()
    for _ in range(iterations):
        result, _, _ = csdiff.merge(base, left, right, filename)
    csdiff_time = (time.time() - start) / iterations

    # Benchmark diff3 (via subprocess)
    # [Implementação simplificada]

    print(f"CSDiff-Web: {csdiff_time*1000:.2f}ms")
    print(f"Overhead: {(csdiff_time/diff3_time - 1)*100:.1f}%")
```

### 2. Análise de Sensibilidade

```python
from src.core.csdiff_web import CSDiffWeb

def test_different_separators(code_base, code_left, code_right):
    """Testa impacto de diferentes conjuntos de separadores."""

    separator_sets = [
        ['{', '}', ';'],              # Mínimo
        ['{', '}', '[', ']', ';'],    # Básico
        ['{', '}', '[', ']', '(', ')', ';', ',']  # Completo
    ]

    for seps in separator_sets:
        # [Configurar separadores customizados]
        merger = CSDiffWeb()
        result, has_conflict, num_conflicts = merger.merge(
            code_base, code_left, code_right, "test.ts"
        )
        print(f"Separadores: {seps}")
        print(f"  Conflitos: {num_conflicts}")
```

### 3. Análise de Correlação

```python
import pandas as pd
import matplotlib.pyplot as plt

def analyze_correlations(csv_path):
    """Analisa correlações entre métricas."""

    df = pd.read_csv(csv_path)

    # Correlação: tamanho do arquivo vs tempo
    # Correlação: número de conflitos vs taxa de sucesso
    # etc.

    correlations = df[['csdiff_web_num_conflicts', 'csdiff_web_time']].corr()
    print(correlations)

    # Gráfico
    plt.scatter(df['csdiff_web_num_conflicts'], df['csdiff_web_time'])
    plt.xlabel('Número de Conflitos')
    plt.ylabel('Tempo (s)')
    plt.title('Correlação Conflitos vs Tempo')
    plt.savefig('correlation.png')
```

---

## Troubleshooting

### Problema: diff3 não encontrado

**Erro**:
```
FileNotFoundError: [Errno 2] No such file or directory: 'diff3'
```

**Solução**:
```bash
# Linux (Debian/Ubuntu)
sudo apt-get install diffutils

# macOS
brew install diffutils

# Verificar
diff3 --version
```

### Problema: Mergiraf não disponível

**Aviso**:
```
Mergiraf não disponível - pulando
```

**Solução** (opcional):
```bash
# Instalar Mergiraf
pip3 install mergiraf

# Verificar
mergiraf --version
```

**Nota**: Mergiraf é opcional. O sistema funciona sem ele.

### Problema: Triplas não encontradas

**Erro**:
```
❌ Nenhuma tripla encontrada em data/triplets
```

**Solução**:
```bash
# Minerar triplas primeiro
python3 scripts/mine_repositories.py --max-triplets 10

# Verificar
ls -l data/triplets/
```

### Problema: Timeout em experimentos

**Erro**:
```
Timeout após 60s
```

**Solução**:
```bash
# Aumentar timeout
python3 scripts/run_experiments.py --timeout 120

# Ou excluir arquivos grandes
# [Implementar filtro de tamanho na mineração]
```

### Problema: Encoding de arquivos

**Erro**:
```
UnicodeDecodeError: 'utf-8' codec can't decode
```

**Solução**:
- Verificar encoding do arquivo
- Adicionar fallback para latin-1 ou outros encodings
- Pular arquivos com encoding problemático

### Problema: Pandas/Numpy não instalado

**Erro**:
```
ModuleNotFoundError: No module named 'pandas'
```

**Solução**:
```bash
pip3 install -r requirements.txt

# Ou instalar manualmente
pip3 install pandas numpy pyyaml tqdm gitpython
```

---

## Dicas e Boas Práticas

### 1. Começe com Dataset Pequeno

```bash
# Teste com 10 triplas primeiro
python3 scripts/mine_repositories.py --max-triplets 10
python3 scripts/run_experiments.py --max-triplets 10

# Depois escale
python3 scripts/mine_repositories.py --max-triplets 100
```

### 2. Use Modo Verboso para Debug

```bash
python3 scripts/run_experiments.py --max-triplets 5 --verbose
```

### 3. Valide Triplas Antes de Experimentar

```bash
# Verificar qualidade das triplas
python3 -c "
from pathlib import Path
for triplet in Path('data/triplets').glob('triplet_*'):
    base = (triplet / 'base.ts').read_text()
    print(f'{triplet.name}: {len(base)} bytes')
"
```

### 4. Salve Configurações de Experimentos

```bash
# Criar script de experimento
cat > run_my_experiment.sh <<'EOF'
#!/bin/bash
python3 scripts/mine_repositories.py --max-triplets 100 --extensions .ts
python3 scripts/run_experiments.py --max-triplets 100 --timeout 120
python3 scripts/analyze_results.py data/results/results_*.csv
EOF

chmod +x run_my_experiment.sh
./run_my_experiment.sh
```

### 5. Documente Resultados

```bash
# Copiar relatórios com nome descritivo
cp data/reports/analysis_*.md results_react_100_triplets.md
cp data/reports/table_*.tex table_react_100_triplets.tex
```

---

## Próximos Passos

Após dominar este guia:

1. **Escalar experimentos**: Minerar 200+ triplas de múltiplos repositórios
2. **Análise comparativa**: Incluir Mergiraf nos experimentos
3. **Visualizações**: Criar gráficos e charts (matplotlib, seaborn)
4. **Publicação**: Gerar relatório científico para TCC

---

**Última atualização**: 2025-12-13
**Versão**: 1.0 (Marco M5 completo)
