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

# Caminho para o slow-diff3 (configurável via variável de ambiente)
SLOW_DIFF3_PATH = os.environ.get(
    "SLOW_DIFF3_PATH",
    "/tmp/slow-diff3/src/index.js"  # Caminho padrão
)


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

        # ETAPA 3: Executar slow-diff3
        try:
            result_exp, has_conflict = self._run_slow_diff3(base_exp, left_exp, right_exp)
            logger.debug(f"slow-diff3 executado. Conflitos: {has_conflict}")

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

    def _run_slow_diff3(
        self,
        base: str,
        left: str,
        right: str
    ) -> Tuple[str, bool]:
        """
        Executa slow-diff3 em arquivos temporários.

        slow-diff3 é uma implementação em Node.js do algoritmo diff3
        desenvolvida por Leonardo dos Anjos. É invocado com a flag -m (merge),
        que produz saída no formato de conflitos do Git.

        Args:
            base: Conteúdo base explodido
            left: Conteúdo left explodido
            right: Conteúdo right explodido

        Returns:
            Tupla (saída_slow_diff3, tem_conflito)
            - saída_slow_diff3: Resultado do merge (string)
            - tem_conflito: True se há marcadores de conflito na saída

        Note:
            ATENÇÃO: Ordem dos argumentos é LEFT, BASE, RIGHT (não base, left, right!)
            slow-diff3 sempre retorna exit code 0, então detectamos conflitos
            pela presença de marcadores <<<<<<< na saída.

            Marcadores usados pelo slow-diff3:
            <<<<<<<  (início do conflito)
            |||||||  (separador base)
            =======  (separador entre left e right)
            >>>>>>>  (fim do conflito)
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            base_file = Path(tmpdir) / "base"
            left_file = Path(tmpdir) / "left"
            right_file = Path(tmpdir) / "right"

            # Escrever conteúdos em arquivos temporários
            base_file.write_text(base, encoding="utf-8")
            left_file.write_text(left, encoding="utf-8")
            right_file.write_text(right, encoding="utf-8")

            # Executar slow-diff3
            # ATENÇÃO: Ordem é LEFT, BASE, RIGHT (diferente do diff3 GNU!)
            # Formato: node slow-diff3/src/index.js <left> <base> <right> -m
            result = subprocess.run(
                [
                    "node",
                    SLOW_DIFF3_PATH,
                    str(left_file),   # LEFT primeiro
                    str(base_file),   # BASE no meio
                    str(right_file),  # RIGHT por último
                    "-m"              # flag de merge
                ],
                capture_output=True,
                text=True,
                encoding="utf-8"
            )

            # slow-diff3 sempre retorna 0, então detectamos conflito pela saída
            output = result.stdout if result.stdout else result.stderr

            # Detectar conflito pela presença de marcadores
            has_conflict = "<<<<<<<" in output

            return output, has_conflict

    def _run_slow_diff3_debug(
        self,
        base: str,
        left: str,
        right: str
    ) -> str:
        """
        Executa slow-diff3 em modo debug para análise de matchings.

        Útil para entender como o algoritmo está casando as linhas
        e diagnosticar problemas de alinhamento.

        Args:
            base: Conteúdo base explodido
            left: Conteúdo left explodido
            right: Conteúdo right explodido

        Returns:
            String com informações de debug (matchings L-B e B-R, chunks)

        Example:
            >>> csdiff = CSDiffWeb(".ts")
            >>> debug_info = csdiff._run_slow_diff3_debug(base, left, right)
            >>> print(debug_info)
            L-B matching:
            1-1    (L)    |    1-1    (B)
            ...
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            base_file = Path(tmpdir) / "base"
            left_file = Path(tmpdir) / "left"
            right_file = Path(tmpdir) / "right"

            # Escrever conteúdos em arquivos temporários
            base_file.write_text(base, encoding="utf-8")
            left_file.write_text(left, encoding="utf-8")
            right_file.write_text(right, encoding="utf-8")

            # Executar slow-diff3 em modo debug (-d)
            result = subprocess.run(
                [
                    "node",
                    SLOW_DIFF3_PATH,
                    str(left_file),
                    str(base_file),
                    str(right_file),
                    "-d"  # flag de debug
                ],
                capture_output=True,
                text=True,
                encoding="utf-8"
            )

            return result.stdout

    def _fallback_diff3(
        self,
        base: str,
        left: str,
        right: str
    ) -> Tuple[str, bool, int]:
        """
        Fallback para slow-diff3 puro (sem explosão).

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
        logger.debug("Usando slow-diff3 puro (sem separadores)")

        result, has_conflict = self._run_slow_diff3(base, left, right)
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
