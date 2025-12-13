"""
Pós-processador: Reconstrói código após merge do diff3.
Complemento do Preprocessor (Seção 2.4 do Plano Técnico).

O postprocessor recebe o resultado do diff3 (que operou no código explodido)
e reconstrói o código original, removendo marcadores contextuais e
restaurando a formatação.

FLUXO:
1. Receber resultado do diff3 (com marcadores §§CSDIFF§§)
2. Remover todos os marcadores contextuais
3. Restaurar linhas vazias originais (§§EMPTY_LINE§§)
4. Opcionalmente: compactar linhas pequenas
5. Retornar código final
"""

import re
from typing import List


class Postprocessor:
    """
    Reconstrói código após merge com separadores.

    Remove marcadores adicionados pelo preprocessor e AlignmentResolver,
    restaurando código para formato legível.
    """

    # Padrão regex para detectar marcadores contextuais
    # Formato: §§CSDIFF_<depth>_<hash>§§<token>
    MARKER_PATTERN = re.compile(r"§§CSDIFF(?:_\d+)?(?:_[a-f0-9]{6})?§§")

    def reconstruct(self, exploded_code: str) -> str:
        """
        Reconstrói código removendo marcadores.

        Args:
            exploded_code: Código após diff3 (com marcadores)

        Returns:
            Código reconstruído sem marcadores

        Examples:
            >>> pp = Postprocessor()
            >>> code = "function foo() §§CSDIFF_0_a3b2c1§§{\\n  return 42§§CSDIFF_1_d4e5f6§§;\\n§§CSDIFF_0_a3b2c1§§}"
            >>> pp.reconstruct(code)
            'function foo() {\\n  return 42;\\n}'
        """
        # Remover todos os marcadores contextuais
        clean_code = self.MARKER_PATTERN.sub("", exploded_code)

        # Restaurar linhas vazias
        clean_code = clean_code.replace("§§EMPTY_LINE§§", "")

        # Opcional: compactar linhas muito pequenas (se desejado)
        # clean_code = self._compact_small_lines(clean_code)

        return clean_code

    def reconstruct_with_conflicts(self, exploded_code: str) -> str:
        """
        Reconstrói código preservando marcadores de conflito do diff3.

        Marcadores de conflito do diff3:
        - <<<<<<< (início do conflito)
        - ||||||| (versão base)
        - ======= (separador)
        - >>>>>>> (fim do conflito)

        Args:
            exploded_code: Código após diff3 com possíveis conflitos

        Returns:
            Código reconstruído com conflitos preservados

        Examples:
            >>> pp = Postprocessor()
            >>> code = "<<<<<<< left\\nconst x = 1§§CSDIFF_0§§;\\n=======\\nconst x = 2§§CSDIFF_0§§;\\n>>>>>>> right"
            >>> result = pp.reconstruct_with_conflicts(code)
            >>> "<<<<<<< left" in result
            True
            >>> "§§CSDIFF" in result
            False
        """
        # Mesmo processo: remover marcadores mas preservar estrutura de conflito
        return self.reconstruct(exploded_code)

    def _compact_small_lines(self, code: str) -> str:
        """
        Compacta linhas muito pequenas em uma só linha (opcional).

        Exemplo:
            Antes:
                {
                return 42
                ;
                }

            Depois:
                { return 42; }

        Args:
            code: Código a compactar

        Returns:
            Código com linhas pequenas compactadas

        Note:
            Este método é OPCIONAL e pode alterar formatação original.
            Use apenas se usuário preferir código mais compacto.
        """
        lines = code.split("\n")
        compacted = []
        buffer = []

        for line in lines:
            stripped = line.strip()

            # Se linha tem só um token pequeno, adicionar ao buffer
            if len(stripped) <= 3 and stripped in "{};,()[]":
                buffer.append(stripped)
            else:
                # Descarregar buffer + linha atual
                if buffer:
                    compacted.append(" ".join(buffer) + " " + stripped)
                    buffer = []
                else:
                    compacted.append(line)

        # Descarregar buffer restante
        if buffer:
            compacted.append(" ".join(buffer))

        return "\n".join(compacted)

    def count_conflicts(self, code: str) -> int:
        """
        Conta número de conflitos no resultado do merge.

        Args:
            code: Código após merge

        Returns:
            Número de blocos de conflito (conta marcadores <<<<<<<)

        Examples:
            >>> pp = Postprocessor()
            >>> code = "<<<<<<< left\\nfoo\\n=======\\nbar\\n>>>>>>> right"
            >>> pp.count_conflicts(code)
            1
        """
        return code.count("<<<<<<<")

    def extract_conflict_blocks(self, code: str) -> List[dict]:
        """
        Extrai blocos de conflito do código (para análise).

        Args:
            code: Código com conflitos

        Returns:
            Lista de dicts com informação sobre cada conflito:
            - 'left': versão left
            - 'base': versão base (se presente)
            - 'right': versão right
            - 'line_start': linha onde conflito começa

        Examples:
            >>> pp = Postprocessor()
            >>> code = "<<<<<<< left\\nfoo\\n=======\\nbar\\n>>>>>>> right"
            >>> conflicts = pp.extract_conflict_blocks(code)
            >>> len(conflicts)
            1
            >>> conflicts[0]['left']
            'foo'
            >>> conflicts[0]['right']
            'bar'
        """
        conflicts = []
        lines = code.split("\n")
        i = 0

        while i < len(lines):
            if lines[i].startswith("<<<<<<<"):
                # Início de conflito
                conflict = {
                    'line_start': i,
                    'left': [],
                    'base': [],
                    'right': []
                }

                i += 1
                current_section = 'left'

                # Ler conteúdo do conflito
                while i < len(lines):
                    if lines[i].startswith("|||||||"):
                        current_section = 'base'
                    elif lines[i].startswith("======="):
                        current_section = 'right'
                    elif lines[i].startswith(">>>>>>>"):
                        # Fim do conflito
                        conflict['left'] = "\n".join(conflict['left'])
                        conflict['base'] = "\n".join(conflict['base'])
                        conflict['right'] = "\n".join(conflict['right'])
                        conflicts.append(conflict)
                        break
                    else:
                        conflict[current_section].append(lines[i])

                    i += 1
            i += 1

        return conflicts

    def has_conflicts(self, code: str) -> bool:
        """
        Verifica se código tem conflitos.

        Args:
            code: Código a verificar

        Returns:
            True se há conflitos, False caso contrário

        Examples:
            >>> pp = Postprocessor()
            >>> pp.has_conflicts("const x = 1;")
            False
            >>> pp.has_conflicts("<<<<<<< left\\nfoo\\n=======\\nbar\\n>>>>>>> right")
            True
        """
        return "<<<<<<<" in code
