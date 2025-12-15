"""
Analisador de métricas estatísticas.
Calcula False Positives, False Negatives e análise comparativa.

Este módulo implementa análise estatística avançada para validação
científica do CSDiff-Web conforme metodologia do TCC.

DEFINIÇÕES:
- True Positive (TP): Ferramenta detectou conflito E há conflito real
- False Positive (FP): Ferramenta detectou conflito MAS não há conflito real
- True Negative (TN): Ferramenta não detectou conflito E não há conflito real
- False Negative (FN): Ferramenta não detectou conflito MAS há conflito real

BASELINE: slow-diff3 é considerado ground truth (referência)
"""

import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)


class MetricsAnalyzer:
    """
    Analisador de métricas estatísticas.

    Calcula FP, FN, precisão, recall, F1-score e comparações.
    """

    def __init__(self, csv_path: Path):
        """
        Inicializa analisador com resultados CSV.

        Args:
            csv_path: Path do CSV gerado pelo Runner
        """
        self.csv_path = Path(csv_path)
        self.df = None
        self.metrics = {}

        # Carregar CSV
        self._load_csv()

    def _load_csv(self):
        """Carrega e valida CSV."""
        try:
            self.df = pd.read_csv(self.csv_path)
            logger.info(f"CSV carregado: {len(self.df)} linhas")

            # Validar colunas necessárias
            required_cols = [
                'csdiff_web_has_conflict',
                'diff3_has_conflict',
                'slow_diff3_has_conflict',
                'csdiff_web_num_conflicts',
                'diff3_num_conflicts',
                'slow_diff3_num_conflicts',
                
            ]

            missing = [col for col in required_cols if col not in self.df.columns]
            if missing:
                logger.warning(f"Colunas faltando no CSV: {missing}")

        except Exception as e:
            logger.error(f"Erro ao carregar CSV: {e}")
            raise

    def calculate_fp_fn(
        self,
        tool_col: str,
        baseline_col: str = 'slow_diff3_has_conflict'
    ) -> Dict:
        """
        Calcula False Positives e False Negatives.

        Usa slow_diff3 como baseline (ground truth).

        Args:
            tool_col: Coluna da ferramenta a analisar (ex: 'csdiff_web_has_conflict')
            baseline_col: Coluna do baseline (padrão: 'slow_diff3_has_conflict')

        Returns:
            Dict com métricas:
            {
                'TP': int,  # True Positives
                'FP': int,  # False Positives
                'TN': int,  # True Negatives
                'FN': int,  # False Negatives
                'precision': float,
                'recall': float,
                'f1_score': float,
                'accuracy': float
            }
        """
        # Filtrar linhas válidas (sem NaN)
        valid_mask = (
            self.df[tool_col].notna() &
            self.df[baseline_col].notna()
        )
        tool_values = self.df[valid_mask][tool_col]
        baseline_values = self.df[valid_mask][baseline_col]

        # Calcular TP, FP, TN, FN
        TP = ((tool_values == True) & (baseline_values == True)).sum()
        FP = ((tool_values == True) & (baseline_values == False)).sum()
        TN = ((tool_values == False) & (baseline_values == False)).sum()
        FN = ((tool_values == False) & (baseline_values == True)).sum()

        # Calcular métricas derivadas
        precision = TP / (TP + FP) if (TP + FP) > 0 else 0.0
        recall = TP / (TP + FN) if (TP + FN) > 0 else 0.0
        f1_score = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        accuracy = (TP + TN) / (TP + FP + TN + FN) if (TP + FP + TN + FN) > 0 else 0.0

        return {
            'TP': int(TP),
            'FP': int(FP),
            'TN': int(TN),
            'FN': int(FN),
            'precision': float(precision),
            'recall': float(recall),
            'f1_score': float(f1_score),
            'accuracy': float(accuracy),
            'total_samples': int(TP + FP + TN + FN)
        }

    def compare_conflict_rates(self) -> Dict:
        """
        Compara taxas de conflito entre ferramentas.

        Returns:
            Dict com comparações:
            {
                'csdiff-web': {'total': int, 'with_conflict': int, 'rate': float},
                'slow-diff3': {...},
                'reduction': {'absolute': int, 'relative': float}
            }
        """
        results = {}

        # Para cada ferramenta
        for tool in ['csdiff_web', 'diff3', 'slow_diff3']:
            conflict_col = f'{tool}_has_conflict'

            if conflict_col not in self.df.columns:
                continue

            # Filtrar valores válidos
            valid = self.df[conflict_col].notna()
            total = valid.sum()
            with_conflict = (self.df[conflict_col] == True).sum()
            rate = (with_conflict / total * 100) if total > 0 else 0.0

            tool_name = tool.replace('_', '-')
            results[tool_name] = {
                'total': int(total),
                'with_conflict': int(with_conflict),
                'without_conflict': int(total - with_conflict),
                'conflict_rate': float(rate)
            }

        # Calcular redução (CSDiff-Web vs slow-diff3)
        if 'csdiff-web' in results and 'slow-diff3' in results:
            csdiff_conflicts = results['csdiff-web']['with_conflict']
            slow_conflicts = results['slow-diff3']['with_conflict']

            absolute_reduction = slow_conflicts - csdiff_conflicts
            relative_reduction = (absolute_reduction / slow_conflicts * 100) if slow_conflicts > 0 else 0.0

            results['reduction'] = {
                'absolute': int(absolute_reduction),
                'relative': float(relative_reduction)
            }

        return results

    def analyze_conflict_distribution(self) -> Dict:
        """
        Analisa distribuição de conflitos (0, 1, 2, 3+).

        Returns:
            Dict com distribuições por ferramenta
        """
        results = {}

        for tool in ['csdiff_web', 'diff3', 'slow_diff3']:
            num_col = f'{tool}_num_conflicts'

            if num_col not in self.df.columns:
                continue

            # Contar conflitos
            conflict_counts = self.df[num_col].value_counts().sort_index()

            # Agrupar 3+
            distribution = {}
            for num_conflicts in conflict_counts.index:
                if pd.isna(num_conflicts):
                    continue

                num_conflicts = int(num_conflicts)
                if num_conflicts >= 3:
                    distribution['3+'] = distribution.get('3+', 0) + conflict_counts[num_conflicts]
                else:
                    distribution[str(num_conflicts)] = int(conflict_counts[num_conflicts])

            tool_name = tool.replace('_', '-')
            results[tool_name] = distribution

        return results

    def analyze_execution_time(self) -> Dict:
        """
        Analisa tempo de execução.

        Returns:
            Dict com estatísticas de tempo por ferramenta
        """
        results = {}

        for tool in ['csdiff_web', 'diff3', 'slow_diff3']:
            time_col = f'{tool}_time'

            if time_col not in self.df.columns:
                continue

            # Filtrar valores válidos
            times = self.df[time_col].dropna()

            if len(times) == 0:
                continue

            tool_name = tool.replace('_', '-')
            results[tool_name] = {
                'mean': float(times.mean()),
                'median': float(times.median()),
                'std': float(times.std()),
                'min': float(times.min()),
                'max': float(times.max()),
                'total': float(times.sum())
            }

        return results

    def generate_summary_report(self) -> Dict:
        """
        Gera relatório resumido com todas as métricas.

        Returns:
            Dict consolidado com todas as análises
        """
        # Calcular FP/FN para CSDiff-Web
        fp_fn_metrics = {}
        if 'csdiff_web_has_conflict' in self.df.columns:
            fp_fn_metrics['csdiff-web'] = self.calculate_fp_fn('csdiff_web_has_conflict', baseline_col='slow_diff3_has_conflict')

        # Outras métricas
        conflict_comparison = self.compare_conflict_rates()
        conflict_distribution = self.analyze_conflict_distribution()
        execution_time = self.analyze_execution_time()

        return {
            'fp_fn_analysis': fp_fn_metrics,
            'conflict_comparison': conflict_comparison,
            'conflict_distribution': conflict_distribution,
            'execution_time': execution_time,
            'dataset_info': {
                'total_triplets': len(self.df),
                'tools_compared': list(conflict_comparison.keys())
            }
        }

    def print_summary(self):
        """Imprime resumo formatado."""
        summary = self.generate_summary_report()

        print("\n" + "=" * 60)
        print("ANÁLISE ESTATÍSTICA - CSDiff-Web")
        print("=" * 60)
        print(f"Total de triplas: {summary['dataset_info']['total_triplets']}")
        print()

        # FP/FN
        if summary['fp_fn_analysis']:
            print("=" * 60)
            print("FALSE POSITIVES / FALSE NEGATIVES")
            print("=" * 60)

            for tool, metrics in summary['fp_fn_analysis'].items():
                print(f"\n{tool.upper()} (baseline: slow-diff3):")
                print(f"  True Positives:  {metrics['TP']}")
                print(f"  False Positives: {metrics['FP']}")
                print(f"  True Negatives:  {metrics['TN']}")
                print(f"  False Negatives: {metrics['FN']}")
                print(f"\n  Precision: {metrics['precision']:.3f}")
                print(f"  Recall:    {metrics['recall']:.3f}")
                print(f"  F1-Score:  {metrics['f1_score']:.3f}")
                print(f"  Accuracy:  {metrics['accuracy']:.3f}")

        # Comparação de conflitos
        if summary['conflict_comparison']:
            print("\n" + "=" * 60)
            print("COMPARAÇÃO DE CONFLITOS")
            print("=" * 60)

            for tool, data in summary['conflict_comparison'].items():
                if tool == 'reduction':
                    continue

                print(f"\n{tool.upper()}:")
                print(f"  Total de triplas:     {data['total']}")
                print(f"  Com conflito:         {data['with_conflict']} ({data['conflict_rate']:.1f}%)")
                print(f"  Sem conflito:         {data['without_conflict']}")

            if 'reduction' in summary['conflict_comparison']:
                red = summary['conflict_comparison']['reduction']
                print(f"\nREDUÇÃO (CSDiff-Web vs slow-diff3):")
                print(f"  Absoluta: {red['absolute']} conflitos")
                print(f"  Relativa: {red['relative']:.1f}%")

        # Tempo de execução
        if summary['execution_time']:
            print("\n" + "=" * 60)
            print("TEMPO DE EXECUÇÃO")
            print("=" * 60)

            for tool, data in summary['execution_time'].items():
                print(f"\n{tool.upper()}:")
                print(f"  Média:   {data['mean']:.4f}s")
                print(f"  Mediana: {data['median']:.4f}s")
                print(f"  Min/Max: {data['min']:.4f}s / {data['max']:.4f}s")

        print("\n" + "=" * 60 + "\n")
