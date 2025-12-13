"""
Pré-processador: Explode código em linhas baseado em separadores sintáticos.
Seção 2.4 do Plano Técnico.

O preprocessor é o núcleo do CSDiff-Web. Ele transforma código denso em
múltiplas linhas usando separadores sintáticos, permitindo que diff3 opere
em granularidade mais fina que linhas de texto puro.

FLUXO:
1. Detectar strings literais (não quebrar dentro delas)
2. Iterar por caractere do código
3. Para cada separador encontrado FORA de strings:
   - Adicionar marcador contextual (via AlignmentResolver)
   - Quebrar linha se necessário
4. Retornar código explodido + mapa de posições
"""

import re
from typing import List, Tuple, Set

from .separators import get_separators
from .alignment_resolver import AlignmentResolver


class Preprocessor:
    """
    Explode código em linhas baseado em separadores sintáticos.

    Este processador implementa a estratégia de explosão definida no
    Plano Técnico (Seção 2.4), com proteção contra quebra dentro de
    strings literais e marcadores contextuais para evitar o Alignment Problem.
    """

    def __init__(self, extension: str):
        """
        Inicializa preprocessor para uma extensão específica.

        Args:
            extension: Extensão do arquivo (ex: ".ts", ".tsx")
        """
        self.separators = get_separators(extension)
        self.extension = extension
        self.resolver = AlignmentResolver()

    def is_inside_string(self, code: str, pos: int) -> bool:
        """
        Verifica se posição está dentro de string literal.

        Detecta strings com:
        - Aspas simples: 'texto'
        - Aspas duplas: "texto"
        - Template literals: `texto ${expr}`

        Lida corretamente com escapes (\\', \\", \\`)

        Args:
            code: Código completo
            pos: Posição (índice) a verificar

        Returns:
            True se posição está dentro de string literal

        Examples:
            >>> p = Preprocessor(".ts")
            >>> code = "const x = 'hello'; const y = 42;"
            >>> p.is_inside_string(code, 10)  # Dentro de 'hello'
            True
            >>> p.is_inside_string(code, 20)  # Fora da string
            False
        """
        in_single = False
        in_double = False
        in_template = False
        i = 0

        while i < pos:
            char = code[i]

            # Escape: pular próximo caractere
            if char == "\\" and i + 1 < len(code):
                i += 2
                continue

            # Toggle estado das strings
            if char == "'" and not in_double and not in_template:
                in_single = not in_single
            elif char == '"' and not in_single and not in_template:
                in_double = not in_double
            elif char == "`" and not in_single and not in_double:
                in_template = not in_template

            i += 1

        return in_single or in_double or in_template

    def explode(self, code: str) -> Tuple[str, List[int]]:
        """
        Explode código em novas linhas nos separadores.

        Este é o método principal do preprocessor. Ele:
        1. Itera por todo o código caractere por caractere
        2. Detecta separadores (respeitando ordem de tamanho)
        3. Verifica se separador está dentro de string
        4. Se válido, adiciona marcador contextual e quebra linha
        5. Retorna código explodido + mapa de posições originais

        Args:
            code: Código original a explodir

        Returns:
            Tupla (código_explodido, mapa_de_posições)
            - código_explodido: string com separadores marcados
            - mapa_de_posições: lista de índices originais de cada linha

        Examples:
            >>> p = Preprocessor(".ts")
            >>> code = "function foo() { return 42; }"
            >>> exploded, positions = p.explode(code)
            >>> "§§CSDIFF" in exploded
            True
        """
        # Resetar estado do resolver
        self.resolver.reset()

        result_lines = []
        position_map = []
        current_line = []
        i = 0

        while i < len(code):
            matched = False

            # Tentar casar com cada separador (do maior para o menor)
            for sep in self.separators:
                if code[i:i+len(sep)] == sep:
                    # Verificar se NÃO está dentro de string
                    if not self.is_inside_string(code, i):
                        # Contexto precedente: tudo na linha atual
                        preceding = "".join(current_line)

                        # Adicionar conteúdo antes do separador (se houver)
                        if current_line:
                            result_lines.append("".join(current_line))
                            position_map.append(i - len(preceding))

                        # Processar separador com marcador contextual
                        marked_sep, should_break = self.resolver.process_token(
                            sep, preceding
                        )

                        # Adicionar separador como linha própria
                        result_lines.append(marked_sep)
                        position_map.append(i)

                        # Limpar linha atual
                        current_line = []

                        # Avançar índice pelo tamanho do separador
                        i += len(sep)
                        matched = True
                        break

            # Se não casou com nenhum separador, adicionar caractere à linha
            if not matched:
                current_line.append(code[i])
                i += 1

        # Adicionar última linha se houver conteúdo
        if current_line:
            result_lines.append("".join(current_line))
            position_map.append(len(code) - len("".join(current_line)))

        # Juntar linhas com newline
        exploded_code = "\n".join(result_lines)

        return exploded_code, position_map

    def preserve_empty_lines(self, code: str) -> str:
        """
        Preserva linhas vazias originais após explosão.

        Linhas vazias têm significado semântico em código (separação lógica),
        então devemos mantê-las após a explosão.

        Args:
            code: Código original

        Returns:
            Código com marcadores para linhas vazias

        Note:
            Este método é opcional e pode ser usado antes de explode()
            se o usuário quiser preservar formatação original.
        """
        # Substituir linhas vazias por marcador especial
        lines = code.split("\n")
        marked_lines = []

        for line in lines:
            if line.strip() == "":
                marked_lines.append("§§EMPTY_LINE§§")
            else:
                marked_lines.append(line)

        return "\n".join(marked_lines)

    def count_separators(self, code: str) -> dict:
        """
        Conta ocorrências de cada separador no código (para debugging).

        Args:
            code: Código a analisar

        Returns:
            Dict mapeando separador → contagem

        Examples:
            >>> p = Preprocessor(".ts")
            >>> counts = p.count_separators("function foo() { return 42; }")
            >>> counts["{"]
            1
            >>> counts[";"]
            1
        """
        counts = {sep: 0 for sep in self.separators}

        i = 0
        while i < len(code):
            for sep in self.separators:
                if code[i:i+len(sep)] == sep:
                    if not self.is_inside_string(code, i):
                        counts[sep] += 1
                    break
            i += 1

        return counts
