# CSDiff-Web: Merge Textual com Separadores Sintáticos para Web

**Projeto de Graduação | Orientador: Prof. Paulo Borba (UFPE)**

CSDiff-Web é uma ferramenta de merge textual que estende a abordagem do CSDiff para o ecossistema Web (TypeScript, JavaScript, JSX, TSX). A ferramenta "explode" código em múltiplas linhas usando separadores sintáticos, permitindo que o diff3 opere em granularidade mais fina que linhas de texto puro.

## Motivação

Ferramentas de merge tradicionais (como diff3) operam linha por linha, gerando conflitos espúrios quando múltiplas mudanças ocorrem na mesma linha. CSDiff-Web resolve isso quebrando código em separadores sintáticos (ex: `{`, `}`, `;`, `=>`) antes do merge.

### Exemplo

**Código Original:**
```typescript
function foo() { return 1; }
```

**Left:** adiciona log
```typescript
function foo() { console.log('x'); return 1; }
```

**Right:** muda retorno
```typescript
function foo() { return 2; }
```

**diff3 tradicional:** ❌ CONFLITO (mesma linha modificada)

**CSDiff-Web:** ✅ SEM CONFLITO (mudanças em separadores diferentes)

## Arquitetura

```
┌─────────────────┐
│   Minerador     │  → Extrai triplas de merge commits do GitHub
└────────┬────────┘
         ▼
┌─────────────────┐
│  CSDiff-Web     │  → Wrapper Python: explosão → diff3 → reconstrução
│     (Core)      │
└────────┬────────┘
         ▼
┌─────────────────┐
│     Runner      │  → Orquestra experimentos (CSDiff-Web vs diff3 vs slow-diff3)
└────────┬────────┘
         ▼
┌─────────────────┐
│   Analisador    │  → Coleta métricas (conflitos, FP, FN)
└─────────────────┘
```

## Estrutura do Projeto

```
csdiff-web/
├── src/
│   ├── core/              # CSDiff-Web Core
│   │   ├── separators.py         # Definição de separadores (.ts, .tsx, .js, .jsx)
│   │   ├── preprocessor.py       # Explosão do código
│   │   ├── postprocessor.py      # Reconstrução após diff3
│   │   ├── alignment_resolver.py # Solução para Alignment Problem
│   │   ├── filters.py            # Detecção de arquivos minificados
│   │   └── csdiff_web.py         # Entry point principal
│   ├── miner/             # Minerador de commits
│   ├── runner/            # Orquestrador de experimentos
│   └── analyzer/          # Análise de resultados
├── tests/                 # Testes unitários e integração
├── examples/              # Exemplos de uso
├── requirements.txt
└── README.md
```

## Instalação

```bash
# Clone o repositório
git clone <repo-url>
cd csdiff-web

# Instale dependências
pip3 install -r requirements.txt

# Verifique instalação do diff3
diff3 --version

# Instale dependências do slow-diff3
cd slow-diff3
npm install
```

## Uso Rápido

### Exemplo Básico

```python
from src.core.csdiff_web import CSDiffWeb

# Criar instância para TypeScript
csdiff = CSDiffWeb(".ts")

# Versões do arquivo
base  = "function foo() { return 1; }"
left  = "function foo() { return 2; }"
right = "function foo() { return 3; }"

# Executar merge
result, has_conflict, num_conflicts = csdiff.merge(base, left, right)

print(result)
print(f"Conflitos: {num_conflicts}")
```

### Executar Exemplos

```bash
python3 examples/simple_merge.py
```

Exemplos incluem:
- ✅ Merge sem conflitos (mudanças em locais diferentes)
- ❌ Merge com conflitos (ambos lados mudam mesma função)
- 🎨 Merge de componentes JSX/TSX
- 📊 Estatísticas de explosão

## Testes

```bash
# Rodar todos os testes
python3 -m pytest tests/ -v

# Testes específicos
python3 -m pytest tests/test_preprocessor.py -v        # Preprocessor
python3 -m pytest tests/test_csdiff_integration.py -v  # Integração
```

**Cobertura atual:** 14 testes unitários + 7 testes de integração

## Recursos Principais

### 1. Separadores por Extensão

| Extensão | Separadores |
|----------|-------------|
| `.ts` `.js` | `{` `}` `[` `]` `(` `)` `;` `,` `=>` `??` |
| `.tsx` `.jsx` | Lógicos + `<` `>` `</` `/>` `{}` `className=` |

### 2. Filtro de Arquivos Minificados

Heurísticas automáticas para detectar e rejeitar arquivos minificados:
- Linhas > 500 caracteres
- Média de linha > 200 caracteres
- Nomes como `.min.js`, `.bundle.js`

### 3. Solução para Alignment Problem

**Problema:** Código explodido gera muitas linhas idênticas (`{`, `}`), confundindo diff3.

**Solução:** Marcadores contextuais únicos
```
§§CSDIFF_<depth>_<hash>§§{
```

Cada separador recebe:
- **Depth:** Profundidade de aninhamento
- **Hash:** Hash do contexto precedente

Isso garante que `{` de funções diferentes sejam distinguíveis.

### 4. Detecção de Strings Literais

O preprocessor **não quebra** separadores dentro de strings:
```typescript
const x = "function() { return; }";  // String preservada intacta
```

Suporta:
- Aspas simples: `'text'`
- Aspas duplas: `"text"`
- Template literals: `` `text ${expr}` ``
- Escapes: `\'` `\"` `` \` ``

## Comparação com Ferramentas Existentes

| Ferramenta | Abordagem | Implementação | Granularidade | Conflitos Espúrios |
|------------|-----------|---------------|-------------------|
| **diff3** | Textual linha a linha | Nativa (C / Binário) | Linha | Alto |
| **slow-diff3** | Textual linha a linha | Interpretada (Node.js) | Linha | Alto |
| **CSDiff-Web** | Textual + separadores | Interpretada (Python) | Separador sintático | Médio |

**Vantagens do CSDiff-Web:**
- ✅ Mais preciso que diff3 puro ou slow-diff3
- ✅ Mais simples que abordagens estruturadas (sem parsing de AST)
- ✅ Funciona com código sintaticamente incorreto
- ✅ Preserva formatação e comentários

## Minerador de Repositórios

O minerador extrai triplas (base, left, right) de merge commits reais do GitHub.

**Uso rápido:**
```bash
# Minerar repositórios TypeScript (meta: 100 triplas)
python3 scripts/mine_repositories.py --language typescript --max-triplets 100

# Minerar todas as linguagens
python3 scripts/mine_repositories.py --all --max-triplets 500
```

**Repositórios configurados:**
- 26 repositórios de alta qualidade (50k-220k GitHub stars)
- 7 TypeScript, 6 TSX, 6 JavaScript, 4 JSX, 3 Mixed
- Inclui: VSCode, React, Next.js, Angular, Node.js, Vue, e mais

Ver documentação completa: [docs/MINER.md](docs/MINER.md)

## Runner de Experimentos

O Runner executa experimentos comparativos entre CSDiff-Web, diff3 e slow-diff3.

**Uso rápido:**
```bash
# Executar em todas as triplas mineradas
python3 scripts/run_experiments.py

# Executar em 50 triplas com timeout de 60s
python3 scripts/run_experiments.py --max-triplets 50 --timeout 60

# Executar apenas CSDiff-Web vs diff3
python3 scripts/run_experiments.py --tools csdiff-web diff3
```

**Saídas geradas:**
- `data/results/results_TIMESTAMP.csv` - Resultados detalhados por tripla
- `data/results/summary_TIMESTAMP.txt` - Resumo estatístico

**Métricas coletadas:**
- Sucesso/falha de cada ferramenta
- Número de conflitos detectados
- Tempo de execução
- Erros e exceções

## Analisador Estatístico

O Analyzer gera análises estatísticas e relatórios científicos dos resultados.

**Uso rápido:**
```bash
# Analisar resultados gerados pelo Runner
python3 scripts/analyze_results.py data/results/results_*.csv

# Especificar diretório de saída
python3 scripts/analyze_results.py data/results/results_*.csv --output data/reports
```

**Análises geradas:**
1. **False Positives/Negatives** - Usa diff3 como baseline
   - TP, FP, TN, FN
   - Precision, Recall, F1-Score, Accuracy

2. **Comparação de conflitos** - Taxa de conflitos por ferramenta
   - Redução absoluta e relativa de conflitos

3. **Distribuição de conflitos** - Casos com 0, 1, 2, 3+ conflitos

4. **Performance** - Tempo de execução (média, mediana, desvio padrão)

**Saídas geradas:**
- `analysis_TIMESTAMP.md` - Relatório Markdown científico
- `table_TIMESTAMP.tex` - Tabela LaTeX para papers

**Exemplo completo:**
```bash
# Pipeline completo
python3 examples/simple_experiments.py  # Gera triplas + experimenta
python3 examples/simple_analysis.py     # Analisa resultados
```

## Próximos Passos (Roadmap)

- [x] **Core:** CSDiff-Web funcional com testes ✅
- [x] **Minerador:** Extração de triplas de merge commits ✅
- [x] **Runner:** Orquestrador de experimentos (CSDiff-Web vs diff3 vs slow-diff3) ✅
- [x] **Analisador:** Coleta de métricas (conflitos, FP, FN) ✅
- [ ] **Docker:** Container para reprodutibilidade
- [ ] **Experimentos em escala:** Executar em 200+ triplas e gerar relatórios
- [ ] **Visualizações:** Gráficos e charts para análise
- [ ] **Publicação:** Submissão de artigo científico

## Marcos de Validação

| Marco | Critério | Status |
|-------|----------|--------|
| **M1: Core Funcional** | Merge básico funciona | ✅ **Completo** |
| **M2: Testes** | Cobertura de testes > 80% | ✅ **Completo** |
| **M3: Minerador** | ≥100 triplas de ≥5 repos | ✅ **Completo** |
| **M4: Runner** | Comparação com diff3 + slow-diff3 | ✅ **Completo** |
| **M5: Analyzer** | Análise estatística (FP/FN, métricas) | ✅ **Completo** |

## Referências

- **TCC de Leonardo dos Anjos Silva (2025):** Identificação do Alignment Problem em JavaScript
- **Mining Framework (SPGroup/UFPE):** Infraestrutura de mineração de repositórios
- **CSDiff Original:** Merge textual com separadores para Java

## Contribuindo

Este é um projeto acadêmico sob orientação do Prof. Paulo Borba. Para questões ou sugestões, entre em contato.



---

**Projeto de Graduação em Ciência da Computação**
**Centro de Informática - Universidade Federal de Pernambuco (UFPE)**
**2025**
-+