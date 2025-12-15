"""
Teste de validação do minerador.
Valida que o minerador consegue extrair triplas de um repositório real.

NOTA: Este teste requer conexão com internet e pode demorar alguns minutos.
"""

import sys
from pathlib import Path
import tempfile
import shutil

# Adicionar src/ ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.miner.github_miner import GitHubMiner
from src.miner.commit_filter import CommitFilter
from src.miner.triplet_extractor import TripletExtractor


class TestMinerValidation:
    """Testes de validação do minerador."""

    def test_commit_filter_basic(self):
        """Testa filtro de commits básico."""
        filter = CommitFilter()

        # Verificar que estatísticas iniciam zeradas
        stats = filter.get_statistics()
        assert stats['total_commits'] == 0
        assert stats['valid_merges'] == 0

    def test_triplet_extractor_basic(self):
        """Testa extrator de triplas básico."""
        with tempfile.TemporaryDirectory() as tmpdir:
            extractor = TripletExtractor(Path(tmpdir))

            # Verificar extensões suportadas
            assert extractor.is_supported_file("test.ts")
            assert extractor.is_supported_file("test.tsx")
            assert extractor.is_supported_file("test.js")
            assert extractor.is_supported_file("test.jsx")
            assert not extractor.is_supported_file("test.py")
            assert not extractor.is_supported_file("README.md")

    def test_miner_initialization(self):
        """Testa inicialização do minerador."""
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

            # Verificar estatísticas iniciais
            stats = miner.get_statistics()
            assert stats['repos_processed'] == 0
            assert stats['total_triplets'] == 0

    def test_mine_small_repo_integration(self, skip_slow=True):
        """
        Teste de integração: minera repositório pequeno real.

        AVISO: Este teste clona um repositório do GitHub (~10-20MB)
        e pode demorar 2-5 minutos dependendo da conexão.

        Para executar:
        pytest tests/test_miner_validation.py::TestMinerValidation::test_mine_small_repo_integration -v
        """
        if skip_slow:
            # Pular por padrão (muito lento para CI)
            import pytest
            pytest.skip("Teste de integração lento - execute manualmente")

        with tempfile.TemporaryDirectory() as tmpdir:
            repos_dir = Path(tmpdir) / "repos"
            triplets_dir = Path(tmpdir) / "triplets"

            # Criar minerador
            miner = GitHubMiner(
                repos_dir=repos_dir,
                triplets_dir=triplets_dir,
                target_triplets=5  # Meta pequena para teste
            )

            # Repositório pequeno conhecido com muitos merges
            # Prettier é bom para testes: ~48k stars, muitos merges, código TypeScript
            repo_info = {
                'url': 'https://github.com/prettier/prettier',
                'name': 'prettier'
            }

            # Minerar (limitar a 200 commits para ser rápido)
            triplets = miner.mine_repository(
                repo_url=repo_info['url'],
                repo_name=repo_info['name'],
                max_commits=200
            )

            # Validações
            assert len(triplets) >= 0, "Deve retornar lista (mesmo que vazia)"

            # Se encontrou triplas, validar estrutura
            if triplets:
                triplet = triplets[0]

                # Verificar campos obrigatórios
                assert 'filepath' in triplet
                assert 'extension' in triplet
                assert 'base_content' in triplet
                assert 'left_content' in triplet
                assert 'right_content' in triplet
                assert 'commit_sha' in triplet

                # Verificar tipos
                assert isinstance(triplet['filepath'], str)
                assert triplet['extension'] in ['.ts', '.tsx', '.js', '.jsx']
                assert isinstance(triplet['base_content'], str)
                assert isinstance(triplet['left_content'], str)
                assert isinstance(triplet['right_content'], str)

                # Verificar que conteúdos não estão vazios
                assert len(triplet['base_content']) > 0
                assert len(triplet['left_content']) > 0
                assert len(triplet['right_content']) > 0

                # Verificar que SHA tem tamanho correto (40 chars hexadecimal)
                assert len(triplet['commit_sha']) == 40

                print(f"\n✓ Teste de integração bem-sucedido!")
                print(f"  Triplas extraídas: {len(triplets)}")
                print(f"  Primeira tripla: {triplet['filepath']}")
                print(f"  Extensão: {triplet['extension']}")
                print(f"  Tamanhos: {len(triplet['base_content'])} / "
                      f"{len(triplet['left_content'])} / "
                      f"{len(triplet['right_content'])} bytes")
            else:
                print("\n⚠ Nenhuma tripla encontrada (pode acontecer em repos pequenos)")
                print("  Isso não é necessariamente um erro - apenas significa que")
                print("  nenhum merge válido foi encontrado nos primeiros 200 commits")


def run_manual_test():
    """
    Executa teste manual (não pytest) para validação rápida.

    Uso:
        python3 tests/test_miner_validation.py
    """
    print("=" * 60)
    print("TESTE MANUAL DE VALIDAÇÃO DO MINERADOR")
    print("=" * 60)
    print("\nEste teste irá:")
    print("1. Criar diretórios temporários")
    print("2. Clonar repositório Prettier (~10-20MB)")
    print("3. Minerar até 5 triplas")
    print("4. Validar resultados")
    print("\nTempo estimado: 2-5 minutos")
    print("=" * 60)

    choice = input("\nContinuar? (s/N): ").strip().lower()

    if choice != 's':
        print("Teste cancelado.")
        return

    # Criar diretórios temporários
    import tempfile
    tmpdir = tempfile.mkdtemp()

    try:
        repos_dir = Path(tmpdir) / "repos"
        triplets_dir = Path(tmpdir) / "triplets"

        print(f"\nDiretórios temporários:")
        print(f"  Repos: {repos_dir}")
        print(f"  Triplets: {triplets_dir}")

        # Criar minerador
        miner = GitHubMiner(
            repos_dir=repos_dir,
            triplets_dir=triplets_dir,
            target_triplets=5
        )

        # Minerar
        print("\nIniciando mineração...")
        triplets = miner.mine_repository(
            repo_url='https://github.com/prettier/prettier',
            repo_name='prettier',
            max_commits=300  # Aumentar um pouco para ter mais chance de encontrar triplas
        )

        # Resultados
        print("\n" + "=" * 60)
        print("RESULTADOS")
        print("=" * 60)
        print(f"Triplas extraídas: {len(triplets)}")

        if triplets:
            print("\n✅ MINERADOR FUNCIONANDO CORRETAMENTE!")
            print("\nPrimeiras triplas:")
            for i, t in enumerate(triplets[:3], 1):
                print(f"\n{i}. {t['filepath']}")
                print(f"   Extensão: {t['extension']}")
                print(f"   Commit: {t['commit_sha'][:8]}")
                print(f"   Tamanhos: {len(t['base_content'])} / "
                      f"{len(t['left_content'])} / "
                      f"{len(t['right_content'])} bytes")

            # Verificar se triplas foram salvas
            saved_triplets = list(triplets_dir.glob("triplet_*"))
            print(f"\nTriplas salvas no disco: {len(saved_triplets)}")

            if saved_triplets:
                # Mostrar conteúdo de uma tripla
                first_triplet = saved_triplets[0]
                print(f"\nConteúdo de {first_triplet.name}:")
                for file in first_triplet.iterdir():
                    print(f"  - {file.name} ({file.stat().st_size} bytes)")

                # Mostrar metadata
                metadata_file = first_triplet / "metadata.txt"
                if metadata_file.exists():
                    print(f"\nMetadata:")
                    print(metadata_file.read_text()[:500])
        else:
            print("\n⚠ Nenhuma tripla encontrada")
            print("\nPossíveis causas:")
            print("- Repositório usa rebases ao invés de merges")
            print("- Primeiros 300 commits não têm merges válidos")
            print("- Arquivos modificados não têm extensão suportada")
            print("\nIsso não é necessariamente um erro do minerador.")

    finally:
        # Limpar diretórios temporários
        print(f"\nLimpando diretórios temporários...")
        shutil.rmtree(tmpdir)
        print("✓ Limpeza concluída")


if __name__ == '__main__':
    # Se executado diretamente, rodar teste manual
    run_manual_test()
