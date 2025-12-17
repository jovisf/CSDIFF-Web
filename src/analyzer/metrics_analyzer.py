"""
Analisador de métricas estatísticas.
Calcula análise comparativa usando merge commit como gabarito.

Este módulo implementa análise estatística para validação
científica das ferramentas (CSDiff-Web, Mergiraf, Slow-diff3).

METODOLOGIA:
1. Análise Individual (Gabarito):
   - Cada ferramenta é comparada diretamente com o merge commit (merged.ts).
   - Classificação: Sucesso (Clean Correct), Erro (Clean Incorrect), Conflito, Falha.

2. Comparação Par a Par (Relativa):
   - Compara ferramentas duas a duas (F1 vs F2).
   - Identifica Falsos Positivos/Negativos Adicionais.
"""

import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple
import logging

from .comparison_classifier import ComparisonClassifier

logger = logging.getLogger(__name__)


class MetricsAnalyzer:
    """
    Analisador de métricas estatísticas.
    """

    def __init__(self, csv_path: Path):
        """
        Inicializa analisador com resultados CSV.

        Args:
            csv_path: Path do CSV gerado pelo Runner
        """
        self.csv_path = Path(csv_path)
        self.df = None
        
        # Ferramentas a serem analisadas (nomes das colunas no CSV usam underscore)
        self.tools = ['csdiff_web', 'mergiraf', 'slow_diff3']

        # Carregar CSV
        self._load_csv()

    def _load_csv(self):
        """Carrega e valida CSV."""
        try:
            self.df = pd.read_csv(self.csv_path)
            logger.info(f"CSV carregado: {len(self.df)} linhas")

            # Validar colunas necessárias para as 3 ferramentas
            required_cols = []
            for tool in self.tools:
                required_cols.extend([
                    f'{tool}_has_conflict',
                    f'{tool}_num_conflicts',
                    f'{tool}_output'
                ])
            
            # Adicionar coluna do gabarito
            required_cols.append('repo_merged_content')

            missing = [col for col in required_cols if col not in self.df.columns]
            if missing:
                logger.warning(f"Colunas faltando no CSV: {missing}")

        except Exception as e:
            logger.error(f"Erro ao carregar CSV: {e}")
            raise

    def analyze_conflict_metrics(self) -> Dict[str, Dict]:
        """
        Analisa métricas relacionadas à quantidade de conflitos.
        """
        results = {}
        for tool in self.tools:
            conflict_num_col = f'{tool}_num_conflicts'
            if conflict_num_col in self.df.columns:
                # Filtrar apenas linhas onde a ferramenta foi executada com sucesso
                # (ou onde num_conflicts é válido)
                conflicts = self.df[conflict_num_col].dropna()
                
                if len(conflicts) > 0:
                    tool_name = tool.replace('_', '-')
                    results[tool_name] = {
                        'total_conflicts': int(conflicts.sum()),
                        'avg_conflicts': float(conflicts.mean()),
                        'max_conflicts': int(conflicts.max()),
                        'conflicts_per_file': float(conflicts.mean()) # Média por arquivo
                    }
        return results

    def analyze_conflict_distribution(self) -> Dict[str, Dict]:
        """
        Analisa a distribuição da quantidade de conflitos (0, 1, 2, 3+).
        """
        results = {}
        for tool in self.tools:
            conflict_num_col = f'{tool}_num_conflicts'
            if conflict_num_col in self.df.columns:
                counts = self.df[conflict_num_col].value_counts().sort_index()
                
                dist = {
                    '0': int(counts.get(0, 0)),
                    '1': int(counts.get(1, 0)),
                    '2': int(counts.get(2, 0)),
                    '3+': int(counts[counts.index >= 3].sum())
                }
                tool_name = tool.replace('_', '-')
                results[tool_name] = dist
        return results

    def analyze_individual_performance(self) -> Dict[str, Dict]:
        """
        Calcula a performance individual de cada ferramenta em relação ao gabarito.
        Baseado no diagrama de avaliação do TCC.

        Returns:
            Dict com estatísticas por ferramenta:
            {
                'csdiff-web': {'clean_correct': 10, 'clean_incorrect': 2, ...},
                'mergiraf': ...
            }
        """
        classifier = ComparisonClassifier()
        repo_col = 'repo_merged_content'

        # Iterar sobre cada ferramenta
        for tool in self.tools:
            output_col = f'{tool}_output'
            conflict_col = f'{tool}_has_conflict'
            error_col = f'{tool}_error'

            if output_col not in self.df.columns:
                continue

            # Iterar sobre as linhas do dataframe
            for idx, row in self.df.iterrows():
                # Tratar valores NaN/None
                output = str(row[output_col]) if pd.notna(row[output_col]) else ""
                has_conflict = bool(row[conflict_col]) if pd.notna(row[conflict_col]) else False
                repo_content = str(row[repo_col]) if pd.notna(row[repo_col]) else ""
                
                # Verificar erro de execução
                error_msg = str(row[error_col]) if error_col in self.df.columns and pd.notna(row[error_col]) else None
                if row.get(f'{tool}_success') is False:
                    error_msg = error_msg or "Execution Failed"

                # Classificar usando o classificador centralizado
                classifier.classify_tool_result(
                    tool_name=tool.replace('_', '-'), # Usar hifen para display
                    output=output,
                    has_conflict=has_conflict,
                    repo_expected=repo_content,
                    error=error_msg
                )

        return classifier.get_tool_statistics()

    def compare_all_pairs(self) -> Dict[str, Dict]:
        """
        Compara todos os pares ordenados de ferramentas (Análise Relativa).
        """
        results = {}
        classifier = ComparisonClassifier()
        repo_col = 'repo_merged_content'

        # Gerar todos os pares ordenados (F1, F2) onde F1 != F2
        for f1 in self.tools:
            for f2 in self.tools:
                if f1 == f2: continue

                pair_key = f"{f1.replace('_', '-')}_vs_{f2.replace('_', '-')}"
                
                # Colunas
                f1_out = f'{f1}_output'
                f2_out = f'{f2}_output'
                f1_conf = f'{f1}_has_conflict'
                f2_conf = f'{f2}_has_conflict'

                if f1_out not in self.df.columns or f2_out not in self.df.columns:
                    continue

                # Resetar stats do classificador para este par
                classifier.reset_statistics()

                for idx, row in self.df.iterrows():
                    classifier.classify_pair_result(
                        f1_output=str(row[f1_out]) if pd.notna(row[f1_out]) else "",
                        f2_output=str(row[f2_out]) if pd.notna(row[f2_out]) else "",
                        repo_expected=str(row[repo_col]) if pd.notna(row[repo_col]) else "",
                        f1_has_conflict=bool(row[f1_conf]),
                        f2_has_conflict=bool(row[f2_conf])
                    )
                
                # Salvar estatísticas do par (usando a propriedade interna do classificador que foi populada)
                pair_stats = classifier.pair_stats.copy()
                results[pair_key] = pair_stats

        return results

    def analyze_execution_time(self) -> Dict:
        """Analisa tempo de execução."""
        results = {}
        for tool in self.tools:
            time_col = f'{tool}_time'
            if time_col in self.df.columns:
                times = self.df[time_col].dropna()
                if len(times) > 0:
                    tool_name = tool.replace('_', '-')
                    results[tool_name] = {
                        'mean': float(times.mean()),
                        'min': float(times.min()),
                        'max': float(times.max())
                    }
        return results

    def generate_summary_report(self) -> Dict:
        """Gera relatório consolidado."""
        return {
            'dataset_info': {
                'total_triplets': len(self.df),
                'tools': [t.replace('_', '-') for t in self.tools]
            },
            'individual_performance': self.analyze_individual_performance(),
            'pairwise_comparisons': self.compare_all_pairs(),
            'execution_time': self.analyze_execution_time(),
            'conflict_metrics': self.analyze_conflict_metrics(), # NOVO
            'conflict_distribution': self.analyze_conflict_distribution() # NOVO
        }

    def print_summary(self):
        """Imprime resumo formatado no terminal."""
        summary = self.generate_summary_report()
        total = summary['dataset_info']['total_triplets']

        print("\n" + "=" * 80)
        print(f"RELATÓRIO DE EXPERIMENTOS (Total de Triplas: {total})")
        print("=" * 80)

        # 1. Tabela de Performance Individual (O que foi pedido: Comparação com Gabarito)
        print("\n1. PERFORMANCE INDIVIDUAL (Ferramenta vs Gabarito)")
        print("-" * 80)
        # Cabeçalho da tabela
        header = f"{'FERRAMENTA':<15} | {'SUCESSO (Correto)':<18} | {'ERRO (Incorreto)':<18} | {'CONFLITO':<10} | {'FALHA':<8}"
        print(header)
        print("-" * 80)

        for tool, stats in summary['individual_performance'].items():
            # Calcular porcentagens
            t_total = stats['total'] if stats['total'] > 0 else 1
            suc_pct = (stats['clean_correct'] / t_total) * 100
            err_pct = (stats['clean_incorrect'] / t_total) * 100
            conf_pct = (stats['conflict'] / t_total) * 100
            fail_pct = (stats['failure'] / t_total) * 100

            print(f"{tool.upper():<15} | "
                  f"{stats['clean_correct']:>4} ({suc_pct:>5.1f}%)    | "
                  f"{stats['clean_incorrect']:>4} ({err_pct:>5.1f}%)    | "
                  f"{stats['conflict']:>4} ({conf_pct:>4.1f}%) | "
                  f"{stats['failure']:>4}")
        print("-" * 80)
        print("* Sucesso: Merge automático idêntico ao gabarito.")
        print("* Erro: Merge automático diferente do gabarito (Silent Mismerge).")
        print("* Conflito: Ferramenta desistiu e reportou conflito.")

        # 2. Comparações Par a Par
        print("\n\n2. COMPARAÇÕES PAR A PAR (Melhoria Relativa)")
        print("-" * 80)
        for pair, metrics in summary['pairwise_comparisons'].items():
            if metrics['total_comparisons'] == 0: continue
            
            f1, f2 = pair.split('_vs_')
            print(f"\n[{f1.upper()} vs {f2.upper()}]")
            print(f"  FP Adicional ({f1} conflitou, {f2} acertou): {metrics['fp_adicional']}")
            print(f"  FN Adicional ({f1} errou, {f2} conflitou):   {metrics['fn_adicional']}")
            print(f"  Ambos Corretos:                              {metrics['corretos']}")

        # 3. Tempo de Execução
        print("\n\n3. TEMPO MÉDIO DE EXECUÇÃO (s)")
        print("-" * 80)
        for tool, times in summary['execution_time'].items():
            print(f"{tool.upper():<15}: {times['mean']:.4f}s")
        
        print("=" * 80 + "\n")