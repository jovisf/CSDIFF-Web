#!/usr/bin/env python3
"""
Script de análise de resultados.
Analisa CSV gerado pelo Runner e gera relatórios científicos.

Uso:
    python3 scripts/analyze_results.py data/results/results_*.csv
    python3 scripts/analyze_results.py data/results/results_*.csv --output reports/
"""

import sys
import argparse
from pathlib import Path

# Adicionar src/ ao PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.analyzer.metrics_analyzer import MetricsAnalyzer
from src.analyzer.report_generator import ReportGenerator


def main():
    parser = argparse.ArgumentParser(
        description='Analisa resultados de experimentos do CSDiff-Web'
    )
    parser.add_argument(
        'csv_file',
        type=Path,
        help='Arquivo CSV com resultados (gerado pelo Runner)'
    )
    parser.add_argument(
        '--output', '-o',
        type=Path,
        default=Path('data/reports'),
        help='Diretório para salvar relatórios (padrão: data/reports)'
    )

    args = parser.parse_args()

    # Verificar se CSV existe
    if not args.csv_file.exists():
        print(f"❌ Arquivo CSV não encontrado: {args.csv_file}")
        print("\nExecute primeiro:")
        print("  python3 scripts/run_experiments.py")
        return 1

    print("=" * 60)
    print("ANÁLISE DE RESULTADOS - CSDiff-Web")
    print("=" * 60)
    print(f"CSV:    {args.csv_file}")
    print(f"Output: {args.output}")
    print("=" * 60)

    # Criar analisador
    print("\nCarregando dados...")
    analyzer = MetricsAnalyzer(args.csv_file)

    # Gerar análise
    print("Calculando métricas...")
    summary = analyzer.generate_summary_report()

    # Imprimir resumo no console
    analyzer.print_summary()

    # Gerar relatórios
    print("Gerando relatórios...")
    generator = ReportGenerator(args.output)

    md_report = generator.generate_markdown_report(summary)
    latex_table = generator.generate_latex_table(summary)

    # Resultados
    print("\n" + "=" * 60)
    print("RELATÓRIOS GERADOS")
    print("=" * 60)
    print(f"Markdown: {md_report}")
    print(f"LaTeX:    {latex_table}")
    print("=" * 60)

    print("\n✅ Análise concluída!")
    print(f"\nPara ver o relatório:")
    print(f"  cat {md_report}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
