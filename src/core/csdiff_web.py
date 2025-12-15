import subprocess
import tempfile
import os
from pathlib import Path
from typing import Tuple, List
import logging

from .preprocessor import Preprocessor
from .postprocessor import Postprocessor
from .diff3_parser import Diff3Parser, ConflictBlock, NormalBlock
from .filters import FileFilter # Mantido para adaptação JS

logger = logging.getLogger(__name__)

class CSDiffWeb:
    """
    Implementação Python do algoritmo SepMerge (Two-Pass).
    1. Executa diff3 padrão.
    2. Se houver conflito, recorta o bloco e aplica CSDiff (Explode -> Diff3 -> Implode) localmente.
    """

    def __init__(self, extension: str, skip_filter: bool = False):
        self.extension = extension
        self.preprocessor = Preprocessor(extension)
        self.postprocessor = Postprocessor()
        self.filter = FileFilter()
        self.skip_filter = skip_filter

    def merge(self, base: str, left: str, right: str, filename: str = "") -> Tuple[str, bool, int]:
        
        # Filtro de minificados (Adaptação para JS)
        if not self.skip_filter and self.filter.should_skip(base, filename):
            return self._run_raw_diff3(base, left, right)

        # PASSO 1: Diff3 Global (Rápido)
        merged_raw, has_conflict = self._run_raw_diff3(base, left, right)

        if not has_conflict:
            return merged_raw, False, 0

        # PASSO 2: Parsear Blocos
        # O diff3 retorna uma string única, precisamos quebrar em linhas para o parser
        blocks = Diff3Parser.parse(merged_raw.splitlines(keepends=True))

        # PASSO 3: Resolver Conflitos Localmente
        final_content_parts = []
        
        for block in blocks:
            if isinstance(block, ConflictBlock):
                # Extrai o texto cru de cada parte do conflito
                l_txt = "".join(block.left_lines)
                b_txt = "".join(block.base_lines)
                r_txt = "".join(block.right_lines)
                
                # Aplica o algoritmo CSDiff APENAS neste bloco
                resolved_chunk = self._run_csdiff_on_block(b_txt, l_txt, r_txt)
                final_content_parts.append(resolved_chunk)
            else:
                # Mantém bloco normal
                final_content_parts.append("".join(block.lines))

        final_result = "".join(final_content_parts)
        final_conflicts = self.postprocessor.count_conflicts(final_result)
        
        return final_result, final_conflicts > 0, final_conflicts

    def _run_csdiff_on_block(self, base: str, left: str, right: str) -> str:
        """
        Executa a lógica 'Explode -> Diff3 -> Clean' em um pedaço de texto.
        """
        # 1. Explode
        base_exp = self.preprocessor.explode(base)
        left_exp = self.preprocessor.explode(left)
        right_exp = self.preprocessor.explode(right)

        # 2. Diff3 nos explodidos
        merged_exp, _ = self._run_raw_diff3(base_exp, left_exp, right_exp)

        # 3. Limpa (Implode)
        # Nota: O SepMerge Java chama removeMarkers aqui
        return self.postprocessor.reconstruct(merged_exp, self.extension)

    # Em src/core/csdiff_web.py

    def _run_raw_diff3(self, base: str, left: str, right: str) -> Tuple[str, bool]:
        with tempfile.TemporaryDirectory() as tmpdir:
            base_path = Path(tmpdir) / "base"
            left_path = Path(tmpdir) / "left"
            right_path = Path(tmpdir) / "right"

            base_path.write_text(base, encoding="utf-8")
            left_path.write_text(left, encoding="utf-8")
            right_path.write_text(right, encoding="utf-8")

            # Usamos git merge-file com --diff3 para garantir que o bloco ||||||| (base) apareça.
            # O flag -p imprime no stdout (capture_output pega isso).
            cmd = [
                "git", "merge-file", 
                "-p", 
                "--diff3", 
                str(left_path), 
                str(base_path), 
                str(right_path)
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
            
            # git merge-file retorna:
            # 0: sem conflito
            # positivo: com conflito
            # negativo: erro
            has_conflict = result.returncode > 0
            
            return result.stdout, has_conflict

    def get_statistics(self, base: str, left: str, right: str) -> dict:
        return {
            'base_lines': len(base.splitlines()),
            'extension': self.extension
        }