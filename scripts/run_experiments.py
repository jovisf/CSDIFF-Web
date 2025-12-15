#!/usr/bin/env python3
"""
Script principal para executar experimentos.
Executa CSDiff-Web + diff3 + slow-diff3 em triplas mineradas.

Uso:
    python3 scripts/run_experiments.py
    python3 scripts/run_experiments.py --max-triplets 50
    python3 scripts/run_experiments.py --tools csdiff-web diff3
"""

import sys
import argparse
import logging
from pathlib import Path

# Adicionar src/ ao PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.runner.experiment_runner import ExperimentRunner


def setup_logging(verbose: bool = False):
    """Configura logging."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def main():
    parser = argparse.ArgumentParser(
        description='Executa experimentos com CSDiff-Web, diff3 e slow-diff3'
    )
    parser.add_argument(
        '--triplets-dir',
        type=Path,
        default=Path('data/triplets'),
        help='Diretório com triplas mineradas (padrão: data/triplets)'
    )
    parser.add_argument(
        '--results-dir',
        type=Path,
        default=Path('data/results'),
        help='Diretório para salvar resultados (padrão: data/results)'
    )
    parser.add_argument(
        '--max-triplets',
        type=int,
        default=None,
        help='Número máximo de triplas a processar (padrão: todas)'
    )
    parser.add_argument(
        '--tools',
        nargs='+',
        choices=['csdiff-web', 'diff3', 'slow-diff3'],
        default=['csdiff-web', 'diff3', 'slow-diff3'],
        help='Ferramentas a executar (padrão: todas)'
    )
    parser.add_argument(
        '--timeout',
        type=int,
        default=60,
        help='Timeout por execução em segundos (padrão: 60)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Modo verboso (DEBUG)'
    )

    args = parser.parse_args()

    # Setup
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)

    # Verificar se diretório de triplas existe
    if not args.triplets_dir.exists():
        logger.error(f"Diretório de triplas não encontrado: {args.triplets_dir}")
        logger.error("Execute primeiro: python3 scripts/mine_repositories.py")
        return 1

    # Contar triplas disponíveis
    triplet_count = len(list(args.triplets_dir.glob("triplet_*")))
    if triplet_count == 0:
        logger.error(f"Nenhuma tripla encontrada em {args.triplets_dir}")
        logger.error("Execute primeiro: python3 scripts/mine_repositories.py")
        return 1

    logger.info(f"Triplas disponíveis: {triplet_count}")
    if args.max_triplets:
        logger.info(f"Processando apenas: {args.max_triplets}")

    # Criar runner
    logger.info("Inicializando runner...")
    runner = ExperimentRunner(
        triplets_dir=args.triplets_dir,
        results_dir=args.results_dir,
        timeout=args.timeout
    )

    # Executar experimentos
    try:
        print("\n" + "=" * 60)
        print("EXECUTANDO EXPERIMENTOS")
        print("=" * 60)
        print(f"Triplas: {triplet_count}")
        print(f"Ferramentas: {', '.join(args.tools)}")
        print(f"Timeout: {args.timeout}s")
        print(f"Resultados: {args.results_dir}")
        print("=" * 60 + "\n")

        results = runner.run_experiments(
            max_triplets=args.max_triplets,
            tools=args.tools
        )

        # Exibir resultados
        print("\n" + "=" * 60)
        print("EXPERIMENTOS CONCLUÍDOS")
        print("=" * 60)
        print(f"Triplas processadas: {results['triplets_processed']}")
        print(f"\nRelatórios gerados:")
        print(f"  CSV:    {results['csv_path']}")
        print(f"  Resumo: {results['summary_path']}")
        print("=" * 60)

        # Exibir métricas resumidas
        print("\nMÉTRICAS RESUMIDAS:")
        print("-" * 60)

        for tool, metrics in results['metrics'].items():
            print(f"\n{tool.upper()}:")
            print(f"  Execuções bem-sucedidas: {metrics['successful_executions']}/{metrics['total_executions']}")
            print(f"  Taxa de sucesso:         {metrics['success_rate']:.1f}%")
            print(f"  Total de conflitos:      {metrics['total_conflicts']}")
            print(f"  Média de conflitos:      {metrics['avg_conflicts']:.2f}")
            print(f"  Tempo médio:             {metrics['avg_time']:.3f}s")

        # Comparação CSDiff-Web vs diff3
        if 'csdiff-web' in results['metrics'] and 'diff3' in results['metrics']:
            csdiff_conflicts = results['metrics']['csdiff-web']['total_conflicts']
            diff3_conflicts = results['metrics']['diff3']['total_conflicts']

            if diff3_conflicts > 0:
                reduction = diff3_conflicts - csdiff_conflicts
                reduction_pct = (reduction / diff3_conflicts * 100)

                print("\n" + "=" * 60)
                print("COMPARAÇÃO: CSDiff-Web vs diff3")
                print("=" * 60)
                print(f"diff3:      {diff3_conflicts} conflitos")
                print(f"CSDiff-Web: {csdiff_conflicts} conflitos")
                print(f"Redução:    {reduction} conflitos ({reduction_pct:.1f}%)")
                print("=" * 60)

        # Estatísticas detalhadas
        runner.print_statistics()

        print(f"\n✅ Para ver resultados completos:")
        print(f"   cat {results['summary_path']}")
        print(f"   cat {results['csv_path']}")

        return 0

    except KeyboardInterrupt:
        logger.warning("\n⚠ Experimentos interrompidos pelo usuário")
        return 130

    except Exception as e:
        logger.error(f"\n❌ Erro durante experimentos: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
