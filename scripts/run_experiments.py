#!/usr/bin/env python3
"""
Script principal para executar experimentos.
Executa CSDiff-Web + mergiraf + slow-diff3 em triplas mineradas.
"""

import sys
import argparse
import logging
from pathlib import Path

# Adicionar a raiz do projeto ao PYTHONPATH para permitir imports de 'src'
# Garante que o caminho seja absoluto para evitar erros
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

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
        description='Executa experimentos com CSDiff-Web, mergiraf e slow-diff3'
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

    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)

    if not args.triplets_dir.exists():
        logger.error(f"Diretório de triplas não encontrado: {args.triplets_dir}")
        return 1

    triplet_count = len(list(args.triplets_dir.glob("triplet_*")))
    
    logger.info("Inicializando runner...")
    runner = ExperimentRunner(
        triplets_dir=args.triplets_dir,
        results_dir=args.results_dir,
        timeout=args.timeout
    )

    try:
        print("\n" + "=" * 60)
        print("EXECUTANDO EXPERIMENTOS")
        print("=" * 60)
        print(f"Triplas:     {triplet_count}")
        print(f"Ferramentas: CSDiff-Web, Mergiraf, Slow-diff3")
        print("=" * 60 + "\n")

        results = runner.run_experiments(
            max_triplets=args.max_triplets
        )

        print("\n" + "=" * 60)
        print("MÉTRICAS RESUMIDAS")
        print("=" * 60)
        
        if results.get('metrics'):
            for tool, metrics in results['metrics'].items():
                print(f"\n{tool.upper()}:")
                print(f"  Sucesso: {metrics['success_rate']:.1f}%")
                print(f"  Média de Conflitos: {metrics['avg_conflicts']:.2f}")
        
        return 0

    except KeyboardInterrupt:
        print("\n⚠ Interrompido pelo usuário")
        return 130
    except Exception as e:
        logger.error(f"Erro fatal: {e}", exc_info=True)
        return 1

if __name__ == '__main__':
    sys.exit(main())