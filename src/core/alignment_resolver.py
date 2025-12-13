"""
Resolução do Problema de Alinhamento (Alignment Problem).
Seção 4.3 do Plano Técnico.

PROBLEMA IDENTIFICADO (TCC Leonardo, Seção 2.1.3, Figura 23):
Quando código é explodido em muitas linhas pequenas e idênticas (ex: "{", "}"),
o algoritmo diff3 confunde o casamento de linhas, gerando conflitos espúrios.

SOLUÇÃO DE 3 CAMADAS:
1. Tamanho Mínimo de Linha (MIN_LINE_LENGTH = 8 chars)
2. Contexto de Aninhamento (depth tracking)
3. Hash de Contexto (marcadores únicos por escopo)

Esta abordagem garante que cada separador tenha um identificador único,
permitindo ao diff3 distinguir corretamente "{" de funções diferentes.
"""

import hashlib
from typing import Tuple


class AlignmentResolver:
    """
    Resolve problema de alinhamento com marcadores contextuais.

    Cada token processado recebe um marcador único baseado em:
    - Profundidade de aninhamento (depth)
    - Hash do contexto precedente (30 caracteres)

    Exemplo de transformação:
        Antes: function foo() { bar(); }
        Depois: function foo() §§CSDIFF_0_a3b2c1§§{ bar() §§CSDIFF_1_d4e5f6§§; §§CSDIFF_1_d4e5f6§§}
    """

    # Configurações do resolvedor
    MIN_LINE_LENGTH = 8      # Tamanho mínimo de linha após explosão
    CONTEXT_WINDOW = 30      # Chars de contexto para hash
    MARKER_PREFIX = "§§CSDIFF"  # Prefixo único para marcadores

    def __init__(self):
        """Inicializa o resolvedor com estado limpo."""
        self.depth = 0                    # Profundidade atual de aninhamento
        self.context_stack = []           # Stack de contextos por nível
        self.current_line_length = 0      # Tamanho da linha atual

    def reset(self):
        """Reseta estado para processar novo arquivo."""
        self.depth = 0
        self.context_stack = []
        self.current_line_length = 0

    def process_token(
        self,
        token: str,
        preceding_context: str
    ) -> Tuple[str, bool]:
        """
        Processa um token e decide se deve quebrar linha.

        Args:
            token: Separador encontrado (ex: "{", "}", ";")
            preceding_context: Código antes do token na linha atual

        Returns:
            Tupla (token_marcado, deve_quebrar_linha)

        Examples:
            >>> resolver = AlignmentResolver()
            >>> token, should_break = resolver.process_token("{", "function foo() ")
            >>> token
            '§§CSDIFF_0_3a4b5c§§{'
            >>> should_break
            True
        """
        # Atualizar profundidade de aninhamento
        self._update_depth(token)

        # Criar marcador contextual único
        marked_token = self._create_marker(token, preceding_context)

        # Decidir se deve quebrar linha
        should_break = self._should_break_line(preceding_context)

        # Atualizar tamanho da linha atual
        if should_break:
            self.current_line_length = len(marked_token)
        else:
            self.current_line_length += len(marked_token)

        return marked_token, should_break

    def _update_depth(self, token: str):
        """
        Atualiza profundidade de aninhamento baseado no token.

        Tokens de abertura: { [ (
        Tokens de fechamento: } ] )
        """
        if token in ("{", "[", "("):
            self.depth += 1
            # Empilhar contexto vazio (será preenchido no próximo token)
            self.context_stack.append("")
        elif token in ("}", "]", ")"):
            self.depth = max(0, self.depth - 1)
            # Desempilhar contexto
            if self.context_stack:
                self.context_stack.pop()

    def _create_marker(self, token: str, context: str) -> str:
        """
        Cria marcador único com contexto.

        Formato: §§CSDIFF_<depth>_<hash>§§<token>

        Args:
            token: Separador original
            context: Contexto precedente

        Returns:
            Token com marcador contextual único
        """
        # Extrair janela de contexto (últimos CONTEXT_WINDOW chars)
        context_window = context[-self.CONTEXT_WINDOW:] if context else ""

        # Se não há contexto, usar marcador simples com depth
        if not context_window.strip():
            return f"{self.MARKER_PREFIX}_{self.depth}§§{token}"

        # Calcular hash do contexto (6 primeiros chars do MD5)
        context_hash = hashlib.md5(context_window.encode()).hexdigest()[:6]

        # Retornar token marcado
        return f"{self.MARKER_PREFIX}_{self.depth}_{context_hash}§§{token}"

    def _should_break_line(self, preceding_context: str) -> bool:
        """
        Decide se deve quebrar linha após o token.

        Critérios:
        1. Linha atual já tem pelo menos MIN_LINE_LENGTH caracteres
        2. OU: Contexto precedente termina com newline (já estamos em nova linha)

        Args:
            preceding_context: Código antes do token

        Returns:
            True se deve quebrar linha, False caso contrário
        """
        # Se contexto precedente já termina com newline, não quebrar novamente
        if preceding_context.endswith("\n"):
            return False

        # Se linha atual tem tamanho suficiente, quebrar
        # Isso evita criar linhas muito pequenas (< 8 chars)
        current_line = preceding_context.split("\n")[-1] if "\n" in preceding_context else preceding_context
        return len(current_line) >= self.MIN_LINE_LENGTH

    def extract_original_token(self, marked_token: str) -> str:
        """
        Extrai token original de um token marcado.

        Args:
            marked_token: Token com marcador (ex: "§§CSDIFF_0_a3b2c1§§{")

        Returns:
            Token original sem marcador (ex: "{")

        Examples:
            >>> resolver = AlignmentResolver()
            >>> resolver.extract_original_token("§§CSDIFF_0_a3b2c1§§{")
            '{'

            >>> resolver.extract_original_token("§§CSDIFF_1§§;")
            ';'
        """
        if self.MARKER_PREFIX in marked_token:
            # Encontrar o separador "§§" final
            parts = marked_token.split("§§")
            if len(parts) >= 3:
                return parts[-1]  # Último elemento após "§§"
        return marked_token  # Já é token não marcado

    def is_marked_token(self, token: str) -> bool:
        """
        Verifica se um token possui marcador contextual.

        Args:
            token: Token a verificar

        Returns:
            True se token possui marcador

        Examples:
            >>> resolver = AlignmentResolver()
            >>> resolver.is_marked_token("§§CSDIFF_0§§{")
            True

            >>> resolver.is_marked_token("{")
            False
        """
        return self.MARKER_PREFIX in token
