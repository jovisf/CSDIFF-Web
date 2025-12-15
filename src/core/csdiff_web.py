"""
CSDiff-Web: Wrapper principal para merge com separadores sintáticos.
Seção 2.5 do Plano Técnico.

Este é o ENTRY POINT do CSDiff-Web. Ele orquestra todo o pipeline:
1. Filtrar arquivos problemáticos (minificados)
2. Pré-processar (explodir com separadores)
3. Executar diff3 nos arquivos explodidos
4. Pós-processar (reconstruir código)
5. Retornar resultado + métricas

FLUXO COMPLETO (Seção 2.1 do Plano):
    ENTRADA: base.ts, left.ts, right.ts
         │
         ▼
    ┌────────────────────┐
    │ DETECTAR EXTENSÃO  │
    └────────────────────┘
         │
         ▼
    ┌────────────────────┐
    │ FILTRAR ARQUIVO    │  ← Rejeita minificados
    └────────────────────┘
         │
         ▼
    ┌────────────────────┐
    │ PRÉ-PROCESSAR      │  ← Explosão + marcadores
    └────────────────────┘
         │
         ▼
    ┌────────────────────┐
    │ EXECUTAR diff3     │  ← Merge nos arquivos explodidos
    └────────────────────┘
         │
         ▼
    ┌────────────────────┐
    │ PÓS-PROCESSAR      │  ← Reconstrução
    └────────────────────┘
         │
         ▼
    SAÍDA: merged.ts (com/sem conflitos)
"""

import subprocess
import tempfile
import os
from pathlib import Path
from typing import Tuple, Optional
import logging

from .preprocessor import Preprocessor
from .postprocessor import Postprocessor
from .filters import FileFilter

# Configurar logging
logger = logging.getLogger(__name__)


class CSDiffWeb:
    """
    Wrapper principal do CSDiff-Web.

    Esta classe implementa o merge textual com separadores sintáticos
    para arquivos TypeScript, JavaScript, TSX e JSX.
    """

    def __init__(self, extension: str, skip_filter: bool = False):
        """
        Inicializa CSDiff-Web para uma extensão específica.

        Args:
            extension: Extensão do arquivo (ex: ".ts", ".tsx")
            skip_filter: Se True, não filtra arquivos minificados (útil para testes)
        """
        self.extension = extension
        self.preprocessor = Preprocessor(extension)
        self.postprocessor = Postprocessor()
        self.filter = FileFilter()
        self.skip_filter = skip_filter

        logger.info(f"CSDiff-Web inicializado para extensão: {extension}")

    def merge(
        self,
        base: str,
        left: str,
        right: str,
        filename: str = ""
    ) -> Tuple[str, bool, int]:
        """
        Executa merge com separadores sintáticos.

        Este é o método principal do CSDiff-Web. Recebe três versões
        de um arquivo (base, left, right) e retorna o merge.

        Args:
            base: Conteúdo da versão base (ancestral comum)
            left: Conteúdo da versão left (primeiro pai do merge)
            right: Conteúdo da versão right (segundo pai do merge)
            filename: Nome do arquivo (opcional, para filtro de minificados)

        Returns:
            Tupla (resultado, tem_conflito, num_conflitos)
            - resultado: Código após merge (string)
            - tem_conflito: True se há conflitos não resolvidos
            - num_conflitos: Número de blocos de conflito

        Examples:
            >>> csdiff = CSDiffWeb(".ts")
            >>> base = "function foo() { return 1; }"
            >>> left = "function foo() { return 2; }"
            >>> right = "function foo() { return 3; }"
            >>> result, has_conflict, num = csdiff.merge(base, left, right)
            >>> has_conflict
            True
        """
        logger.debug(f"Iniciando merge para arquivo: {filename or 'sem nome'}")

        # ETAPA 1: Verificar se arquivo deve ser ignorado
        if not self.skip_filter:
            if self.filter.should_skip(base, filename):
                reason = self.filter.get_skip_reason(base, filename)
                logger.warning(f"Arquivo ignorado (fallback para diff3 puro): {reason}")
                return self._fallback_diff3(base, left, right)

        # ETAPA 2: Pré-processar (explodir código)
        try:
            base_exp, _ = self.preprocessor.explode(base)
            left_exp, _ = self.preprocessor.explode(left)
            right_exp, _ = self.preprocessor.explode(right)

            logger.debug("Pré-processamento concluído")
            logger.debug(f"  Base: {len(base.split())} → {len(base_exp.split())} linhas")
            logger.debug(f"  Left: {len(left.split())} → {len(left_exp.split())} linhas")
            logger.debug(f"  Right: {len(right.split())} → {len(right_exp.split())} linhas")

        except Exception as e:
            logger.error(f"Erro no pré-processamento: {e}")
            logger.warning("Fallback para diff3 puro")
            return self._fallback_diff3(base, left, right)

        # ETAPA 3: Executar diff3
        try:
            result_exp, has_conflict = self._run_diff3(base_exp, left_exp, right_exp)
            logger.debug(f"diff3 executado. Conflitos: {has_conflict}")

        except Exception as e:
            logger.error(f"Erro ao executar diff3: {e}")
            return "", True, 0

        # ETAPA 4: Pós-processar (reconstruir código)
        try:
            result = self.postprocessor.reconstruct(result_exp)
            num_conflicts = self.postprocessor.count_conflicts(result)

            logger.debug(f"Pós-processamento concluído. Conflitos finais: {num_conflicts}")

        except Exception as e:
            logger.error(f"Erro no pós-processamento: {e}")
            return result_exp, has_conflict, result_exp.count("<<<<<<<")

        return result, has_conflict, num_conflicts

    def _run_diff3(
        self,
        base: str,
        left: str,
        right: str
    ) -> Tuple[str, bool]:
        """
        Executa diff3 em arquivos temporários.

        diff3 é invocado com a flag -m (merge), que produz saída
        no formato de conflitos do Git.

        Args:
            base: Conteúdo base explodido
            left: Conteúdo left explodido
            right: Conteúdo right explodido

        Returns:
            Tupla (saída_diff3, tem_conflito)
            - saída_diff3: Resultado do merge (string)
            - tem_conflito: True se diff3 retornou código de saída != 0

        Note:
            diff3 retorna:
            - 0: merge bem-sucedido sem conflitos
            - 1: merge com conflitos
            - 2: erro na execução
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            base_file = Path(tmpdir) / "base"
            left_file = Path(tmpdir) / "left"
            right_file = Path(tmpdir) / "right"

            # Escrever conteúdos em arquivos temporários
            base_file.write_text(base, encoding="utf-8")
            left_file.write_text(left, encoding="utf-8")
            right_file.write_text(right, encoding="utf-8")

            # Executar diff3
            # Formato: diff3 -m <left> <base> <right>
            result = subprocess.run(
                ["diff3", "-m", str(left_file), str(base_file), str(right_file)],
                capture_output=True,
                text=True,
                encoding="utf-8"
            )

            # diff3 retorna 0 se sem conflitos, 1 se com conflitos, 2 se erro
            has_conflict = result.returncode != 0

            # Saída pode estar em stdout ou stderr dependendo da versão
            output = result.stdout if result.stdout else result.stderr

            return output, has_conflict

    def _fallback_diff3(
        self,
        base: str,
        left: str,
        right: str
    ) -> Tuple[str, bool, int]:
        """
        Fallback para diff3 puro (sem explosão).

        Usado quando:
        - Arquivo é minificado
        - Pré-processamento falha
        - Usuário deseja comparação com baseline

        Args:
            base: Conteúdo base original
            left: Conteúdo left original
            right: Conteúdo right original

        Returns:
            Tupla (resultado, tem_conflito, num_conflitos)
        """
        logger.debug("Usando diff3 puro (sem separadores)")

        result, has_conflict = self._run_diff3(base, left, right)
        num_conflicts = result.count("<<<<<<<")

        return result, has_conflict, num_conflicts

    def get_statistics(self, base: str, left: str, right: str) -> dict:
        """
        Retorna estatísticas sobre o merge (para análise).

        Args:
            base, left, right: Conteúdos das três versões

        Returns:
            Dict com métricas:
            - 'base_lines': linhas originais da base
            - 'base_exploded_lines': linhas após explosão
            - 'separator_count': número de separadores detectados
            - 'skip_reason': motivo de rejeição (se aplicável)

        Examples:
            >>> csdiff = CSDiffWeb(".ts")
            >>> stats = csdiff.get_statistics("const x = 1;", "", "")
            >>> 'base_lines' in stats
            True
        """
        stats = {
            'base_lines': len(base.split("\n")),
            'left_lines': len(left.split("\n")),
            'right_lines': len(right.split("\n")),
            'extension': self.extension,
        }

        # Adicionar estatísticas de explosão
        try:
            base_exp, _ = self.preprocessor.explode(base)
            stats['base_exploded_lines'] = len(base_exp.split("\n"))
            stats['explosion_ratio'] = stats['base_exploded_lines'] / max(1, stats['base_lines'])
        except:
            stats['base_exploded_lines'] = 0
            stats['explosion_ratio'] = 0

        # Adicionar contagem de separadores
        stats['separator_count'] = self.preprocessor.count_separators(base)

        # Adicionar motivo de skip (se aplicável)
        stats['skip_reason'] = self.filter.get_skip_reason(base)

        return stats
