"""
Filtro de arquivos problemáticos (minificados, linha única, etc.).
Seção 4.4 do Plano Técnico.

Arquivos minificados causam "falha catastrófica" no SepMerge conforme
identificado no TCC de Leonardo (Seção 4.2). Este módulo implementa
heurísticas para detectar e excluir esses arquivos ANTES do processamento.
"""

from typing import List


class FileFilter:
    """
    Detecta e filtra arquivos problemáticos que devem ser ignorados.

    Critérios de rejeição:
    1. Arquivos de linha única ou muito pequenos (< 3 linhas)
    2. Arquivos minificados (linhas muito longas, avg > 200 chars)
    3. Nomes de arquivo indicando minificação (.min.js, .bundle.js)

    Referência: TCC Leonardo, Seção 4.2 - Análise JavaScript
    """

    # Heurísticas baseadas em análise empírica
    MAX_LINE_LENGTH_FOR_MINIFIED = 500  # Se qualquer linha > 500 chars → minificado
    MIN_LINES_FOR_VALID = 3             # Arquivos com < 3 linhas são rejeitados
    MAX_AVG_LINE_LENGTH = 200           # Média > 200 chars indica minificação

    def should_skip(self, content: str, filename: str = "") -> bool:
        """
        Determina se um arquivo deve ser ignorado no processamento.

        Args:
            content: Conteúdo completo do arquivo como string
            filename: Nome do arquivo (opcional, usado para padrões de nome)

        Returns:
            True se arquivo deve ser IGNORADO, False se deve ser processado

        Examples:
            >>> filter = FileFilter()
            >>> filter.should_skip("const x = 1;")
            True  # Muito pequeno (1 linha)

            >>> minified = "const a=1,b=2,c=3;" * 100  # Linha muito longa
            >>> filter.should_skip(minified)
            True

            >>> normal = "function foo() {\\n  return 42;\\n}"
            >>> filter.should_skip(normal)
            False
        """
        # Verificar padrão no nome do arquivo primeiro (mais rápido)
        if filename and self.is_minified_filename(filename):
            return True

        # Analisar conteúdo do arquivo
        lines = content.split("\n")

        # Filtro 1: Arquivo muito pequeno
        if len(lines) < self.MIN_LINES_FOR_VALID:
            return True

        # Filtro 2: Arquivo vazio ou só com whitespace
        non_empty_lines = [line for line in lines if line.strip()]
        if not non_empty_lines:
            return True

        # Filtro 3: Linhas muito longas (característica de minificados)
        max_length = max(len(line) for line in non_empty_lines)
        if max_length > self.MAX_LINE_LENGTH_FOR_MINIFIED:
            return True

        # Filtro 4: Média de tamanho de linha muito alta
        avg_length = sum(len(line) for line in non_empty_lines) / len(non_empty_lines)
        if avg_length > self.MAX_AVG_LINE_LENGTH:
            return True

        # Passou em todos os filtros → arquivo é válido
        return False

    def is_minified_filename(self, filename: str) -> bool:
        """
        Verifica se o nome do arquivo indica minificação.

        Args:
            filename: Nome ou caminho do arquivo

        Returns:
            True se nome indica arquivo minificado

        Examples:
            >>> filter = FileFilter()
            >>> filter.is_minified_filename("bundle.min.js")
            True

            >>> filter.is_minified_filename("app.bundle.js")
            True

            >>> filter.is_minified_filename("index.ts")
            False
        """
        # Padrões comuns de nomes de arquivos minificados
        minified_patterns = [
            ".min.js",
            ".min.ts",
            ".min.jsx",
            ".min.tsx",
            ".bundle.js",
            ".bundle.ts",
            ".prod.js",
            "-min.js",
            "-min.ts",
            ".umd.js",       # Universal Module Definition (geralmente minificado)
            ".esm.min.js",   # ES Module minificado
        ]

        filename_lower = filename.lower()
        return any(pattern in filename_lower for pattern in minified_patterns)

    def get_skip_reason(self, content: str, filename: str = "") -> str:
        """
        Retorna descrição detalhada do motivo de rejeição (para logging).

        Args:
            content: Conteúdo do arquivo
            filename: Nome do arquivo

        Returns:
            String descrevendo o motivo de rejeição, ou vazio se válido

        Examples:
            >>> filter = FileFilter()
            >>> filter.get_skip_reason("x=1;")
            'Arquivo muito pequeno: 1 linhas (mínimo: 3)'
        """
        if filename and self.is_minified_filename(filename):
            return f"Nome indica minificação: {filename}"

        lines = content.split("\n")

        if len(lines) < self.MIN_LINES_FOR_VALID:
            return f"Arquivo muito pequeno: {len(lines)} linhas (mínimo: {self.MIN_LINES_FOR_VALID})"

        non_empty_lines = [line for line in lines if line.strip()]
        if not non_empty_lines:
            return "Arquivo vazio ou só com whitespace"

        max_length = max(len(line) for line in non_empty_lines)
        if max_length > self.MAX_LINE_LENGTH_FOR_MINIFIED:
            return f"Linha muito longa detectada: {max_length} chars (limite: {self.MAX_LINE_LENGTH_FOR_MINIFIED})"

        avg_length = sum(len(line) for line in non_empty_lines) / len(non_empty_lines)
        if avg_length > self.MAX_AVG_LINE_LENGTH:
            return f"Média de tamanho de linha muito alta: {avg_length:.1f} chars (limite: {self.MAX_AVG_LINE_LENGTH})"

        return ""  # Arquivo válido
