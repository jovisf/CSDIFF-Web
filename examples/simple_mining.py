"""
Exemplo simples de uso do minerador.
Demonstra mineração de um repositório pequeno.
"""

import sys
from pathlib import Path

# Adicionar src/ ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.miner.github_miner import GitHubMiner


def example_mine_single_repo():
    """Exemplo: Minerar um único repositório pequeno."""
    print("=" * 60)
    print("EXEMPLO: Mineração de Repositório Único")
    print("=" * 60)

    # Configurar minerador
    miner = GitHubMiner(
        repos_dir=Path('data/repos'),
        triplets_dir=Path('data/triplets'),
        target_triplets=10  # Meta pequena para exemplo
    )

    # Repositório pequeno para teste (Prettier - ~48k stars, mas com muitos merges)
    repo_info = {
        'url': 'https://github.com/prettier/prettier',
        'name': 'prettier'
    }

    print(f"\nMinerando: {repo_info['name']}")
    print(f"URL: {repo_info['url']}")
    print(f"Meta: 10 triplas\n")

    # Minerar
    try:
        triplets = miner.mine_repository(
            repo_url=repo_info['url'],
            repo_name=repo_info['name'],
            max_commits=500  # Limitar para exemplo rápido
        )

        print("\n" + "=" * 60)
        print("RESULTADO")
        print("=" * 60)
        print(f"Triplas extraídas: {len(triplets)}")

        if triplets:
            print("\nPrimeira tripla:")
            t = triplets[0]
            print(f"  Arquivo: {t['filepath']}")
            print(f"  Extensão: {t['extension']}")
            print(f"  Commit: {t['commit_sha'][:8]}")
            print(f"  Tamanhos: {len(t['base_content'])} / {len(t['left_content'])} / {len(t['right_content'])} bytes")

        print(f"\nTriplas salvas em: data/triplets/")

    except Exception as e:
        print(f"\n❌ Erro: {e}")


def example_mine_multiple_repos():
    """Exemplo: Minerar múltiplos repositórios pequenos."""
    print("\n\n" + "=" * 60)
    print("EXEMPLO: Mineração de Múltiplos Repositórios")
    print("=" * 60)

    # Configurar minerador
    miner = GitHubMiner(
        repos_dir=Path('data/repos'),
        triplets_dir=Path('data/triplets'),
        target_triplets=20
    )

    # Lista de repositórios pequenos
    repos = [
        {'url': 'https://github.com/prettier/prettier', 'name': 'prettier'},
        {'url': 'https://github.com/facebook/jest', 'name': 'jest'},
    ]

    print(f"\nMinerando {len(repos)} repositórios")
    print(f"Meta global: 20 triplas\n")

    # Minerar
    try:
        triplets = miner.mine_repositories(
            repo_list=repos,
            max_triplets=20
        )

        print("\n" + "=" * 60)
        print("RESULTADO FINAL")
        print("=" * 60)
        print(f"Total de triplas: {len(triplets)}")

        # Agrupar por extensão
        by_ext = {}
        for t in triplets:
            ext = t['extension']
            by_ext[ext] = by_ext.get(ext, 0) + 1

        print("\nDistribuição por extensão:")
        for ext, count in sorted(by_ext.items()):
            print(f"  {ext}: {count} triplas")

    except Exception as e:
        print(f"\n❌ Erro: {e}")


if __name__ == '__main__':
    print("⚠ AVISO: Este exemplo clonará repositórios do GitHub.")
    print("Isso pode demorar e consumir ~100MB de espaço em disco.\n")

    choice = input("Continuar? (s/N): ").strip().lower()

    if choice == 's':
        example_mine_single_repo()
        # example_mine_multiple_repos()  # Descomente para rodar
    else:
        print("Exemplo cancelado.")
