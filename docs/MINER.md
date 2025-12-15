# Minerador de Merge Commits - Documentação

O Minerador é responsável por extrair triplas (base, left, right) de merge commits de repositórios GitHub, conforme especificado na **Seção 3 do Plano Técnico**.

## Arquitetura do Minerador

```
┌─────────────────────┐
│  GitHub Repository  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   GitHubMiner       │  ← Orquestrador principal
│ - Clona repos       │
│ - Lista commits     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   CommitFilter      │  ← Filtro CRÍTICO
│ - 2 pais EXATOS     │
│ - Não fast-forward  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  TripletExtractor   │  ← Extração de triplas
│ - Arquivos válidos  │
│ - Modificados em    │
│   AMBOS os lados    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  data/triplets/     │
│  triplet_001/       │
│    base.ts          │
│    left.ts          │
│    right.ts         │
│    metadata.txt     │
└─────────────────────┘
```

## Módulos

### 1. CommitFilter ([commit_filter.py](../src/miner/commit_filter.py))

Filtra commits de merge válidos.

**Critérios de validação:**
1. ✅ Commit tem EXATAMENTE 2 pais (não 0, não 1, não 3+)
2. ✅ Merge base (ancestral comum) existe
3. ✅ NÃO é fast-forward (base != left e base != right)

**Exemplo:**
```python
from src.miner.commit_filter import CommitFilter

filter = CommitFilter()
valid_merges = filter.filter_merge_commits(repo, all_commits)

filter.print_statistics()
# Output:
# Total de commits analisados: 1000
#   Commits de merge (--merges): 150
#   └─ Pais inválidos (≠ 2):     20
#   └─ Sem merge base:           5
#   └─ Fast-forwards:            30
# ✓ MERGES VÁLIDOS:              95
```

### 2. TripletExtractor ([triplet_extractor.py](../src/miner/triplet_extractor.py))

Extrai triplas de arquivos modificados.

**Critérios de seleção de arquivo:**
1. ✅ Extensão suportada (.ts, .tsx, .js, .jsx)
2. ✅ Modificado em AMBOS os pais (left E right)
3. ✅ Existe nas três versões (base, left, right)

**Exemplo:**
```python
from src.miner.triplet_extractor import TripletExtractor

extractor = TripletExtractor(output_dir=Path('data/triplets'))
triplets = extractor.extract_triplet(repo, merge_info)

# Cada tripla contém:
# {
#     'filepath': 'src/index.ts',
#     'extension': '.ts',
#     'base_content': '...',
#     'left_content': '...',
#     'right_content': '...',
#     'commit_sha': 'abc123...'
# }
```

### 3. GitHubMiner ([github_miner.py](../src/miner/github_miner.py))

Orquestrador principal da mineração.

**Responsabilidades:**
- Clonar/atualizar repositórios
- Iterar sobre commits de merge
- Aplicar filtros
- Extrair triplas
- Salvar no disco
- Gerenciar estatísticas globais

**Exemplo:**
```python
from src.miner.github_miner import GitHubMiner

miner = GitHubMiner(
    repos_dir=Path('data/repos'),
    triplets_dir=Path('data/triplets'),
    target_triplets=100
)

repos = [
    {'url': 'https://github.com/microsoft/TypeScript', 'name': 'typescript'},
    {'url': 'https://github.com/facebook/react', 'name': 'react'}
]

triplets = miner.mine_repositories(repos, max_triplets=100)
```

## Uso

### Opção 1: Script de linha de comando

```bash
# Minerar TypeScript (meta: 100 triplas)
python3 scripts/mine_repositories.py --language typescript --max-triplets 100

# Minerar todas as linguagens (meta: 500 triplas)
python3 scripts/mine_repositories.py --all --max-triplets 500

# Minerar TSX com verbose
python3 scripts/mine_repositories.py --language tsx --max-triplets 50 --verbose

# Limitar número de repositórios
python3 scripts/mine_repositories.py --language javascript --max-repos 3 --max-triplets 30
```

**Opções disponíveis:**
- `--language`: Categoria (typescript, tsx, javascript, jsx, mixed, all)
- `--max-triplets`: Meta de triplas (padrão: 100)
- `--max-repos`: Máximo de repos a processar (padrão: todos)
- `--config`: Caminho do YAML de configuração
- `--repos-dir`: Onde clonar repos (padrão: data/repos)
- `--output-dir`: Onde salvar triplas (padrão: data/triplets)
- `--verbose`: Modo debug

### Opção 2: Uso em código Python

```python
from pathlib import Path
from src.miner.github_miner import GitHubMiner

# Configurar minerador
miner = GitHubMiner(
    repos_dir=Path('data/repos'),
    triplets_dir=Path('data/triplets'),
    target_triplets=50
)

# Minerar repositório único
triplets = miner.mine_repository(
    repo_url='https://github.com/prettier/prettier',
    repo_name='prettier'
)

print(f"Extraídas {len(triplets)} triplas")
```

### Opção 3: Exemplo interativo

```bash
python3 examples/simple_mining.py
```

## Configuração de Repositórios

Arquivo: [config/repositories.yaml](../config/repositories.yaml)

Estrutura:
```yaml
typescript:
  - name: vscode
    url: https://github.com/microsoft/vscode
    description: "Visual Studio Code"
    stars: 150000

tsx:
  - name: nextjs
    url: https://github.com/vercel/next.js
    description: "Next.js framework"
    stars: 118000

# ... mais categorias
```

**Repositórios incluídos:**
- **TypeScript:** 7 repos (VSCode, TypeScript, Angular, Nest, Grafana, Supabase, Playwright)
- **TSX:** 6 repos (Next.js, Material-UI, Ant Design, Chakra UI, React Native, Expo)
- **JavaScript:** 6 repos (React, Node.js, Vue, Express, Webpack, Babel)
- **JSX:** 4 repos (React Router, Redux, Create React App, Gatsby)
- **Mixed:** 3 repos (Storybook, Jest, Prettier)

**Total:** 26 repositórios de alta qualidade (50k-220k stars)

## Estrutura de Saída

```
data/triplets/
├── triplet_001/
│   ├── base.ts          # Versão do ancestral comum
│   ├── left.ts          # Versão do primeiro pai
│   ├── right.ts         # Versão do segundo pai
│   └── metadata.txt     # Metadados (SHAs, tamanhos, etc)
├── triplet_002/
│   ├── base.tsx
│   ├── left.tsx
│   ├── right.tsx
│   └── metadata.txt
└── ...
```

**Exemplo de metadata.txt:**
```
Triplet ID: 1
Original File: src/components/Button.tsx
Extension: .tsx
Commit SHA: a1b2c3d4e5f6...
Base SHA: 1234567890ab...
Left SHA: abcdef123456...
Right SHA: 9876543210fe...

File Sizes:
  Base: 523 bytes
  Left: 612 bytes
  Right: 578 bytes
```

## Estatísticas

O minerador coleta estatísticas detalhadas:

```python
miner.print_final_statistics()
```

**Saída:**
```
============================================================
ESTATÍSTICAS FINAIS DA MINERAÇÃO
============================================================
Repositórios processados:  5
Repositórios com falha:    0
Total de commits:          2453
  └─ Commits de merge:     387
  └─ Merges válidos:       142

✓ TRIPLAS EXTRAÍDAS:       103
============================================================
Taxa de merges válidos: 36.7%
Média de triplas por merge: 0.7
Triplas salvas em: data/triplets
============================================================
```

## Performance e Limites

| Aspecto | Valor |
|---------|-------|
| **Commits por repo** | 1000 (configurável) |
| **Timeout de clone** | 300s (5 minutos) |
| **Triplas por repo** | Até meta global |
| **Espaço em disco** | ~50-100MB por repo clonado |
| **Tempo médio** | 2-5 min por repo (depende do tamanho) |

## Troubleshooting

### Problema: "No module named 'git'"

**Solução:**
```bash
pip3 install gitpython
```

### Problema: "No module named 'yaml'"

**Solução:**
```bash
pip3 install pyyaml
```

### Problema: Clone lento

**Solução:** Use `--max-repos` para limitar quantidade:
```bash
python3 scripts/mine_repositories.py --language typescript --max-repos 3
```

### Problema: Poucos merges válidos encontrados

**Causas comuns:**
- Repositório usa rebases ao invés de merges
- Histórico linear (sem merges reais)
- Fast-forwards habilitados

**Solução:** Trocar por repositórios com mais merges (verificar no GitHub Insights → Network)

## Validação dos Resultados

Para validar que a mineração foi bem-sucedida:

```bash
# Contar triplas extraídas
ls -d data/triplets/triplet_* | wc -l

# Verificar conteúdo de uma tripla
cat data/triplets/triplet_001/metadata.txt

# Verificar tamanhos
du -sh data/repos/
du -sh data/triplets/
```

## Próximos Passos

Após mineração bem-sucedida:

1. ✅ Verificar que há ≥100 triplas
2. ✅ Validar distribuição por extensão
3. ➡️ **Implementar Runner** (executar CSDiff-Web + diff3 + Mergiraf nas triplas)
4. ➡️ **Implementar Analisador** (coletar métricas e gerar CSV)

---

**Referência:** Seção 3 do Plano Técnico
