#!/usr/bin/env python3
"""
Script principal de mineração de repositórios.
Carrega configuração do YAML e executa mineração completa.

Uso:
    python3 scripts/mine_repositories.py --language typescript --max-triplets 100
    python3 scripts/mine_repositories.py --all --max-triplets 500
"""

import sys
import argparse
import yaml
import logging
from pathlib import Path

# Adicionar src/ ao PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.miner.github_miner import GitHubMiner


def setup_logging(verbose: bool = False):
    """Configura logging."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def load_config(config_path: Path) -> dict:
    """Carrega configuração do YAML."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def main():
    parser = argparse.ArgumentParser(
        description='Minera merge commits de repositórios GitHub'
    )
    parser.add_argument(
        '--language',
        choices=['typescript', 'tsx', 'javascript', 'jsx', 'mixed', 'all'],
        default='all',
        help='Categoria de linguagem a minerar'
    )
    parser.add_argument(
        '--max-triplets',
        type=int,
        default=100,
        help='Número máximo de triplas a extrair (padrão: 100)'
    )
    parser.add_argument(
        '--max-repos',
        type=int,
        default=None,
        help='Número máximo de repositórios a processar (padrão: todos)'
    )
    parser.add_argument(
        '--config',
        type=Path,
        default=Path('config/repositories.yaml'),
        help='Caminho para arquivo de configuração YAML'
    )
    parser.add_argument(
        '--repos-dir',
        type=Path,
        default=Path('data/repos'),
        help='Diretório para clonar repositórios'
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path('data/triplets'),
        help='Diretório para salvar triplas'
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

    # Carregar configuração
    logger.info(f"Carregando configuração de: {args.config}")
    config = load_config(args.config)

    # Selecionar repositórios
    if args.language == 'all':
        # Minerar todas as categorias
        repo_list = []
        for category in ['typescript', 'tsx', 'javascript', 'jsx', 'mixed']:
            if category in config:
                repo_list.extend(config[category])
    else:
        # Minerar categoria específica
        if args.language not in config:
            logger.error(f"Categoria '{args.language}' não encontrada no config")
            return 1
        repo_list = config[args.language]

    # Limitar número de repos se especificado
    if args.max_repos:
        repo_list = repo_list[:args.max_repos]

    logger.info(f"Selecionados {len(repo_list)} repositórios para mineração")
    logger.info(f"Meta: {args.max_triplets} triplas")

    # Criar minerador
    miner = GitHubMiner(
        repos_dir=args.repos_dir,
        triplets_dir=args.output_dir,
        target_triplets=args.max_triplets
        #target_triplets=10 # Para forçar a olhar outros repositórios durante testes --max-repos: 5 --max-triplets: 50
    )

    # Executar mineração
    try:
        triplets = miner.mine_repositories(
            repo_list=repo_list,
            max_triplets=args.max_triplets
        )

        logger.info(f"\n✓ Mineração concluída!")
        logger.info(f"Total de triplas: {len(triplets)}")
        logger.info(f"Triplas salvas em: {args.output_dir}")

        return 0

    except KeyboardInterrupt:
        logger.warning("\n⚠ Mineração interrompida pelo usuário")
        return 130

    except Exception as e:
        logger.error(f"\n❌ Erro durante mineração: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
