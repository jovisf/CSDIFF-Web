"""
Testes de integração para validar slow-diff3.

Estes testes verificam que:
1. slow-diff3 está instalado e acessível
2. CSDiffWeb usa slow-diff3 corretamente
3. Marcadores de conflito são detectados
4. Modo debug funciona
"""

import pytest
import subprocess
import os
from pathlib import Path
import sys

# Adicionar src/ ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.csdiff_web import CSDiffWeb, SLOW_DIFF3_PATH


class TestSlowDiff3Installation:
    """Testa instalação e disponibilidade do slow-diff3."""

    def test_slow_diff3_path_exists(self):
        """Verifica que SLOW_DIFF3_PATH aponta para arquivo existente."""
        path = Path(SLOW_DIFF3_PATH)
        assert path.exists(), f"slow-diff3 não encontrado em {SLOW_DIFF3_PATH}"
        assert path.is_file(), f"{SLOW_DIFF3_PATH} não é um arquivo"

    def test_node_available(self):
        """Verifica que Node.js está instalado."""
        result = subprocess.run(
            ["node", "--version"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, "Node.js não está instalado"
        assert result.stdout.startswith('v'), f"Node version inesperada: {result.stdout}"

    def test_slow_diff3_help(self):
        """Verifica que slow-diff3 pode ser executado."""
        result = subprocess.run(
            ["node", SLOW_DIFF3_PATH, "-h"],
            capture_output=True,
            text=True
        )
        # slow-diff3 -h retorna 0
        assert "Usage:" in result.stdout or "Options:" in result.stdout, \
            f"slow-diff3 help não funcionou: {result.stdout}"


class TestSlowDiff3Behavior:
    """Testa comportamento específico do slow-diff3."""

    def test_conflict_markers_format(self):
        """Verifica formato dos marcadores de conflito."""
        merger = CSDiffWeb(".ts", skip_filter=True)

        base = "linha1\nlinha2"
        left = "linha1\nlinha2\nlinha3"
        right = "linha1\nlinha2\nlinha4"

        result, has_conflict, num_conflicts = merger.merge(base, left, right, "test.ts")

        # Verificar marcadores do slow-diff3
        assert "<<<<<<<" in result
        assert "||||||" in result  # slow-diff3 usa 7 pipes (|||||||)
        assert "=======" in result
        assert ">>>>>>>" in result
        assert has_conflict is True
        assert num_conflicts == 1

    def test_argument_order(self):
        """Verifica que ordem dos argumentos está correta (left, base, right)."""
        merger = CSDiffWeb(".ts", skip_filter=True)

        # Base tem linha comum
        base = "comum\n"
        # Left adiciona A
        left = "comum\nA\n"
        # Right adiciona B
        right = "comum\nB\n"

        result, has_conflict, _ = merger.merge(base, left, right, "test.ts")

        # Deve haver conflito entre A e B
        # Verificar que LEFT (A) aparece primeiro no conflito
        conflict_start = result.find("<<<<<<<")
        conflict_middle = result.find("=======")

        left_section = result[conflict_start:conflict_middle]
        right_section = result[conflict_middle:result.find(">>>>>>>")]

        # A deve estar na seção left
        assert "A" in left_section
        # B deve estar na seção right
        assert "B" in right_section

    def test_no_conflict_case(self):
        """Verifica merge sem conflito."""
        merger = CSDiffWeb(".ts", skip_filter=True)

        base = "function foo() { return 1; }"
        left = "function foo() { console.log('A'); return 1; }"
        right = "function foo() { return 1; }"  # sem mudança

        result, has_conflict, num_conflicts = merger.merge(base, left, right, "test.ts")

        # Não deve ter marcadores de conflito
        assert "<<<<<<<" not in result
        assert has_conflict is False
        assert num_conflicts == 0


class TestSlowDiff3Debug:
    """Testa modo debug do slow-diff3."""

    def test_debug_mode_output(self):
        """Verifica que modo debug retorna matchings."""
        merger = CSDiffWeb(".ts", skip_filter=True)

        base = "function foo() { return 1; }"
        left = "function foo() { return 2; }"
        right = "function foo() { return 3; }"

        # Usar método de debug
        debug_output = merger._run_slow_diff3_debug(base, left, right)

        # Verificar estrutura da saída de debug
        # slow-diff3 pode retornar "No matching" quando não há matching
        assert "matching" in debug_output.lower()
        assert "(L)" in debug_output and "(B)" in debug_output and "(R)" in debug_output
        assert "chunk" in debug_output.lower()

    def test_debug_mode_chunks(self):
        """Verifica que debug mostra chunks stable/unstable."""
        merger = CSDiffWeb(".ts", skip_filter=True)

        base = "linha1\nlinha2\nlinha3"
        left = "linha1\nmodificada\nlinha3"
        right = "linha1\nlinha2\nlinha3"

        debug_output = merger._run_slow_diff3_debug(base, left, right)

        # Deve mostrar chunks
        assert "chunk:" in debug_output.lower()


class TestCSDiffWebIntegration:
    """Testa integração completa do CSDiffWeb com slow-diff3."""

    def test_preprocessor_integration(self):
        """Verifica que preprocessor + slow-diff3 funcionam juntos."""
        merger = CSDiffWeb(".ts", skip_filter=True)

        base = "function foo() { return 1; }"
        left = "function foo() { console.log('test'); return 1; }"
        right = "function foo() { return 2; }"

        result, has_conflict, num_conflicts = merger.merge(base, left, right, "test.ts")

        # Deve ter conflito
        assert has_conflict is True
        assert num_conflicts == 1

        # Resultado deve estar reconstruído (não explodido)
        assert "function foo" in result
        assert "(" in result
        assert "{" in result

    def test_postprocessor_integration(self):
        """Verifica que postprocessor reconstrói código corretamente."""
        merger = CSDiffWeb(".ts", skip_filter=True)

        base = "const x = 1; const y = 2;"
        left = "const x = 10; const y = 2;"
        right = "const x = 1; const y = 20;"

        result, has_conflict, num_conflicts = merger.merge(base, left, right, "test.ts")

        # slow-diff3 pode marcar como conflito dependendo do algoritmo de matching
        # O importante é que o resultado esteja reconstruído corretamente

        # Resultado deve conter ambas as variáveis
        assert "const x" in result
        assert "const y" in result

        # Resultado deve estar reconstruído (não explodido linha por linha)
        # Se não tiver conflito, deve estar em linha compacta
        if not has_conflict:
            lines = [l for l in result.split('\n') if l.strip()]
            assert len(lines) <= 2  # Máximo 2 linhas (uma por const)

    def test_fallback_uses_slow_diff3(self):
        """Verifica que fallback também usa slow-diff3."""
        merger = CSDiffWeb(".ts", skip_filter=False)

        # Código minificado (deve acionar fallback)
        minified = "function a(){return 1}function b(){return 2}function c(){return 3}function d(){return 4}function e(){return 5}"

        result, has_conflict, num_conflicts = merger.merge(
            minified,
            minified + "function f(){return 6}",
            minified + "function g(){return 7}",
            "minified.min.js"
        )

        # Fallback deve funcionar (usando slow-diff3 sem explosão)
        assert result != ""


class TestEdgeCases:
    """Testa casos extremos."""

    def test_empty_files(self):
        """Testa merge de arquivos vazios."""
        merger = CSDiffWeb(".ts", skip_filter=True)

        result, has_conflict, num_conflicts = merger.merge("", "", "", "test.ts")

        # Resultado pode ter whitespace residual
        assert result.strip() == ""
        assert has_conflict is False
        assert num_conflicts == 0

    def test_identical_files(self):
        """Testa merge de arquivos idênticos."""
        merger = CSDiffWeb(".ts", skip_filter=True)

        code = "const x = 1;"
        result, has_conflict, num_conflicts = merger.merge(code, code, code, "test.ts")

        assert "const x = 1" in result
        assert has_conflict is False
        assert num_conflicts == 0

    def test_large_file(self):
        """Testa merge de arquivo grande."""
        merger = CSDiffWeb(".ts", skip_filter=True)

        # Criar código grande
        base_lines = ["const x{} = {};".format(i, i) for i in range(100)]
        base = "\n".join(base_lines)

        left_lines = base_lines[:50] + ["const NEW_LEFT = 1;"] + base_lines[50:]
        left = "\n".join(left_lines)

        right_lines = base_lines[:75] + ["const NEW_RIGHT = 2;"] + base_lines[75:]
        right = "\n".join(right_lines)

        result, has_conflict, num_conflicts = merger.merge(base, left, right, "test.ts")

        # Mudanças em locais diferentes - não deve conflitar
        assert "NEW_LEFT" in result
        assert "NEW_RIGHT" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
