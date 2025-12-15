"""
Exemplo simples de uso do CSDiff-Web.
Demonstra merge de três versões de um arquivo TypeScript.
"""

import sys
from pathlib import Path

# Adicionar src/ ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.csdiff_web import CSDiffWeb


def example_basic_merge():
    """Exemplo 1: Merge sem conflitos - mudanças em locais diferentes."""
    print("=" * 60)
    print("EXEMPLO 1: Merge sem conflitos")
    print("=" * 60)

    csdiff = CSDiffWeb(".ts")

    base = """function add(a, b) {
    return a + b;
}

function subtract(a, b) {
    return a - b;
}"""

    left = """function add(a, b) {
    console.log('Adding:', a, b);
    return a + b;
}

function subtract(a, b) {
    return a - b;
}"""

    right = """function add(a, b) {
    return a + b;
}

function subtract(a, b) {
    console.log('Subtracting:', a, b);
    return a - b;
}"""

    print("\nVERSÃO BASE:")
    print(base)
    print("\nVERSÃO LEFT (adiciona log em add):")
    print(left)
    print("\nVERSÃO RIGHT (adiciona log em subtract):")
    print(right)

    result, has_conflict, num_conflicts = csdiff.merge(base, left, right)

    print("\n" + "=" * 60)
    print("RESULTADO DO MERGE:")
    print("=" * 60)
    print(result)
    print(f"\nConflitos: {num_conflicts}")
    print(f"Status: {'❌ COM CONFLITOS' if has_conflict else '✅ SEM CONFLITOS'}")


def example_conflicting_merge():
    """Exemplo 2: Merge com conflitos - ambos lados mudam a mesma função."""
    print("\n\n" + "=" * 60)
    print("EXEMPLO 2: Merge com conflitos")
    print("=" * 60)

    csdiff = CSDiffWeb(".ts")

    base = """function calculate(x) {
    return x * 2;
}"""

    left = """function calculate(x) {
    return x * 3;  // Left mudou multiplicador
}"""

    right = """function calculate(x) {
    return x * 5;  // Right mudou multiplicador
}"""

    print("\nVERSÃO BASE:")
    print(base)
    print("\nVERSÃO LEFT (multiplica por 3):")
    print(left)
    print("\nVERSÃO RIGHT (multiplica por 5):")
    print(right)

    result, has_conflict, num_conflicts = csdiff.merge(base, left, right)

    print("\n" + "=" * 60)
    print("RESULTADO DO MERGE:")
    print("=" * 60)
    print(result)
    print(f"\nConflitos: {num_conflicts}")
    print(f"Status: {'❌ COM CONFLITOS' if has_conflict else '✅ SEM CONFLITOS'}")


def example_jsx_merge():
    """Exemplo 3: Merge de componente JSX."""
    print("\n\n" + "=" * 60)
    print("EXEMPLO 3: Merge de JSX/TSX")
    print("=" * 60)

    csdiff = CSDiffWeb(".tsx")

    base = """function Button() {
    return <button>Click me</button>;
}"""

    left = """function Button() {
    return <button className="btn">Click me</button>;
}"""

    right = """function Button() {
    return <button onClick={handleClick}>Click me</button>;
}"""

    print("\nVERSÃO BASE:")
    print(base)
    print("\nVERSÃO LEFT (adiciona className):")
    print(left)
    print("\nVERSÃO RIGHT (adiciona onClick):")
    print(right)

    result, has_conflict, num_conflicts = csdiff.merge(base, left, right)

    print("\n" + "=" * 60)
    print("RESULTADO DO MERGE:")
    print("=" * 60)
    print(result)
    print(f"\nConflitos: {num_conflicts}")
    print(f"Status: {'❌ COM CONFLITOS' if has_conflict else '✅ SEM CONFLITOS'}")


def example_statistics():
    """Exemplo 4: Estatísticas de explosão."""
    print("\n\n" + "=" * 60)
    print("EXEMPLO 4: Estatísticas de Explosão")
    print("=" * 60)

    csdiff = CSDiffWeb(".ts")

    code = """function fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}"""

    stats = csdiff.get_statistics(code, code, code)

    print("\nCÓDIGO:")
    print(code)
    print("\nESTATÍSTICAS:")
    print(f"  Linhas originais: {stats['base_lines']}")
    print(f"  Linhas após explosão: {stats['base_exploded_lines']}")
    print(f"  Razão de explosão: {stats['explosion_ratio']:.2f}x")
    print(f"  Extensão: {stats['extension']}")
    print(f"\n  Separadores detectados:")
    for sep, count in stats['separator_count'].items():
        if count > 0:
            print(f"    '{sep}': {count}")


if __name__ == "__main__":
    example_basic_merge()
    example_conflicting_merge()
    example_jsx_merge()
    example_statistics()

    print("\n\n" + "=" * 60)
    print("Exemplos concluídos!")
    print("=" * 60)
