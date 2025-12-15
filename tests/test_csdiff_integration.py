"""
Testes de integração end-to-end do CSDiff-Web.
Valida o pipeline completo: filtro → explosão → diff3 → reconstrução
"""

import pytest
from src.core.csdiff_web import CSDiffWeb


class TestBasicMerge:
    """Testa merges básicos sem conflitos."""

    def test_no_conflict_one_side_change(self):
        """Merge sem conflito: apenas um lado muda."""
        csdiff = CSDiffWeb(".ts", skip_filter=True)

        base = "function foo() { return 1; }"
        left = "function foo() { return 2; }"
        right = "function foo() { return 1; }"  # Sem mudança

        result, has_conflict, num_conflicts = csdiff.merge(base, left, right)

        assert has_conflict == False
        assert num_conflicts == 0
        assert "return 2" in result

    def test_no_conflict_different_locations(self):
        """Merge sem conflito: mudanças em locais diferentes."""
        csdiff = CSDiffWeb(".ts", skip_filter=True)

        base = """function foo() { return 1; }
function bar() { return 2; }"""

        left = """function foo() { return 10; }
function bar() { return 2; }"""

        right = """function foo() { return 1; }
function bar() { return 20; }"""

        result, has_conflict, num_conflicts = csdiff.merge(base, left, right)

        assert has_conflict == False
        assert num_conflicts == 0
        assert "return 10" in result
        assert "return 20" in result


class TestConflictingMerge:
    """Testa merges com conflitos."""

    def test_conflict_same_line(self):
        """Merge com conflito: ambos mudam mesma linha."""
        csdiff = CSDiffWeb(".ts", skip_filter=True)

        base = "function foo() { return 1; }"
        left = "function foo() { return 2; }"
        right = "function foo() { return 3; }"

        result, has_conflict, num_conflicts = csdiff.merge(base, left, right)

        assert has_conflict == True
        assert num_conflicts >= 1
        assert "<<<<<<<" in result
        assert ">>>>>>>" in result


class TestFileFiltering:
    """Testa filtro de arquivos minificados."""

    def test_minified_detection(self):
        """Deve detectar arquivo minificado e usar fallback."""
        csdiff = CSDiffWeb(".ts", skip_filter=False)

        # Arquivo minificado (linha muito longa)
        minified = "const x=1,y=2,z=3,a=4,b=5,c=6;" * 50

        result, _, _ = csdiff.merge(minified, minified, minified)

        # Deve executar sem erro (usando fallback)
        assert result is not None

    def test_normal_file_processing(self):
        """Arquivo normal deve ser processado com separadores."""
        csdiff = CSDiffWeb(".ts", skip_filter=False)

        base = "function foo() { return 1; }"
        stats = csdiff.get_statistics(base, base, base)

        # Deve ter explosão
        assert stats['explosion_ratio'] > 1.0


class TestJSXSupport:
    """Testa suporte a JSX/TSX."""

    def test_jsx_tags(self):
        """Deve processar tags JSX corretamente."""
        csdiff = CSDiffWeb(".tsx", skip_filter=True)

        base = "<div>Hello</div>"
        left = "<div>Hello World</div>"
        right = "<div>Hello</div>"

        result, has_conflict, _ = csdiff.merge(base, left, right)

        assert has_conflict == False
        assert "Hello World" in result

    def test_jsx_attributes(self):
        """Deve lidar com atributos JSX."""
        csdiff = CSDiffWeb(".tsx", skip_filter=True)

        base = '<div className="old">Text</div>'
        left = '<div className="new">Text</div>'
        right = '<div className="old">Text</div>'

        result, has_conflict, _ = csdiff.merge(base, left, right)

        assert has_conflict == False
        assert 'className="new"' in result or "className='new'" in result or 'new' in result


class TestStatistics:
    """Testa coleta de estatísticas."""

    def test_explosion_ratio(self):
        """Deve calcular razão de explosão."""
        csdiff = CSDiffWeb(".ts", skip_filter=True)

        base = "function foo() { return 1; }"
        stats = csdiff.get_statistics(base, base, base)

        assert 'explosion_ratio' in stats
        assert stats['explosion_ratio'] > 1.0  # Deve ter mais linhas após explosão

    def test_separator_count(self):
        """Deve contar separadores."""
        csdiff = CSDiffWeb(".ts", skip_filter=True)

        base = "function foo() { return 1; }"
        stats = csdiff.get_statistics(base, base, base)

        assert 'separator_count' in stats
        assert stats['separator_count']['{'] == 1
        assert stats['separator_count']['}'] == 1


class TestRealWorldScenarios:
    """Testes com cenários realistas."""

    def test_function_addition(self):
        """Cenário: adicionar nova função em ambos os lados."""
        csdiff = CSDiffWeb(".ts", skip_filter=True)

        base = """function existing() {
    return 1;
}"""

        left = """function existing() {
    return 1;
}

function newLeft() {
    return 2;
}"""

        right = """function existing() {
    return 1;
}

function newRight() {
    return 3;
}"""

        result, has_conflict, _ = csdiff.merge(base, left, right)

        # Ambas funções devem estar presentes
        assert "newLeft" in result
        assert "newRight" in result

    def test_import_addition(self):
        """Cenário: adicionar imports diferentes."""
        csdiff = CSDiffWeb(".ts", skip_filter=True)

        base = "const x = 1;"

        left = """import { foo } from 'lib';
const x = 1;"""

        right = """import { bar } from 'lib';
const x = 1;"""

        result, has_conflict, _ = csdiff.merge(base, left, right)

        # Ambos imports devem estar presentes
        assert "foo" in result
        assert "bar" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
