"""
Exemplo simples de uso do Analyzer.
Demonstra análise estatística de resultados de experimentos.
"""

import sys
from pathlib import Path
import tempfile
import shutil

# Adicionar src/ ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.runner.experiment_runner import ExperimentRunner
from src.analyzer.metrics_analyzer import MetricsAnalyzer
from src.analyzer.report_generator import ReportGenerator


def create_synthetic_triplets(output_dir: Path):
    """
    Cria triplas sintéticas com diferentes cenários.
    """
    print(f"Criando triplas sintéticas em {output_dir}...")

    # Tripla 1: Sem conflito - CSDiff-Web resolve, diff3 também
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

    # Tripla 2: Conflito - CSDiff-Web resolve, diff3 conflita (FP para CSDiff-Web)
    triplet_2 = output_dir / "triplet_002"
    triplet_2.mkdir(parents=True, exist_ok=True)

    (triplet_2 / "base.ts").write_text("""function calculate(x) {
    const result = x * 2;
    return result;
}""")

    (triplet_2 / "left.ts").write_text("""function calculate(x) {
    const result = x * 3;
    console.log('Left change');
    return result;
}""")

    (triplet_2 / "right.ts").write_text("""function calculate(x) {
    const result = x * 5;
    console.log('Right change');
    return result;
}""")

    (triplet_2 / "metadata.txt").write_text("""Triplet ID: 2
Original File: src/calc.ts
Extension: .ts
Commit SHA: synthetic002
""")

    # Tripla 3: Sem conflito - mudança em locais diferentes
    triplet_3 = output_dir / "triplet_003"
    triplet_3.mkdir(parents=True, exist_ok=True)

    (triplet_3 / "base.tsx").write_text("""function Button() {
    return <button>Click</button>;
}

function Header() {
    return <h1>Title</h1>;
}""")

    (triplet_3 / "left.tsx").write_text("""function Button() {
    return <button className="btn">Click</button>;
}

function Header() {
    return <h1>Title</h1>;
}""")

    (triplet_3 / "right.tsx").write_text("""function Button() {
    return <button>Click</button>;
}

function Header() {
    return <h1 className="header">Title</h1>;
}""")

    (triplet_3 / "metadata.txt").write_text("""Triplet ID: 3
Original File: src/Button.tsx
Extension: .tsx
Commit SHA: synthetic003
""")

    # Tripla 4: Conflito real - ambas ferramentas devem conflitar
    triplet_4 = output_dir / "triplet_004"
    triplet_4.mkdir(parents=True, exist_ok=True)

    (triplet_4 / "base.ts").write_text("""const config = {
    timeout: 1000
};""")

    (triplet_4 / "left.ts").write_text("""const config = {
    timeout: 2000
};""")

    (triplet_4 / "right.ts").write_text("""const config = {
    timeout: 3000
};""")

    (triplet_4 / "metadata.txt").write_text("""Triplet ID: 4
Original File: src/config.ts
Extension: .ts
Commit SHA: synthetic004
""")

    print(f"✓ 4 triplas criadas")


def run_analysis_example():
    """Executa exemplo completo de análise."""
    print("=" * 60)
    print("EXEMPLO: Análise de Resultados")
    print("=" * 60)

    # Criar diretórios temporários
    tmpdir = tempfile.mkdtemp()

    try:
        triplets_dir = Path(tmpdir) / "triplets"
        results_dir = Path(tmpdir) / "results"
        reports_dir = Path(tmpdir) / "reports"

        print(f"\nDiretórios temporários:")
        print(f"  Triplas:    {triplets_dir}")
        print(f"  Resultados: {results_dir}")
        print(f"  Relatórios: {reports_dir}")

        # FASE 1: Criar triplas e executar experimentos
        print("\n" + "=" * 60)
        print("FASE 1: Executando Experimentos")
        print("=" * 60)

        create_synthetic_triplets(triplets_dir)

        runner = ExperimentRunner(
            triplets_dir=triplets_dir,
            results_dir=results_dir,
            timeout=30
        )

        results = runner.run_experiments(
        )

        print(f"\n✓ Experimentos concluídos")
        print(f"  Triplas processadas: {results['triplets_processed']}")
        print(f"  CSV gerado: {results['csv_path']}")

        # FASE 2: Analisar resultados
        print("\n" + "=" * 60)
        print("FASE 2: Análise Estatística")
        print("=" * 60)

        # Criar analisador
        analyzer = MetricsAnalyzer(results['csv_path'])

        # Gerar análise
        print("\nCalculando métricas...")
        summary = analyzer.generate_summary_report()

        # Imprimir resumo
        analyzer.print_summary()

        # FASE 3: Gerar relatórios
        print("\n" + "=" * 60)
        print("FASE 3: Gerando Relatórios")
        print("=" * 60)

        reports_dir.mkdir(parents=True, exist_ok=True)
        generator = ReportGenerator(reports_dir)

        md_report = generator.generate_markdown_report(summary)
        latex_table = generator.generate_latex_table(summary)

        print(f"\nRelatórios gerados:")
        print(f"  Markdown: {md_report}")
        print(f"  LaTeX:    {latex_table}")

        # FASE 4: Exibir relatório Markdown
        print("\n" + "=" * 60)
        print("RELATÓRIO MARKDOWN GERADO")
        print("=" * 60)
        print(md_report.read_text(encoding='utf-8'))

        # FASE 5: Exibir tabela LaTeX
        print("\n" + "=" * 60)
        print("TABELA LATEX GERADA")
        print("=" * 60)
        print(latex_table.read_text(encoding='utf-8'))

        # FASE 6: Análise detalhada
        print("\n" + "=" * 60)
        print("ANÁLISE DETALHADA")
        print("=" * 60)

        # Métricas de conflito
        conflict_comparison = summary['conflict_comparison']
        print("\nComparação de Conflitos:")
        print(f"  diff3:      {conflict_comparison['diff3']['with_conflict']} conflitos")
        print(f"  CSDiff-Web: {conflict_comparison['csdiff-web']['with_conflict']} conflitos")
        print(f"  Redução:    {conflict_comparison['reduction']['absolute']} ({conflict_comparison['reduction']['relative']:.1f}%)")

        # FP/FN
        fp_fn = summary['fp_fn_analysis']['csdiff-web']
        print(f"\nAnálise FP/FN (usando diff3 como baseline):")
        print(f"  True Positives:  {fp_fn['TP']}")
        print(f"  False Positives: {fp_fn['FP']}")
        print(f"  True Negatives:  {fp_fn['TN']}")
        print(f"  False Negatives: {fp_fn['FN']}")
        print(f"  Precisão:        {fp_fn['precision']:.2%}")
        print(f"  Recall:          {fp_fn['recall']:.2%}")
        print(f"  F1-Score:        {fp_fn['f1_score']:.2%}")
        print(f"  Acurácia:        {fp_fn['accuracy']:.2%}")

        # Tempo
        time_stats = summary['execution_time']
        print(f"\nComparação de Tempo:")
        print(f"  diff3:      {time_stats['diff3']['mean']:.3f}s (média)")
        print(f"  CSDiff-Web: {time_stats['csdiff-web']['mean']:.3f}s (média)")

        # Interpretação
        print("\n" + "=" * 60)
        print("INTERPRETAÇÃO DOS RESULTADOS")
        print("=" * 60)

        if conflict_comparison['reduction']['relative'] > 0:
            print(f"✓ CSDiff-Web reduziu conflitos em {conflict_comparison['reduction']['relative']:.1f}%")
        else:
            print(f"⚠ CSDiff-Web não reduziu conflitos")

        if fp_fn['precision'] >= 0.9:
            print(f"✓ Alta precisão ({fp_fn['precision']:.1%}) - poucos falsos positivos")
        else:
            print(f"⚠ Precisão moderada ({fp_fn['precision']:.1%})")

        if fp_fn['recall'] >= 0.9:
            print(f"✓ Alto recall ({fp_fn['recall']:.1%}) - poucos falsos negativos")
        else:
            print(f"⚠ Recall moderado ({fp_fn['recall']:.1%})")

        print("\n" + "=" * 60)
        print("✅ Análise concluída com sucesso!")
        print("=" * 60)

    finally:
        # Limpar diretórios temporários
        print(f"\nLimpando diretórios temporários...")
        shutil.rmtree(tmpdir)
        print("✓ Limpeza concluída")


if __name__ == '__main__':
    run_analysis_example()
