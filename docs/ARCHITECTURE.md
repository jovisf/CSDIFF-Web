# Arquitetura do CSDiff-Web

Este documento descreve a arquitetura completa do CSDiff-Web, incluindo módulos, fluxos de dados e decisões de design.

## Visão Geral

CSDiff-Web é organizado em 4 módulos principais que formam um pipeline científico completo:

```
┌──────────────┐
│   MINER      │  Extrai triplas (base, left, right) de merge commits reais
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   CORE       │  Pipeline de merge estruturado com separadores
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   RUNNER     │  Orquestra experimentos comparativos (3 ferramentas)
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  ANALYZER    │  Análise estatística e relatórios científicos
└──────────────┘
```

---

## Módulo 1: CORE (Pipeline de Merge)

**Localização**: `src/core/`

### Componentes

#### 1.1 Separators ([separators.py](../src/core/separators.py))

**Responsabilidade**: Define separadores sintáticos por extensão de arquivo.

**API Principal**:
```python
def get_separators(extension: str) -> List[str]
```

**Separadores configurados**:
- `.ts`, `.js`: `{`, `}`, `[`, `]`, `(`, `)`, `;`, `,`, `=>`, `??`
- `.tsx`, `.jsx`: Todos acima + `<`, `>`, `</`, `/>`, `{}`, `className=`

**Design**: Separadores ordenados por comprimento (maior → menor) para matching greedy correto.

#### 1.2 Filters ([filters.py](../src/core/filters.py))

**Responsabilidade**: Detecta e rejeita arquivos minificados.

**API Principal**:
```python
def is_minified(code: str, filename: str) -> bool
```

**Heurísticas**:
1. Nome contém `.min.`, `.bundle.`, `-min.`
2. Linha > 500 caracteres
3. Comprimento médio > 200 caracteres
4. Proporção linhas longas > 50%

#### 1.3 Preprocessor ([preprocessor.py](../src/core/preprocessor.py))

**Responsabilidade**: "Explode" código em múltiplas linhas nos separadores.

**API Principal**:
```python
def preprocess(code: str, separators: List[str]) -> str
```

**Algoritmo**:
1. Itera sobre código caractere por caractere
2. Para cada posição, verifica se há match com algum separador
3. **CRÍTICO**: Pula separadores dentro de strings literais
4. Insere `\n` antes do separador encontrado
5. Retorna código explodido

**Detecção de strings**:
- Suporta: `'...'`, `"..."`, `` `...` ``
- Detecta escapes: `\'`, `\"`, `` \` ``
- Não quebra separadores dentro de strings

**Exemplo**:
```typescript
// Input
function foo() { return x; }

// Output (explodido)
function foo(
) {
 return x;
 }
```

#### 1.4 Alignment Resolver ([alignment_resolver.py](../src/core/alignment_resolver.py))

**Responsabilidade**: Resolve o **Alignment Problem** adicionando marcadores contextuais únicos.

**Problema**:
Após explosão, muitas linhas idênticas (`{`, `}`, `;`) confundem diff3, causando alinhamentos incorretos.

**Solução**:
Adiciona marcadores únicos baseados em:
- **Profundidade de aninhamento** (depth)
- **Hash MD5 do contexto** precedente (6 dígitos)

**API Principal**:
```python
def add_markers(code: str) -> str
def remove_markers(code: str) -> str
```

**Formato do marcador**:
```
§§CSDIFF_<depth>_<hash>§§<token>
```

**Exemplo**:
```
§§CSDIFF_0_a1b2c3§§{       // Depth 0, contexto único
§§CSDIFF_1_d4e5f6§§{       // Depth 1, contexto diferente
```

**Cálculo de hash**:
- Janela de 50 caracteres precedentes
- MD5 truncado em 6 dígitos hex
- Garante unicidade por contexto

#### 1.5 Postprocessor ([postprocessor.py](../src/core/postprocessor.py))

**Responsabilidade**: Reconstrói código original após diff3.

**API Principal**:
```python
def postprocess(exploded: str) -> str
def count_conflicts(code: str) -> Tuple[bool, int]
```

**Algoritmo de reconstrução**:
1. Remove marcadores contextuais (`§§CSDIFF_...§§`)
2. Concatena linhas sequenciais não-vazias
3. Preserva marcadores de conflito do diff3:
   - `<<<<<<<`
   - `=======`
   - `>>>>>>>`
4. Preserva linhas vazias originais

**Contagem de conflitos**:
- Conta blocos `<<<<<<<` ... `>>>>>>>`
- Retorna: (has_conflict: bool, num_conflicts: int)

#### 1.6 CSDiff-Web Core ([csdiff_web.py](../src/core/csdiff_web.py))

**Responsabilidade**: Orquestrador principal do pipeline.

**API Principal**:
```python
def merge(
    base: str,
    left: str,
    right: str,
    filename: str = ""
) -> Tuple[str, bool, int]
```

**Retorno**: `(result, has_conflict, num_conflicts)`

**Pipeline**:
```
1. Detectar extensão
2. [Filters] Rejeitar se minificado
3. Obter separadores
4. [Preprocessor] Explodir código
5. [AlignmentResolver] Adicionar marcadores
6. Escrever arquivos temporários
7. Executar diff3
8. Ler resultado
9. [AlignmentResolver] Remover marcadores
10. [Postprocessor] Reconstruir código
11. Contar conflitos
12. Retornar resultado
```

**Execução do diff3**:
```bash
diff3 -m left_temp base_temp right_temp
```

---

## Módulo 2: MINER (Mineração de Repositórios)

**Localização**: `src/miner/`

### Componentes

#### 2.1 Commit Filter ([commit_filter.py](../src/miner/commit_filter.py))

**Responsabilidade**: Filtra merge commits válidos.

**API Principal**:
```python
def is_valid_merge_commit(commit: Commit) -> bool
```

**Critérios CRÍTICOS** (orientação do Prof. Paulo Borba):
1. **EXATAMENTE 2 pais** (não 3+)
2. **Não fast-forward** (deve haver merge real)
3. Modificações em ambos os lados
4. Arquivos com extensões suportadas

**Estatísticas coletadas**:
- Total de commits analisados
- Merge commits encontrados
- Merge commits válidos
- Commits rejeitados por motivo

#### 2.2 Triplet Extractor ([triplet_extractor.py](../src/miner/triplet_extractor.py))

**Responsabilidade**: Extrai triplas (base, left, right) de merge commits.

**API Principal**:
```python
def extract_triplets_from_commit(
    commit: Commit,
    extensions: List[str]
) -> List[Triplet]
```

**Algoritmo**:
1. Para cada arquivo modificado no merge commit:
   - Verificar extensão suportada
   - Verificar modificação em AMBOS os lados (left E right)
   - Extrair versões: base (ancestral), left (parent 0), right (parent 1)
   - Criar objeto Triplet com metadados

**Triplet estrutura**:
```python
{
    'base': str,           # Código ancestral comum
    'left': str,           # Versão do parent 0
    'right': str,          # Versão do parent 1
    'filepath': str,       # Caminho do arquivo
    'extension': str,      # Extensão (.ts, .tsx, etc)
    'commit_sha': str,     # SHA do merge commit
    'repo': str            # Nome do repositório
}
```

**Filtros aplicados**:
- Arquivos muito grandes (> 10MB)
- Arquivos binários
- Arquivos sem modificação bilateral

#### 2.3 GitHub Miner ([github_miner.py](../src/miner/github_miner.py))

**Responsabilidade**: Orquestrador de mineração completo.

**API Principal**:
```python
def mine_repository(
    repo_url: str,
    output_dir: Path,
    max_triplets: int = 100
) -> MiningResults
```

**Pipeline**:
```
1. Clonar repositório (ou atualizar se existir)
2. Iterar commits na branch principal
3. [CommitFilter] Filtrar merge commits válidos
4. [TripletExtractor] Extrair triplas
5. Salvar triplas em diretórios:
   - triplet_001/base.ts
   - triplet_001/left.ts
   - triplet_001/right.ts
   - triplet_001/metadata.txt
6. Gerar estatísticas
```

**Configuração**: `config/repositories.yaml`
- 26 repositórios curados
- Categorias: TypeScript, TSX, JavaScript, JSX, Mixed
- Total: ~2M+ GitHub stars

---

## Módulo 3: RUNNER (Orquestrador de Experimentos)

**Localização**: `src/runner/`

### Componentes

#### 3.1 Tool Executor ([tool_executor.py](../src/runner/tool_executor.py))

**Responsabilidade**: Executa ferramentas de merge e coleta métricas.

**Ferramentas suportadas**:
1. **CSDiff-Web** - Implementação própria
2. **diff3** - Baseline padrão
3. **Mergiraf** - Merge estruturado (opcional)

**API Principal**:
```python
def execute_all(
    base: str, left: str, right: str,
    extension: str, filename: str,
    base_file: Path, left_file: Path, right_file: Path
) -> Dict[str, ToolResult]
```

**ToolResult estrutura**:
```python
{
    'success': bool,
    'has_conflict': bool,
    'num_conflicts': int,
    'execution_time': float,
    'result': str,
    'error': Optional[str]
}
```

**Execução**:
- **CSDiff-Web**: Via API Python
- **diff3**: Comando shell `diff3 -m`
- **Mergiraf**: Comando shell `mergiraf merge`

**Timeout**: Configurável (padrão 60s)

#### 3.2 Result Collector ([result_collector.py](../src/runner/result_collector.py))

**Responsabilidade**: Coleta resultados e gera relatórios.

**API Principal**:
```python
def add_result(
    triplet_id: str,
    triplet_metadata: Dict,
    tool_results: Dict[str, ToolResult]
)

def generate_csv(filename: str = None) -> Path
def generate_summary(filename: str = None) -> Path
```

**Formato CSV**:
```csv
triplet_id,filepath,extension,commit_sha,
csdiff_web_success,csdiff_web_has_conflict,csdiff_web_num_conflicts,csdiff_web_time,csdiff_web_error,
diff3_success,diff3_has_conflict,diff3_num_conflicts,diff3_time,diff3_error,
mergiraf_success,mergiraf_has_conflict,mergiraf_num_conflicts,mergiraf_time,mergiraf_error
```

**Métricas agregadas**:
- Total de execuções por ferramenta
- Taxa de sucesso
- Total/média de conflitos
- Tempo médio/min/max

#### 3.3 Experiment Runner ([experiment_runner.py](../src/runner/experiment_runner.py))

**Responsabilidade**: Orquestrador principal de experimentos.

**API Principal**:
```python
def run_experiments(
    max_triplets: Optional[int] = None,
    tools: List[str] = ['csdiff-web', 'diff3', 'mergiraf']
) -> ExperimentResults
```

**Pipeline**:
```
1. Carregar triplas de data/triplets/
2. Para cada tripla:
   - [ToolExecutor] Executar ferramentas
   - [ResultCollector] Coletar métricas
3. Gerar CSV consolidado
4. Gerar resumo textual
5. Calcular estatísticas globais
```

**Saídas**:
- `results_TIMESTAMP.csv` - Dados brutos
- `summary_TIMESTAMP.txt` - Resumo estatístico

---

## Módulo 4: ANALYZER (Análise Estatística)

**Localização**: `src/analyzer/`

### Componentes

#### 4.1 Metrics Analyzer ([metrics_analyzer.py](../src/analyzer/metrics_analyzer.py))

**Responsabilidade**: Análise estatística profunda dos resultados.

**API Principal**:
```python
def calculate_fp_fn(
    tool_col: str,
    baseline_col: str = 'diff3_has_conflict'
) -> Dict

def compare_conflict_rates() -> Dict
def analyze_conflict_distribution() -> Dict
def analyze_execution_time() -> Dict
def generate_summary_report() -> Dict
```

**Análises realizadas**:

**1. False Positives/False Negatives**:
- Baseline: diff3 (ground truth)
- Matriz de confusão: TP, FP, TN, FN
- Métricas: Precision, Recall, F1-Score, Accuracy

```
TP: Ambos detectam conflito
FP: CSDiff detecta, diff3 não (falso positivo)
TN: Nenhum detecta conflito
FN: diff3 detecta, CSDiff não (falso negativo)
```

**2. Comparação de conflitos**:
- Taxa de conflito por ferramenta
- Redução absoluta e relativa (CSDiff vs diff3)

**3. Distribuição de conflitos**:
- Casos com 0 conflitos
- Casos com 1 conflito
- Casos com 2 conflitos
- Casos com 3+ conflitos

**4. Performance**:
- Tempo médio, mediana, desvio padrão
- Min/Max por ferramenta
- Overhead do CSDiff vs diff3

#### 4.2 Report Generator ([report_generator.py](../src/analyzer/report_generator.py))

**Responsabilidade**: Gera relatórios científicos formatados.

**API Principal**:
```python
def generate_markdown_report(
    summary: Dict,
    filename: str = None
) -> Path

def generate_latex_table(
    summary: Dict,
    filename: str = None
) -> Path
```

**Relatório Markdown**:
- Seções: FP/FN, Conflitos, Distribuição, Performance, Conclusões
- Tabelas formatadas
- Interpretação automática (baseada em thresholds)
- Metadados (data, dataset, ferramentas)

**Tabela LaTeX**:
- Formato: `\begin{table}...\end{table}`
- Pronta para inclusão em papers
- Labels e captions configuráveis

**Conclusões automáticas**:
- Redução de conflitos > 20%: "Redução significativa"
- Redução 5-20%: "Redução moderada"
- Redução < 5%: "Desempenho similar"
- Precision > 90%: "Alta precisão"
- Overhead < 2x: "Aceitável para uso prático"

---

## Fluxos de Dados

### Fluxo 1: Pipeline Completo (Mineração → Análise)

```
┌─────────────────────────────────────────────────────────────┐
│ FASE 1: MINERAÇÃO                                          │
└─────────────────────────────────────────────────────────────┘
  python3 scripts/mine_repositories.py --max-triplets 100
                          ↓
         Clona repos do GitHub
                          ↓
         Filtra merge commits válidos (EXATAMENTE 2 pais)
                          ↓
         Extrai triplas (base, left, right)
                          ↓
         Salva em data/triplets/triplet_NNN/

┌─────────────────────────────────────────────────────────────┐
│ FASE 2: EXPERIMENTOS                                       │
└─────────────────────────────────────────────────────────────┘
  python3 scripts/run_experiments.py --tools csdiff-web diff3
                          ↓
         Carrega triplas de data/triplets/
                          ↓
         Para cada tripla:
           - Executa CSDiff-Web
           - Executa diff3
           - Executa Mergiraf (opcional)
           - Coleta métricas (conflitos, tempo)
                          ↓
         Gera CSV consolidado: data/results/results_*.csv
         Gera resumo: data/results/summary_*.txt

┌─────────────────────────────────────────────────────────────┐
│ FASE 3: ANÁLISE                                             │
└─────────────────────────────────────────────────────────────┘
  python3 scripts/analyze_results.py data/results/results_*.csv
                          ↓
         Carrega CSV com pandas
                          ↓
         Calcula FP/FN (baseline: diff3)
         Calcula métricas (precision, recall, F1)
         Compara taxas de conflito
         Analisa distribuição
         Analisa performance
                          ↓
         Gera relatório MD: data/reports/analysis_*.md
         Gera tabela LaTeX: data/reports/table_*.tex
```

### Fluxo 2: Pipeline Core (Merge de Arquivo Único)

```
Input: (base, left, right, filename)
         ↓
┌────────────────────┐
│  CORE PIPELINE     │
└────────────────────┘
         ↓
[1] Detectar extensão (.ts, .tsx, .js, .jsx)
         ↓
[2] Filters: Rejeitar se minificado
         ↓
[3] Obter separadores para extensão
         ↓
[4] Preprocessor: Explodir código
    - Detecta strings literais
    - Insere \n antes de separadores
         ↓
[5] AlignmentResolver: Adicionar marcadores
    - Calcula depth (profundidade)
    - Calcula hash MD5 do contexto
    - Formata: §§CSDIFF_<depth>_<hash>§§<token>
         ↓
[6] Escrever arquivos temporários
         ↓
[7] Executar diff3 -m left_temp base_temp right_temp
         ↓
[8] Ler resultado do diff3
         ↓
[9] AlignmentResolver: Remover marcadores
         ↓
[10] Postprocessor: Reconstruir
     - Remove marcadores
     - Concatena linhas
     - Preserva conflitos do diff3
         ↓
[11] Contar conflitos (<<<<<<<...>>>>>>>)
         ↓
Output: (result, has_conflict, num_conflicts)
```

---

## Decisões de Design

### 1. Por que não parsing de AST?

**Decisão**: Usar separadores textuais em vez de AST parsing.

**Razões**:
- ✅ Simplicidade: Não requer parser completo de TypeScript/JavaScript
- ✅ Robustez: Funciona com código sintaticamente incorreto
- ✅ Performance: Muito mais rápido que parsing de AST
- ✅ Preservação: Mantém formatação e comentários intactos
- ✅ Flexibilidade: Fácil adicionar suporte a novas linguagens

**Trade-off**: Menos preciso que abordagens estruturadas (ex: Mergiraf)

### 2. Por que diff3 como baseline?

**Decisão**: Usar diff3 como ground truth para análise FP/FN.

**Razões**:
- ✅ Padrão de facto em sistemas de controle de versão (Git)
- ✅ Comportamento bem documentado e testado
- ✅ Amplamente usado na indústria
- ✅ Permite comparação com estado da arte

**Alternativa considerada**: Usar análise manual (muito custoso)

### 3. Por que marcadores contextuais?

**Decisão**: Adicionar marcadores únicos com depth + hash MD5.

**Problema resolvido**: Alignment Problem
- Explosão gera muitas linhas idênticas (`{`, `}`, `;`)
- diff3 pode alinhar incorretamente

**Solução**:
- Depth: Garante que `{` de níveis diferentes sejam únicos
- Hash: Garante que `{` de contextos diferentes sejam únicos

**Alternativa rejeitada**: Números sequenciais (não sobrevivem a modificações)

### 4. Por que execução sequencial?

**Decisão**: Processar triplas uma por vez (não paralelo).

**Razões**:
- ✅ Simplicidade de implementação
- ✅ Facilita debug e rastreamento
- ✅ Performance adequada (~0.006s por tripla)
- ✅ Evita race conditions em I/O

**Trade-off**: Não aproveita múltiplos cores (aceitável para dataset < 1000 triplas)

### 5. Por que EXATAMENTE 2 pais?

**Decisão**: Filtrar apenas merge commits com exatamente 2 pais.

**Razões** (orientação Prof. Paulo Borba):
- ✅ Octopus merges (3+ pais) são raros e atípicos
- ✅ Simplifica análise (sempre 2 branches)
- ✅ Alinha com caso de uso mais comum (feature branch → main)

### 6. Por que Python?

**Decisão**: Implementar em Python 3.8+.

**Razões**:
- ✅ Ecossistema científico maduro (pandas, numpy)
- ✅ Fácil integração com ferramentas existentes
- ✅ Prototipagem rápida
- ✅ GitPython para manipulação de repositórios

**Trade-off**: Performance inferior a linguagens compiladas (aceitável)

---

## Métricas de Qualidade

### Cobertura de Testes

- **Core**: 21 testes unitários (100% passing)
- **Miner**: Testado com repos sintéticos
- **Runner**: Testado com triplas sintéticas
- **Analyzer**: Testado com CSVs sintéticos

**Meta**: Cobertura > 80% (atingida no Core)

### Performance

- **CSDiff-Web**: ~0.006s por arquivo
- **diff3**: ~0.004s por arquivo
- **Overhead**: ~47% (aceitável)

**Meta**: Overhead < 2x (atingida)

### Escalabilidade

- **Testado**: Até 100 triplas simultaneamente
- **Estimado**: Suporta até 1000 triplas sem otimizações
- **Gargalo**: I/O de disco (arquivos temporários)

---

## Extensibilidade

### Adicionar Nova Linguagem

1. Editar `src/core/separators.py`:
   ```python
   SEPARATORS['.nova'] = ['{', '}', ';', '->']
   ```

2. Criar testes em `tests/test_core/test_separators.py`

3. Validar com exemplos reais

### Adicionar Nova Ferramenta de Merge

1. Editar `src/runner/tool_executor.py`:
   ```python
   def _execute_nova_tool(self, ...):
       # Implementação
   ```

2. Adicionar à lista de ferramentas em `execute_all()`

3. Atualizar `ResultCollector` para coletar métricas

### Adicionar Nova Métrica

1. Editar `src/analyzer/metrics_analyzer.py`:
   ```python
   def calculate_nova_metric(self) -> Dict:
       # Cálculo
   ```

2. Adicionar ao `generate_summary_report()`

3. Atualizar `ReportGenerator` para exibir

---

## Referências Técnicas

- **Git diff3**: https://git-scm.com/docs/git-merge-file
- **Mergiraf**: https://github.com/qundao/mergiraf
- **CSDiff original**: Pesquisa SPGroup/UFPE
- **Alignment Problem**: TCC Leonardo dos Anjos Silva (2025)

---

**Última atualização**: 2025-12-13
**Marco atual**: M5 (Analyzer) concluído ✅
