"""
Filtro de commits de merge.
Seção 3.1 e 3.2 do Plano Técnico.

REQUISITOS DO ORIENTADOR:
- Filtrar ESTRITAMENTE commits de merge reais (com dois pais)
- Ignorar rebases ou fast-forwards
- Retornar apenas commits com EXATAMENTE 2 pais

Este módulo implementa o FILTRO CRÍTICO mencionado no pseudocódigo:
    SE len(pais.split()) ≠ 2:
        CONTINUAR  # Ignorar (não é merge real)
"""

from git import Commit
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class CommitFilter:
    """
    Filtra commits de merge válidos para mineração.

    Um commit de merge válido DEVE:
    1. Ter EXATAMENTE 2 pais (não 0, não 1, não 3+)
    2. NÃO ser fast-forward (base != left_parent e base != right_parent)
    3. Ter ancestral comum válido (merge base existe)
    """

    def __init__(self):
        self.stats = {
            'total_commits': 0,
            'merge_commits': 0,
            'invalid_parent_count': 0,
            'fast_forwards': 0,
            'no_merge_base': 0,
            'valid_merges': 0
        }

    def is_valid_merge_commit(self, commit: Commit) -> bool:
        """
        Verifica se commit é um merge válido.

        Args:
            commit: Objeto Commit do GitPython

        Returns:
            True se commit é merge válido, False caso contrário

        Examples:
            >>> filter = CommitFilter()
            >>> filter.is_valid_merge_commit(some_commit)
            True  # Se commit tem 2 pais e não é fast-forward
        """
        self.stats['total_commits'] += 1

        # FILTRO 1: Deve ter EXATAMENTE 2 pais
        if len(commit.parents) != 2:
            self.stats['invalid_parent_count'] += 1
            logger.debug(
                f"Ignorando {commit.hexsha[:8]}: "
                f"{len(commit.parents)} pais (esperado: 2)"
            )
            return False

        self.stats['merge_commits'] += 1
        return True

    def is_fast_forward(
        self,
        base: Commit,
        left_parent: Commit,
        right_parent: Commit
    ) -> bool:
        """
        Verifica se merge é fast-forward.

        Um merge é fast-forward se:
        - base == left_parent (right foi mergeado em left sem mudanças)
        - base == right_parent (left foi mergeado em right sem mudanças)

        Args:
            base: Ancestral comum (merge base)
            left_parent: Primeiro pai do merge
            right_parent: Segundo pai do merge

        Returns:
            True se é fast-forward, False caso contrário

        Examples:
            >>> filter = CommitFilter()
            >>> filter.is_fast_forward(base_commit, left_commit, right_commit)
            False  # Se é merge real com mudanças em ambos os lados
        """
        is_ff = (base.hexsha == left_parent.hexsha or
                 base.hexsha == right_parent.hexsha)

        if is_ff:
            self.stats['fast_forwards'] += 1
            logger.debug(
                f"Fast-forward detectado: base={base.hexsha[:8]}, "
                f"left={left_parent.hexsha[:8]}, "
                f"right={right_parent.hexsha[:8]}"
            )

        return is_ff

    def get_merge_base(
        self,
        repo,
        left_parent: Commit,
        right_parent: Commit
    ) -> Optional[Commit]:
        """
        Encontra ancestral comum (merge base) entre dois commits.

        Args:
            repo: Repositório Git
            left_parent: Primeiro pai
            right_parent: Segundo pai

        Returns:
            Commit do merge base, ou None se não encontrado

        Examples:
            >>> filter = CommitFilter()
            >>> base = filter.get_merge_base(repo, left, right)
            >>> base is not None
            True
        """
        try:
            merge_bases = repo.merge_base(left_parent, right_parent)
            if not merge_bases:
                self.stats['no_merge_base'] += 1
                logger.warning(
                    f"Nenhum merge base encontrado entre "
                    f"{left_parent.hexsha[:8]} e {right_parent.hexsha[:8]}"
                )
                return None

            # Retornar primeiro merge base (geralmente há apenas um)
            return merge_bases[0]

        except Exception as e:
            logger.error(f"Erro ao buscar merge base: {e}")
            self.stats['no_merge_base'] += 1
            return None

    def filter_merge_commits(
        self,
        repo,
        commits: List[Commit]
    ) -> List[Dict]:
        """
        Filtra lista de commits, retornando apenas merges válidos.

        Args:
            repo: Repositório Git
            commits: Lista de commits a filtrar

        Returns:
            Lista de dicts com estrutura:
            {
                'commit': Commit do merge,
                'base': Commit do ancestral comum,
                'left': Primeiro pai,
                'right': Segundo pai
            }

        Examples:
            >>> filter = CommitFilter()
            >>> merges = filter.filter_merge_commits(repo, all_commits)
            >>> len(merges) >= 0
            True
        """
        valid_merges = []

        for commit in commits:
            # Filtro 1: Deve ter exatamente 2 pais
            if not self.is_valid_merge_commit(commit):
                continue

            left_parent, right_parent = commit.parents

            # Filtro 2: Encontrar merge base
            base = self.get_merge_base(repo, left_parent, right_parent)
            if base is None:
                continue

            # Filtro 3: Não pode ser fast-forward
            if self.is_fast_forward(base, left_parent, right_parent):
                logger.debug(f"Ignorando {commit.hexsha[:8]}: fast-forward")
                continue

            # Commit válido!
            self.stats['valid_merges'] += 1
            valid_merges.append({
                'commit': commit,
                'base': base,
                'left': left_parent,
                'right': right_parent
            })

            logger.info(
                f"✓ Merge válido: {commit.hexsha[:8]} "
                f"(base: {base.hexsha[:8]}, "
                f"left: {left_parent.hexsha[:8]}, "
                f"right: {right_parent.hexsha[:8]})"
            )

        return valid_merges

    def get_statistics(self) -> Dict:
        """
        Retorna estatísticas do filtro.

        Returns:
            Dict com contadores de cada tipo de rejeição

        Examples:
            >>> filter = CommitFilter()
            >>> filter.filter_merge_commits(repo, commits)
            >>> stats = filter.get_statistics()
            >>> stats['valid_merges'] >= 0
            True
        """
        return self.stats.copy()

    def print_statistics(self):
        """Imprime estatísticas formatadas."""
        print("\n" + "=" * 60)
        print("ESTATÍSTICAS DO FILTRO DE COMMITS")
        print("=" * 60)
        print(f"Total de commits analisados: {self.stats['total_commits']}")
        print(f"  Commits de merge (--merges): {self.stats['merge_commits']}")
        print(f"  └─ Pais inválidos (≠ 2):     {self.stats['invalid_parent_count']}")
        print(f"  └─ Sem merge base:           {self.stats['no_merge_base']}")
        print(f"  └─ Fast-forwards:            {self.stats['fast_forwards']}")
        print(f"\n✓ MERGES VÁLIDOS:              {self.stats['valid_merges']}")
        print("=" * 60)

        if self.stats['merge_commits'] > 0:
            success_rate = (self.stats['valid_merges'] /
                          self.stats['merge_commits'] * 100)
            print(f"Taxa de aprovação: {success_rate:.1f}%")
        print()
