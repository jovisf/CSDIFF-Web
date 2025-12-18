#!/usr/bin/env python3
"""
Script de análise de resultados.
Analisa CSV gerado pelo Runner e gera relatórios científicos.

Este script processa os dados brutos e gera:
1. Resumo no terminal (Performance Individual e Comparações).
2. Relatório detalhado em Markdown.
3. Tabela LaTeX para inclusão em artigos/TCC.

Uso:
    python3 scripts/analyze_results.py data/results/results_*.csv
    python3 scripts/analyze_results.py data/results/results_*.csv --output reports/
"""

import sys
import argparse
from pathlib import Path

# Adicionar src/ ao PYTHONPATH para garantir importação correta
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.analyzer.metrics_analyzer import MetricsAnalyzer
from src.analyzer.report_generator import ReportGenerator


def main():
    parser = argparse.ArgumentParser(
        description='Analisa resultados experimentais (CSDiff-Web, Mergiraf, Slow-diff3)'
    )
    parser.add_argument(
        '--input', '-i',
        type=Path,
        required=True,
        dest='csv_file',
        help='Arquivo CSV com resultados (gerado pelo run_experiments.py)'
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
    print("ANÁLISE DE RESULTADOS - EXPERIMENTO DE MERGE")
    print("=" * 60)
    print(f"Input (CSV): {args.csv_file}")
    print(f"Output Dir:  {args.output}")
    print("=" * 60)

    try:
        # 1. Criar e executar analisador
        print("\n[1/3] Carregando e processando dados...")
        analyzer = MetricsAnalyzer(args.csv_file)
        
        print("[2/3] Calculando métricas e classificações...")
        summary = analyzer.generate_summary_report()

        # Imprimir resumo no console (Tabelas de texto)
        analyzer.print_summary()

        # 2. Gerar relatórios persistentes
        print("[3/3] Gerando arquivos de relatório...")
        generator = ReportGenerator(args.output)

        # Relatório Markdown (Completo)
        md_report = generator.generate_markdown_report(summary)
        
        # Tabela LaTeX (Apenas a tabela de performance individual para o TCC)
        latex_table = generator.generate_latex_table(summary)

        # Resultados finais
        print("\n" + "=" * 60)
        print("PROCESSO CONCLUÍDO")
        print("=" * 60)
        print(f"📄 Relatório Markdown: {md_report}")
        print(f"📄 Tabela LaTeX:      {latex_table}")
        print("=" * 60)

        print(f"\nPara visualizar o relatório formatado:")
        print(f"  cat {md_report}")

        return 0

    except Exception as e:
        print(f"\n❌ Erro durante a análise: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())