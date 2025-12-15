"""
Minerador de commits de merge do GitHub.
Seção 3.3 do Plano Técnico.

Este módulo orquestra todo o processo de mineração:
1. Clonar repositórios do GitHub
2. Listar commits de merge (--merges)
3. Filtrar merges válidos (2 pais, não fast-forward)
4. Extrair triplas de arquivos modificados
5. Salvar triplas no disco

IMPLEMENTA O ALGORITMO DA SEÇÃO 3.2:
    MinerarMergeCommits(repositorios, extensoes)
"""

from git import Repo
from pathlib import Path
from typing import List, Dict, Optional
from tqdm import tqdm
import logging

from .commit_filter import CommitFilter
from .triplet_extractor import TripletExtractor

logger = logging.getLogger(__name__)


class GitHubMiner:
    """
    Minerador principal de merge commits do GitHub.

    Responsável por:
    - Clonar repositórios
    - Encontrar commits de merge
    - Orquestrar filtro e extração
    - Gerenciar estatísticas globais
    """

    def __init__(
        self,
        repos_dir: Path,
        triplets_dir: Path,
        target_triplets: int = 100
    ):
        """
        Inicializa minerador.

        Args:
            repos_dir: Diretório onde clonar repositórios
            triplets_dir: Diretório para salvar triplas
            target_triplets: Meta de triplas a minerar (padrão: 100)
        """
        self.repos_dir = Path(repos_dir)
        self.triplets_dir = Path(triplets_dir)
        self.target_triplets = target_triplets

        # Criar diretórios se não existirem
        self.repos_dir.mkdir(parents=True, exist_ok=True)
        self.triplets_dir.mkdir(parents=True, exist_ok=True)

        # Estatísticas globais
        self.stats = {
            'repos_processed': 0,
            'repos_failed': 0,
            'total_commits': 0,
            'total_merges': 0,
            'valid_merges': 0,
            'total_triplets': 0
        }

    def clone_or_update_repo(
        self,
        repo_url: str,
        repo_name: str
    ) -> Optional[Repo]:
        """
        Clona repositório ou atualiza se já existe.

        Args:
            repo_url: URL do repositório (ex: https://github.com/user/repo)
            repo_name: Nome do repositório (usado como diretório)

        Returns:
            Objeto Repo do GitPython, ou None se falhar

        Examples:
            >>> miner = GitHubMiner(Path('/tmp/repos'), Path('/tmp/triplets'))
            >>> repo = miner.clone_or_update_repo('https://github.com/user/repo', 'repo')
            >>> repo is not None
            True
        """
        repo_path = self.repos_dir / repo_name

        try:
            if repo_path.exists():
                logger.info(f"Repositório {repo_name} já existe, atualizando...")
                repo = Repo(repo_path)
                # Atualizar remote origin
                origin = repo.remotes.origin
                origin.fetch()
                logger.info(f"✓ Repositório {repo_name} atualizado")
            else:
                logger.info(f"Clonando {repo_url}...")
                repo = Repo.clone_from(repo_url, repo_path)
                logger.info(f"✓ Repositório {repo_name} clonado")

            return repo

        except Exception as e:
            logger.error(f"Erro ao clonar/atualizar {repo_name}: {e}")
            self.stats['repos_failed'] += 1
            return None

    def mine_repository(
        self,
        repo_url: str,
        repo_name: str,
        max_commits: int = 1000
    ) -> List[Dict]:
        """
        Minera um repositório completo.

        Args:
            repo_url: URL do repositório
            repo_name: Nome do repositório
            max_commits: Máximo de commits a analisar (evitar repos muito grandes)

        Returns:
            Lista de triplas extraídas

        Examples:
            >>> miner = GitHubMiner(Path('/tmp/repos'), Path('/tmp/triplets'))
            >>> triplets = miner.mine_repository('https://github.com/user/repo', 'repo')
            >>> isinstance(triplets, list)
            True
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"MINERANDO: {repo_name}")
        logger.info(f"{'='*60}")

        # Clonar/atualizar repositório
        repo = self.clone_or_update_repo(repo_url, repo_name)
        if repo is None:
            return []

        self.stats['repos_processed'] += 1

        # Listar commits de merge
        logger.info("Listando commits de merge...")
        try:
            # Usar --merges flag do git log
            merge_commits = list(
                repo.iter_commits('--all', merges=True, max_count=max_commits)
            )
            logger.info(f"Encontrados {len(merge_commits)} commits de merge")
            self.stats['total_commits'] += len(merge_commits)
            self.stats['total_merges'] += len(merge_commits)

        except Exception as e:
            logger.error(f"Erro ao listar commits: {e}")
            return []

        # Filtrar merges válidos
        logger.info("Filtrando merges válidos...")
        commit_filter = CommitFilter()
        valid_merges = commit_filter.filter_merge_commits(repo, merge_commits)
        self.stats['valid_merges'] += len(valid_merges)

        commit_filter.print_statistics()

        if not valid_merges:
            logger.warning(f"Nenhum merge válido encontrado em {repo_name}")
            return []

        # Extrair triplas
        logger.info(f"Extraindo triplas de {len(valid_merges)} merges...")
        triplet_extractor = TripletExtractor(self.triplets_dir)

        all_triplets = []
        for merge_info in tqdm(valid_merges, desc="Extraindo triplas"):
            triplets = triplet_extractor.extract_triplet(repo, merge_info)
            all_triplets.extend(triplets)

            # Verificar se atingiu meta
            if len(all_triplets) >= self.target_triplets:
                logger.info(f"Meta de {self.target_triplets} triplas atingida!")
                break

        triplet_extractor.print_statistics()

        self.stats['total_triplets'] += len(all_triplets)

        logger.info(f"\n✓ {len(all_triplets)} triplas extraídas de {repo_name}")
        return all_triplets

    def mine_repositories(
        self,
        repo_list: List[Dict],
        max_triplets: Optional[int] = None
    ) -> List[Dict]:
        """
        Minera múltiplos repositórios.

        Args:
            repo_list: Lista de dicts com 'url' e 'name'
            max_triplets: Máximo de triplas totais (para todos os repos)

        Returns:
            Lista consolidada de todas as triplas

        Examples:
            >>> miner = GitHubMiner(Path('/tmp/repos'), Path('/tmp/triplets'))
            >>> repos = [
            ...     {'url': 'https://github.com/user/repo1', 'name': 'repo1'},
            ...     {'url': 'https://github.com/user/repo2', 'name': 'repo2'}
            ... ]
            >>> triplets = miner.mine_repositories(repos, max_triplets=50)
            >>> len(triplets) <= 50
            True
        """
        all_triplets = []
        max_total = max_triplets or self.target_triplets

        print("\n" + "=" * 60)
        print(f"INICIANDO MINERAÇÃO DE {len(repo_list)} REPOSITÓRIOS")
        print(f"Meta: {max_total} triplas")
        print("=" * 60)

        for i, repo_info in enumerate(repo_list, 1):
            print(f"\n[{i}/{len(repo_list)}] Processando: {repo_info['name']}")

            triplets = self.mine_repository(
                repo_info['url'],
                repo_info['name']
            )

            all_triplets.extend(triplets)

            # Salvar triplas conforme são extraídas
            self._save_triplets_batch(triplets, len(all_triplets) - len(triplets))

            # Verificar se atingiu meta global
            if len(all_triplets) >= max_total:
                logger.info(
                    f"\n🎯 Meta global de {max_total} triplas atingida! "
                    f"Parando mineração."
                )
                break

            logger.info(
                f"Progresso: {len(all_triplets)}/{max_total} triplas "
                f"({len(all_triplets)/max_total*100:.1f}%)"
            )

        self.print_final_statistics()
        return all_triplets[:max_total]

    def _save_triplets_batch(
        self,
        triplets: List[Dict],
        start_id: int
    ):
        """
        Salva lote de triplas no disco.

        Args:
            triplets: Lista de triplas a salvar
            start_id: ID inicial para numeração
        """
        extractor = TripletExtractor(self.triplets_dir)

        for i, triplet in enumerate(triplets):
            triplet_id = start_id + i + 1
            extractor.save_triplet(triplet, triplet_id)

        logger.info(f"✓ {len(triplets)} triplas salvas no disco")

    def get_statistics(self) -> Dict:
        """Retorna estatísticas globais da mineração."""
        return self.stats.copy()

    def print_final_statistics(self):
        """Imprime estatísticas finais consolidadas."""
        print("\n" + "=" * 60)
        print("ESTATÍSTICAS FINAIS DA MINERAÇÃO")
        print("=" * 60)
        print(f"Repositórios processados:  {self.stats['repos_processed']}")
        print(f"Repositórios com falha:    {self.stats['repos_failed']}")
        print(f"Total de commits:          {self.stats['total_commits']}")
        print(f"  └─ Commits de merge:     {self.stats['total_merges']}")
        print(f"  └─ Merges válidos:       {self.stats['valid_merges']}")
        print(f"\n✓ TRIPLAS EXTRAÍDAS:       {self.stats['total_triplets']}")
        print("=" * 60)

        if self.stats['total_merges'] > 0:
            valid_rate = (self.stats['valid_merges'] /
                         self.stats['total_merges'] * 100)
            print(f"Taxa de merges válidos: {valid_rate:.1f}%")

        if self.stats['valid_merges'] > 0:
            triplets_per_merge = (self.stats['total_triplets'] /
                                 self.stats['valid_merges'])
            print(f"Média de triplas por merge: {triplets_per_merge:.1f}")

        print(f"\nTriplas salvas em: {self.triplets_dir}")
        print("=" * 60 + "\n")
