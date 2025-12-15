"""
Testes unitários para o Preprocessor.
Valida explosão de código, detecção de strings e marcadores contextuais.
"""

import pytest
from src.core.preprocessor import Preprocessor
from src.core.alignment_resolver import AlignmentResolver


class TestStringDetection:
    """Testa detecção de strings literais."""

    def test_single_quotes(self):
        """Deve detectar strings com aspas simples."""
        p = Preprocessor(".ts")
        code = "const x = 'hello';"
        # Posição 11 é dentro de 'hello'
        assert p.is_inside_string(code, 11) == True
        # Posição 18 é depois da string
        assert p.is_inside_string(code, 18) == False

    def test_double_quotes(self):
        """Deve detectar strings com aspas duplas."""
        p = Preprocessor(".ts")
        code = 'const x = "world";'
        assert p.is_inside_string(code, 12) == True
        assert p.is_inside_string(code, 18) == False

    def test_template_literals(self):
        """Deve detectar template literals."""
        p = Preprocessor(".ts")
        code = "const x = `template ${expr}`;"
        assert p.is_inside_string(code, 12) == True
        assert p.is_inside_string(code, 29) == False

    def test_escaped_quotes(self):
        """Deve lidar com escapes corretamente."""
        p = Preprocessor(".ts")
        code = "const x = 'hello\\'world';"
        # Posição 17 é dentro da string (após escape)
        assert p.is_inside_string(code, 17) == True


class TestExplosion:
    """Testa explosão de código em separadores."""

    def test_simple_function(self):
        """Deve explodir função simples."""
        p = Preprocessor(".ts")
        code = "function foo() { return 42; }"
        exploded, positions = p.explode(code)

        # Deve conter marcadores
        assert "§§CSDIFF" in exploded
        # Deve ter mais linhas que o original
        assert exploded.count("\n") > code.count("\n")

    def test_preserves_strings(self):
        """Não deve quebrar dentro de strings."""
        p = Preprocessor(".ts")
        code = "const x = 'hello; world';"
        exploded, _ = p.explode(code)

        # String deve permanecer intacta
        assert "'hello; world'" in exploded or "hello; world" in exploded

    def test_nested_braces(self):
        """Deve lidar com aninhamento de chaves."""
        p = Preprocessor(".ts")
        code = "if (x) { if (y) { z(); } }"
        exploded, _ = p.explode(code)

        # Deve ter marcadores com diferentes profundidades
        assert "§§CSDIFF_0" in exploded or "§§CSDIFF_1" in exploded

    def test_jsx_tags(self):
        """Deve explodir tags JSX (apenas em .tsx)."""
        p = Preprocessor(".tsx")
        code = "<div className='test'>Hello</div>"
        exploded, _ = p.explode(code)

        # Deve quebrar em tags
        assert "§§CSDIFF" in exploded


class TestSeparatorCounting:
    """Testa contagem de separadores."""

    def test_count_separators(self):
        """Deve contar separadores corretamente."""
        p = Preprocessor(".ts")
        code = "function foo() { return 42; }"
        counts = p.count_separators(code)

        assert counts["{"] == 1
        assert counts["}"] == 1
        assert counts["("] == 1
        assert counts[")"] == 1
        assert counts[";"] == 1

    def test_ignores_strings(self):
        """Não deve contar separadores dentro de strings."""
        p = Preprocessor(".ts")
        code = "const x = '{;}';"
        counts = p.count_separators(code)

        # Deve contar apenas o ";" fora da string
        assert counts[";"] == 1
        assert counts["{"] == 0  # Está dentro da string


class TestPostprocessing:
    """Testa integração com postprocessor."""

    def test_roundtrip(self):
        """Explosão + reconstrução deve preservar código."""
        from src.core.postprocessor import Postprocessor

        p = Preprocessor(".ts")
        pp = Postprocessor()

        original = "function foo() { return 42; }"
        exploded, _ = p.explode(original)
        reconstructed = pp.reconstruct(exploded)

        # Remover espaços extras para comparação
        assert reconstructed.replace(" ", "").replace("\n", "") == original.replace(" ", "")


class TestEdgeCases:
    """Testa casos de borda."""

    def test_empty_file(self):
        """Deve lidar com arquivo vazio."""
        p = Preprocessor(".ts")
        exploded, positions = p.explode("")
        assert exploded == ""
        assert positions == []

    def test_only_strings(self):
        """Deve lidar com arquivo que é só strings."""
        p = Preprocessor(".ts")
        code = "'hello world'"
        exploded, _ = p.explode(code)
        # Não deve ter marcadores
        assert "§§CSDIFF" not in exploded

    def test_multiline_code(self):
        """Deve lidar com código já multi-linha."""
        p = Preprocessor(".ts")
        code = """function foo() {
    return 42;
}"""
        exploded, _ = p.explode(code)
        assert "§§CSDIFF" in exploded


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
