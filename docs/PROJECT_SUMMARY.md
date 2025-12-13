# Resumo do Projeto - CSDiff-Web

**Status Atual**: ✅ Marco M5 (Analyzer) Concluído  
**Data**: 2025-12-13  
**Versão**: 1.0.0

---

## 🎯 Objetivo do Projeto

CSDiff-Web é uma ferramenta de merge 3-way estruturado para TypeScript, JavaScript, JSX e TSX que utiliza separadores sintáticos para reduzir conflitos de merge. Desenvolvido como TCC na UFPE sob orientação do Prof. Paulo Borba.

---

## ✅ Marcos Completados

### M1: Core Funcional ✅
**Data**: 2025-12-13  
**Versão**: 0.1.0

**Implementado**:
- Pipeline completo de merge (6 módulos, ~1,207 linhas)
- Suporte para .ts, .tsx, .js, .jsx
- Solução para Alignment Problem com marcadores contextuais
- Detecção de strings literais (single, double, template)
- Filtro de arquivos minificados

**Módulos**:
- `separators.py` - Separadores por extensão
- `filters.py` - Detecção de minificados
- `preprocessor.py` - Explosão de código
- `alignment_resolver.py` - Marcadores únicos
- `postprocessor.py` - Reconstrução
- `csdiff_web.py` - Orquestrador

**Resultado**: Pipeline funcional com performance ~0.006s por arquivo

---

### M2: Testes ✅
**Data**: 2025-12-13  
**Versão**: 0.2.0

**Implementado**:
- 21 testes unitários
- 100% passing
- Cobertura > 80%

**Cobertura**:
- Separadores (6 testes)
- Filters (4 testes)
- Preprocessor (3 testes)
- Alignment (3 testes)
- Postprocessor (2 testes)
- Integração (3 testes)

**Resultado**: Validação completa do Core

---

### M3: Miner ✅
**Data**: 2025-12-13  
**Versão**: 0.3.0

**Implementado**:
- Sistema completo de mineração (3 módulos, ~889 linhas)
- Filtro de merge commits (EXATAMENTE 2 pais)
- Extração de triplas (base, left, right)
- 26 repositórios configurados (2M+ stars)

**Módulos**:
- `commit_filter.py` - Filtragem de commits
- `triplet_extractor.py` - Extração de triplas
- `github_miner.py` - Orquestrador

**Repositórios Incluídos**:
- TypeScript: vscode, typescript, deno, etc.
- TSX: react, next.js, material-ui, etc.
- JavaScript: node, jquery, express, etc.
- JSX: preact, inferno, etc.

**Resultado**: Sistema robusto de mineração de dados reais

---

### M4: Runner ✅
**Data**: 2025-12-13  
**Versão**: 0.4.0

**Implementado**:
- Orquestrador de experimentos (3 módulos, ~1,030 linhas)
- Execução de CSDiff-Web, diff3, Mergiraf
- Coleta de métricas (conflitos, tempo, erros)
- Geração de CSV e resumos

**Módulos**:
- `tool_executor.py` - Execução de ferramentas
- `result_collector.py` - Coleta de resultados
- `experiment_runner.py` - Orquestrador

**Métricas Coletadas**:
- Sucesso/falha
- Número de conflitos
- Tempo de execução
- Mensagens de erro

**Resultado**: Pipeline de experimentação completo e automatizado

---

### M5: Analyzer ✅
**Data**: 2025-12-13  
**Versão**: 1.0.0

**Implementado**:
- Análise estatística avançada (2 módulos, ~450 linhas)
- Cálculo de FP/FN com diff3 como baseline
- Métricas: Precision, Recall, F1-Score, Accuracy
- Relatórios científicos (Markdown + LaTeX)

**Módulos**:
- `metrics_analyzer.py` - Análise estatística
- `report_generator.py` - Geração de relatórios

**Análises Realizadas**:
1. False Positives/Negatives
2. Comparação de taxas de conflito
3. Distribuição de conflitos (0, 1, 2, 3+)
4. Performance (tempo médio, mediana, desvio)

**Resultado**: Sistema completo de análise científica pronto para TCC

---

## 📊 Estatísticas Globais

### Código Implementado
- **Core**: 1,207 linhas (6 módulos)
- **Miner**: 889 linhas (3 módulos)
- **Runner**: 1,030 linhas (3 módulos)
- **Analyzer**: 450 linhas (2 módulos)
- **Total**: ~3,576 linhas de código Python

### Testes
- 21 testes unitários
- 100% passing
- Cobertura > 80% do Core

### Documentação
- README.md principal (~250 linhas)
- ARCHITECTURE.md (~5,000 linhas)
- USAGE_GUIDE.md (~800 linhas)
- CHANGELOG.md (~300 linhas)
- Comentários inline em código

### Configuração
- 26 repositórios curados
- 4 linguagens suportadas (.ts, .tsx, .js, .jsx)
- Total: 2M+ GitHub stars nos repos

---

## 🔬 Resultados Preliminares

### Performance
- **CSDiff-Web médio**: ~0.006s
- **diff3 médio**: ~0.004s
- **Overhead**: ~47% (aceitável)

### Qualidade
- **Precision**: ~100% (em triplas sintéticas)
- **Recall**: ~100% (em triplas sintéticas)
- **F1-Score**: ~100% (em triplas sintéticas)
- **Accuracy**: ~100% (em triplas sintéticas)

*Nota: Resultados baseados em 4 triplas sintéticas. Experimentos em escala com dados reais ainda pendentes.*

---

## 📁 Estrutura do Projeto

```
csdiff-web/
├── src/
│   ├── core/           # Pipeline de merge (6 módulos) ✅
│   ├── miner/          # Mineração de triplas (3 módulos) ✅
│   ├── runner/         # Orquestrador de experimentos (3 módulos) ✅
│   └── analyzer/       # Análise estatística (2 módulos) ✅
├── scripts/
│   ├── mine_repositories.py    # CLI mineração ✅
│   ├── run_experiments.py      # CLI experimentos ✅
│   └── analyze_results.py      # CLI análise ✅
├── tests/              # 21 testes ✅
├── examples/           # Demos funcionais ✅
├── config/
│   └── repositories.yaml       # 26 repos configurados ✅
├── docs/
│   ├── ARCHITECTURE.md         # Arquitetura técnica ✅
│   ├── USAGE_GUIDE.md          # Guia de uso ✅
│   └── PROJECT_SUMMARY.md      # Este arquivo ✅
├── data/               # Dados experimentais (gitignored)
│   ├── triplets/       # Triplas mineradas
│   ├── results/        # CSVs de resultados
│   └── reports/        # Relatórios MD/LaTeX
├── README.md           # Documentação principal ✅
├── CHANGELOG.md        # Histórico de versões ✅
└── requirements.txt    # Dependências ✅
```

---

## 🚀 Pipeline Completo

```
1. MINERAÇÃO
   python3 scripts/mine_repositories.py --max-triplets 100
   ↓
   data/triplets/triplet_NNN/

2. EXPERIMENTOS
   python3 scripts/run_experiments.py --tools csdiff-web diff3
   ↓
   data/results/results_TIMESTAMP.csv

3. ANÁLISE
   python3 scripts/analyze_results.py data/results/results_*.csv
   ↓
   data/reports/analysis_TIMESTAMP.md
   data/reports/table_TIMESTAMP.tex
```

---

## 🎓 Contribuição Científica

### Problema Resolvido
**Alignment Problem**: Explosão de código gera muitas linhas idênticas, confundindo diff3.

### Solução Proposta
Marcadores contextuais únicos baseados em:
- Profundidade de aninhamento (depth)
- Hash MD5 do contexto precedente

### Formato do Marcador
```
§§CSDIFF_<depth>_<hash>§§<token>
```

### Exemplo
```typescript
// Sem marcadores (confuso)
{
{
{

// Com marcadores (únicos)
§§CSDIFF_0_a1b2c3§§{
§§CSDIFF_1_d4e5f6§§{
§§CSDIFF_2_g7h8i9§§{
```

---

## 📝 Próximos Passos

### Curto Prazo (1-2 semanas)
1. **Minerar 200+ triplas** de repositórios reais
2. **Executar experimentos em escala** com CSDiff-Web + diff3 + Mergiraf
3. **Gerar análises robustas** com dados reais

### Médio Prazo (1 mês)
4. **Criar visualizações** (gráficos, charts)
5. **Implementar Docker** para reprodutibilidade
6. **Documentar resultados** para TCC

### Longo Prazo (2-3 meses)
7. **Escrever artigo científico**
8. **Preparar apresentação de TCC**
9. **Submeter para publicação** (opcional)

---

## 🏆 Conquistas

- ✅ **5 Marcos completados** (M1-M5)
- ✅ **14 módulos implementados** (Core, Miner, Runner, Analyzer)
- ✅ **3,576 linhas de código** Python de alta qualidade
- ✅ **21 testes unitários** (100% passing)
- ✅ **6,000+ linhas de documentação** técnica
- ✅ **26 repositórios** configurados para mineração
- ✅ **Pipeline científico completo** (Minar → Experimentar → Analisar)
- ✅ **Relatórios LaTeX** prontos para papers

---

## 👥 Equipe

**Aluno**: João Victor  
**Orientador**: Prof. Paulo Borba  
**Instituição**: UFPE - Centro de Informática  
**Curso**: Ciência da Computação  
**Ano**: 2025

---

## 📚 Referências

1. **CSDiff Original** - Merge textual com separadores para Java
2. **TCC Leonardo dos Anjos Silva (2025)** - Identificação do Alignment Problem em JavaScript
3. **Mining Framework (SPGroup/UFPE)** - Infraestrutura de mineração de repositórios
4. **Git diff3** - Ferramenta base de merge 3-way
5. **Mergiraf** - Merge estruturado baseado em AST

---

## 📄 Licença

Projeto acadêmico - UFPE  
*Licença a definir*

---

**Última Atualização**: 2025-12-13  
**Status**: ✅ Pronto para experimentos em escala  
**Versão**: 1.0.0
