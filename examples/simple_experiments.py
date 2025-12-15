"""
Exemplo simples de uso do Runner.
Cria triplas sintéticas e executa experimentos.
"""

import sys
from pathlib import Path
import tempfile
import shutil

# Adicionar src/ ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.runner.experiment_runner import ExperimentRunner


def create_synthetic_triplets(output_dir: Path, num_triplets: int = 3):
    """
    Cria triplas sintéticas para teste.

    Args:
        output_dir: Diretório onde criar triplas
        num_triplets: Número de triplas a criar
    """
    print(f"Criando {num_triplets} triplas sintéticas em {output_dir}...")

    # Tripla 1: Sem conflito - mudanças em locais diferentes
    triplet_1 = output_dir / "triplet_001"
    triplet_1.mkdir(parents=True, exist_ok=True)

    (triplet_1 / "base.ts").write_text("""function add(a, b) {
    return a + b;
}

function subtract(a, b) {
    return a - b;
}""")

    (triplet_1 / "left.ts").write_text("""function add(a, b) {
    console.log('Adding');
    return a + b;
}

function subtract(a, b) {
    return a - b;
}""")

    (triplet_1 / "right.ts").write_text("""function add(a, b) {
    return a + b;
}

function subtract(a, b) {
    console.log('Subtracting');
    return a - b;
}""")

    (triplet_1 / "metadata.txt").write_text("""Triplet ID: 1
Original File: src/math.ts
Extension: .ts
Commit SHA: synthetic001
""")

    # Tripla 2: Com conflito - mudanças no mesmo local
    triplet_2 = output_dir / "triplet_002"
    triplet_2.mkdir(parents=True, exist_ok=True)

    (triplet_2 / "base.ts").write_text("""function calculate(x) {
    return x * 2;
}""")

    (triplet_2 / "left.ts").write_text("""function calculate(x) {
    return x * 3;
}""")

    (triplet_2 / "right.ts").write_text("""function calculate(x) {
    return x * 5;
}""")

    (triplet_2 / "metadata.txt").write_text("""Triplet ID: 2
Original File: src/calc.ts
Extension: .ts
Commit SHA: synthetic002
""")

    # Tripla 3: JSX - sem conflito
    triplet_3 = output_dir / "triplet_003"
    triplet_3.mkdir(parents=True, exist_ok=True)

    (triplet_3 / "base.tsx").write_text("""function Button() {
    return <button>Click</button>;
}""")

    (triplet_3 / "left.tsx").write_text("""function Button() {
    return <button className="btn">Click</button>;
}""")

    (triplet_3 / "right.tsx").write_text("""function Button() {
    return <button onClick={handleClick}>Click</button>;
}""")

    (triplet_3 / "metadata.txt").write_text("""Triplet ID: 3
Original File: src/Button.tsx
Extension: .tsx
Commit SHA: synthetic003
""")

    print(f"✓ {num_triplets} triplas criadas")


def run_example():
    """Executa exemplo de experimentos."""
    print("=" * 60)
    print("EXEMPLO: Runner de Experimentos")
    print("=" * 60)

    # Criar diretórios temporários
    tmpdir = tempfile.mkdtemp()

    try:
        triplets_dir = Path(tmpdir) / "triplets"
        results_dir = Path(tmpdir) / "results"

        print(f"\nDiretórios temporários:")
        print(f"  Triplas:    {triplets_dir}")
        print(f"  Resultados: {results_dir}")

        # Criar triplas sintéticas
        create_synthetic_triplets(triplets_dir, num_triplets=3)

        # Criar runner
        print("\nInicializando runner...")
        runner = ExperimentRunner(
            triplets_dir=triplets_dir,
            results_dir=results_dir,
            timeout=30
        )

        # Executar experimentos
        print("\nExecutando experimentos...")
        results = runner.run_experiments(
            tools=['csdiff-web', 'diff3', 'slow-diff3']
        )

        # Exibir resultados
        print("\n" + "=" * 60)
        print("RESULTADOS")
        print("=" * 60)
        print(f"Triplas processadas: {results['triplets_processed']}")
        print(f"\nRelatórios gerados:")
        print(f"  CSV:    {results['csv_path']}")
        print(f"  Resumo: {results['summary_path']}")

        # Exibir métricas
        print("\nMÉTRICAS:")
        for tool, metrics in results['metrics'].items():
            print(f"\n{tool.upper()}:")
            print(f"  Execuções:   {metrics['successful_executions']}/{metrics['total_executions']}")
            print(f"  Conflitos:   {metrics['total_conflicts']} total, {metrics['avg_conflicts']:.2f} média")
            print(f"  Tempo:       {metrics['avg_time']:.3f}s média")

        # Comparação
        if 'csdiff-web' in results['metrics'] and 'diff3' in results['metrics']:
            csdiff_conflicts = results['metrics']['csdiff-web']['total_conflicts']
            diff3_conflicts = results['metrics']['diff3']['total_conflicts']

            print("\n" + "=" * 60)
            print("COMPARAÇÃO: CSDiff-Web vs diff3")
            print("=" * 60)
            print(f"diff3:      {diff3_conflicts} conflitos")
            print(f"CSDiff-Web: {csdiff_conflicts} conflitos")

            if diff3_conflicts > 0:
                reduction = diff3_conflicts - csdiff_conflicts
                reduction_pct = (reduction / diff3_conflicts * 100)
                print(f"Redução:    {reduction} conflitos ({reduction_pct:.1f}%)")

        # Mostrar conteúdo do resumo
        print("\n" + "=" * 60)
        print("RESUMO COMPLETO:")
        print("=" * 60)
        if results['summary_path']:
            print(results['summary_path'].read_text())

        # Mostrar CSV
        print("\n" + "=" * 60)
        print("CSV (primeiras linhas):")
        print("=" * 60)
        if results['csv_path']:
            lines = results['csv_path'].read_text().split('\n')
            for line in lines[:10]:  # Primeiras 10 linhas
                print(line)

    finally:
        # Limpar diretórios temporários
        print(f"\nLimpando diretórios temporários...")
        shutil.rmtree(tmpdir)
        print("✓ Limpeza concluída")


if __name__ == '__main__':
    run_example()
