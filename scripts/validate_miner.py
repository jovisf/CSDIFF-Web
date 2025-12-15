#!/usr/bin/env python3
"""
Script de validação rápida do minerador.
Testa os componentes principais sem clonar repositórios completos.
"""

import sys
from pathlib import Path

# Adicionar src/ ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.miner.commit_filter import CommitFilter
from src.miner.triplet_extractor import TripletExtractor
from src.miner.github_miner import GitHubMiner


def test_commit_filter():
    """Testa CommitFilter."""
    print("=" * 60)
    print("1. Testando CommitFilter")
    print("=" * 60)

    filter = CommitFilter()

    # Testar métodos básicos
    stats = filter.get_statistics()
    assert stats['total_commits'] == 0
    assert stats['valid_merges'] == 0

    print("✓ CommitFilter inicializado corretamente")
    print("✓ Estatísticas funcionando")
    print()


def test_triplet_extractor():
    """Testa TripletExtractor."""
    print("=" * 60)
    print("2. Testando TripletExtractor")
    print("=" * 60)

    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        extractor = TripletExtractor(Path(tmpdir))

        # Testar detecção de extensões
        test_cases = [
            ("src/index.ts", True),
            ("src/component.tsx", True),
            ("src/app.js", True),
            ("src/ui.jsx", True),
            ("README.md", False),
            ("test.py", False),
            ("config.json", False),
        ]

        print("Testando detecção de extensões:")
        for filepath, expected in test_cases:
            result = extractor.is_supported_file(filepath)
            status = "✓" if result == expected else "✗"
            print(f"  {status} {filepath}: {result} (esperado: {expected})")
            assert result == expected

        print("\n✓ TripletExtractor funcionando corretamente")
        print()


def test_github_miner():
    """Testa GitHubMiner."""
    print("=" * 60)
    print("3. Testando GitHubMiner")
    print("=" * 60)

    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        repos_dir = Path(tmpdir) / "repos"
        triplets_dir = Path(tmpdir) / "triplets"

        miner = GitHubMiner(
            repos_dir=repos_dir,
            triplets_dir=triplets_dir,
            target_triplets=10
        )

        # Verificar que diretórios foram criados
        assert repos_dir.exists()
        assert triplets_dir.exists()
        print(f"✓ Diretórios criados:")
        print(f"  - {repos_dir}")
        print(f"  - {triplets_dir}")

        # Verificar estatísticas iniciais
        stats = miner.get_statistics()
        assert stats['repos_processed'] == 0
        assert stats['total_triplets'] == 0
        print("✓ Estatísticas inicializadas corretamente")

        print("\n✓ GitHubMiner funcionando corretamente")
        print()


def test_configuration():
    """Testa configuração de repositórios."""
    print("=" * 60)
    print("4. Testando Configuração de Repositórios")
    print("=" * 60)

    import yaml
    config_path = Path(__file__).parent.parent / "config" / "repositories.yaml"

    assert config_path.exists(), f"Arquivo de configuração não encontrado: {config_path}"
    print(f"✓ Arquivo de configuração existe: {config_path}")

    # Carregar e validar YAML
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    # Verificar categorias
    categories = ['typescript', 'tsx', 'javascript', 'jsx', 'mixed']
    for category in categories:
        assert category in config, f"Categoria {category} não encontrada"
        repos = config[category]
        assert isinstance(repos, list), f"Categoria {category} deve ser lista"
        assert len(repos) > 0, f"Categoria {category} está vazia"
        print(f"✓ Categoria '{category}': {len(repos)} repositórios")

    # Contar total
    total_repos = sum(len(config[cat]) for cat in categories)
    print(f"\n✓ Total de repositórios configurados: {total_repos}")

    # Validar estrutura de um repositório
    first_repo = config['typescript'][0]
    required_fields = ['name', 'url', 'description']
    for field in required_fields:
        assert field in first_repo, f"Campo '{field}' ausente"
    print(f"✓ Estrutura de repositório válida")

    print()


def test_example_files():
    """Verifica se arquivos de exemplo existem."""
    print("=" * 60)
    print("5. Testando Arquivos de Exemplo")
    print("=" * 60)

    base_dir = Path(__file__).parent.parent

    files_to_check = [
        "examples/simple_merge.py",
        "examples/simple_mining.py",
        "scripts/mine_repositories.py",
        "docs/MINER.md",
    ]

    for filepath in files_to_check:
        full_path = base_dir / filepath
        if full_path.exists():
            size = full_path.stat().st_size
            print(f"✓ {filepath} ({size} bytes)")
        else:
            print(f"✗ {filepath} NÃO ENCONTRADO")
            assert False, f"Arquivo necessário não encontrado: {filepath}"

    print()


def print_summary():
    """Imprime resumo da validação."""
    print("=" * 60)
    print("RESUMO DA VALIDAÇÃO")
    print("=" * 60)
    print()
    print("✅ Todos os testes passaram!")
    print()
    print("Componentes validados:")
    print("  ✓ CommitFilter")
    print("  ✓ TripletExtractor")
    print("  ✓ GitHubMiner")
    print("  ✓ Configuração YAML")
    print("  ✓ Arquivos de exemplo")
    print()
    print("Próximos passos:")
    print("  1. Executar mineração real:")
    print("     python3 scripts/mine_repositories.py --language typescript --max-triplets 10")
    print()
    print("  2. Ou testar com exemplo interativo:")
    print("     python3 examples/simple_mining.py")
    print()
    print("  3. Ou executar teste de integração (lento, clona repos):")
    print("     python3 tests/test_miner_validation.py")
    print()
    print("=" * 60)


def main():
    """Executa todos os testes de validação."""
    print("\n🔍 VALIDAÇÃO DO MINERADOR - CSDiff-Web\n")

    try:
        test_commit_filter()
        test_triplet_extractor()
        test_github_miner()
        test_configuration()
        test_example_files()

        print_summary()
        return 0

    except AssertionError as e:
        print(f"\n❌ ERRO: {e}")
        return 1

    except Exception as e:
        print(f"\n❌ ERRO INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
