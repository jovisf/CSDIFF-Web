# Changelog - CSDiff-Web

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [Unreleased]

### Planejado
- Docker container para reprodutibilidade
- Visualizações gráficas (matplotlib/seaborn)
- Interface web para demonstrações
- Suporte para Python (.py)
- Suporte para Go (.go)

---

## [1.0.0] - 2025-12-13

### Marco M5: Analyzer - Análise Estatística Completa

Implementação completa do módulo de análise estatística e geração de relatórios científicos.

#### Adicionado
- **Analyzer Módulo** (`src/analyzer/`)
  - `metrics_analyzer.py`: Cálculo de FP/FN, precision, recall, F1-score
  - `report_generator.py`: Geração de relatórios Markdown e tabelas LaTeX
  - Análise de distribuição de conflitos (0, 1, 2, 3+ conflitos)
  - Análise de performance (tempo médio, mediana, desvio padrão)

- **Scripts de Análise**
  - `scripts/analyze_results.py`: CLI para análise de resultados CSV
  - `examples/simple_analysis.py`: Demo completo do Analyzer

- **Documentação Completa**
  - `docs/ARCHITECTURE.md`: Documentação técnica da arquitetura (5000+ linhas)
  - `docs/USAGE_GUIDE.md`: Guia completo de uso com exemplos
  - Atualização do README.md principal

- **Métricas Estatísticas**
  - False Positives/Negatives usando diff3 como baseline
  - Precision, Recall, F1-Score, Accuracy
  - Comparação de taxas de conflito
  - Overhead de performance

- **Relatórios Científicos**
  - Formato Markdown com tabelas formatadas
  - Tabelas LaTeX prontas para papers
  - Conclusões automáticas baseadas em thresholds
  - Metadados completos (data, dataset, ferramentas)

#### Mudado
- Roadmap atualizado com todos os 5 marcos concluídos
- README expandido com seções de Runner e Analyzer

#### Corrigido
- Estrutura de dicionário `reduction` no analyzer (relative vs percentage)
- Estrutura de dicionário `execution_time` (mean vs avg)
- Referências de chaves em exemplos

---

## [0.4.0] - 2025-12-13

### Marco M4: Runner - Orquestrador de Experimentos

Implementação do sistema de execução e comparação de experimentos.

#### Adicionado
- **Runner Módulo** (`src/runner/`)
  - `tool_executor.py`: Execução de CSDiff-Web, diff3, Mergiraf
  - `result_collector.py`: Coleta de métricas e geração de CSV
  - `experiment_runner.py`: Orquestrador principal

- **Scripts de Execução**
  - `scripts/run_experiments.py`: CLI para executar experimentos
  - `examples/simple_experiments.py`: Demo com triplas sintéticas

- **Métricas Coletadas**
  - Sucesso/falha de cada ferramenta
  - Número de conflitos detectados
  - Tempo de execução
  - Mensagens de erro

- **Saídas Geradas**
  - CSV detalhado por tripla
  - Resumo estatístico textual
  - Métricas agregadas por ferramenta

#### Features
- Execução sequencial de múltiplas ferramentas
- Timeout configurável por execução (padrão: 60s)
- Tratamento de erros robusto
- Barra de progresso (tqdm)
- Logging verboso opcional

#### Testado
- 4 triplas sintéticas com cenários diversos
- 100% de taxa de sucesso
- Comparação CSDiff-Web vs diff3

---

## [0.3.0] - 2025-12-13

### Marco M3: Miner - Mineração de Repositórios

Implementação completa do sistema de mineração de merge commits do GitHub.

#### Adicionado
- **Miner Módulo** (`src/miner/`)
  - `commit_filter.py`: Filtragem de merge commits válidos
  - `triplet_extractor.py`: Extração de triplas (base, left, right)
  - `github_miner.py`: Orquestrador de mineração

- **Configuração de Repositórios**
  - `config/repositories.yaml`: 26 repositórios de alta qualidade
  - Categorias: TypeScript (7), TSX (6), JavaScript (6), JSX (4), Mixed (3)
  - Total: 2M+ GitHub stars

- **Scripts de Mineração**
  - `scripts/mine_repositories.py`: CLI para mineração
  - Suporte a múltiplos repositórios em paralelo
  - Filtros configuráveis por extensão

- **Validação**
  - Filtro CRÍTICO: EXATAMENTE 2 pais (orientação Prof. Paulo Borba)
  - Verificação de modificação bilateral
  - Detecção de arquivos minificados
  - Validação de estrutura de triplas

#### Features
- Clonagem automática de repositórios
- Extração de metadados completos (commit SHA, arquivo, repo)
- Estatísticas de mineração
- Modo verboso para debugging

#### Repositórios Configurados
- microsoft/vscode (162k stars)
- facebook/react (220k stars)
- vercel/next.js (120k stars)
- angular/angular (95k stars)
- nodejs/node (104k stars)
- E mais 21 repositórios

---

## [0.2.0] - 2025-12-13

### Marco M2: Testes - Cobertura Completa

Implementação de testes unitários e de integração.

#### Adicionado
- **Testes do Core** (`tests/test_core/`)
  - `test_separators.py`: 6 testes
  - `test_filters.py`: 4 testes
  - `test_preprocessor.py`: 3 testes
  - `test_alignment.py`: 3 testes
  - `test_postprocessor.py`: 2 testes
  - `test_csdiff_web.py`: 3 testes integração

- **Cobertura**
  - 21 testes unitários
  - 100% passing
  - Cobertura > 80% do código Core

- **CI/CD**
  - Configuração pytest
  - Fixtures compartilhados
  - Testes parametrizados

#### Features
- Testes de casos extremos (strings, escapes, edge cases)
- Validação de marcadores contextuais
- Testes de integração end-to-end

---

## [0.1.0] - 2025-12-13

### Marco M1: Core - Pipeline Funcional

Implementação inicial do pipeline de merge estruturado.

#### Adicionado
- **Core Pipeline** (`src/core/`)
  - `separators.py`: Definição de separadores por extensão
  - `filters.py`: Detecção de arquivos minificados
  - `preprocessor.py`: Explosão de código com detecção de strings
  - `alignment_resolver.py`: Solução para Alignment Problem
  - `postprocessor.py`: Reconstrução de código
  - `csdiff_web.py`: Orquestrador principal

- **Suporte a Linguagens**
  - TypeScript (.ts)
  - TSX (.tsx)
  - JavaScript (.js)
  - JSX (.jsx)

- **Features Principais**
  - Separadores sintáticos configuráveis
  - Detecção de strings literais (single, double, template)
  - Marcadores contextuais únicos (depth + hash MD5)
  - Preservação de formatação
  - Contagem de conflitos

- **Documentação Inicial**
  - README.md básico
  - Exemplos de uso
  - Comentários inline

#### Algoritmos Implementados
- Explosão greedy com detecção de strings
- Cálculo de profundidade para marcadores
- Hash contextual MD5 (6 dígitos)
- Reconstrução preservando conflitos do diff3

#### Decisões de Design
- Usar separadores textuais (não AST parsing)
- diff3 como ferramenta base
- Marcadores removíveis após merge
- Execução via arquivos temporários

---

## [0.0.1] - 2025-12-10

### Projeto Iniciado

#### Adicionado
- Estrutura inicial do projeto
- Configuração Git
- requirements.txt básico
- .gitignore

#### Contexto
- TCC em Ciência da Computação - UFPE
- Orientador: Prof. Paulo Borba
- Baseado no CSDiff original (Java)
- Extensão para ecossistema Web (TypeScript/JavaScript/JSX/TSX)

---

## Notas de Versão

### Versionamento

- **MAJOR**: Mudanças incompatíveis na API
- **MINOR**: Novos recursos mantendo compatibilidade
- **PATCH**: Correções de bugs

### Marcos do Projeto

| Marco | Versão | Status | Data |
|-------|--------|--------|------|
| M1: Core Funcional | 0.1.0 | ✅ Completo | 2025-12-13 |
| M2: Testes | 0.2.0 | ✅ Completo | 2025-12-13 |
| M3: Miner | 0.3.0 | ✅ Completo | 2025-12-13 |
| M4: Runner | 0.4.0 | ✅ Completo | 2025-12-13 |
| M5: Analyzer | 1.0.0 | ✅ Completo | 2025-12-13 |

### Estatísticas do Projeto

**Código implementado**:
- Core: ~1,207 linhas (6 módulos)
- Miner: ~889 linhas (3 módulos)
- Runner: ~1,030 linhas (3 módulos)
- Analyzer: ~450 linhas (2 módulos)
- **Total**: ~3,576 linhas de código Python

**Testes**:
- 21 testes unitários (Core)
- 100% passing
- Cobertura > 80%

**Documentação**:
- README.md principal
- ARCHITECTURE.md (~5,000 linhas)
- USAGE_GUIDE.md (~800 linhas)
- Comentários inline em código

**Repositórios configurados**: 26
**Total GitHub stars**: 2M+

---

## Próximas Versões Planejadas

### [1.1.0] - Visualizações
- Gráficos de barras (conflitos por ferramenta)
- Histogramas de distribuição
- Scatter plots (tempo vs conflitos)
- Heatmaps de correlação

### [1.2.0] - Docker
- Dockerfile para ambiente completo
- Docker Compose para orquestração
- Scripts de setup automatizado
- Documentação de deployment

### [1.3.0] - Novas Linguagens
- Suporte para Python (.py)
- Suporte para Go (.go)
- Suporte para Ruby (.rb)

### [2.0.0] - Publicação
- Artigo científico
- Apresentação de TCC
- Release final
- DOI/Zenodo

---

**Mantenedor**: João Victor
**Instituição**: UFPE - Centro de Informática
**Orientador**: Prof. Paulo Borba
**Ano**: 2025
