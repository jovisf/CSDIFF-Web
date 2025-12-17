"""
Analisador de métricas estatísticas.
Calcula análise comparativa usando merge commit como gabarito.

Este módulo implementa análise estatística avançada para validação
científica do CSDiff-Web conforme metodologia do TCC.

METODOLOGIA CORRIGIDA:
- Gabarito: Merge commit real do repositório (merged.ts)
- Comparação: Pares ordenados de ferramentas (F1, F2)
- Classificação: Falsos Positivos Adicionais e Falsos Negativos Adicionais

DEFINIÇÕES:
- Falso Positivo Adicional (F1 sobre F2): F1 reportou conflito, mas F2
  integrou corretamente (F2 = resultado do repo)
- Falso Negativo Adicional (F1 sobre F2): F1 não reportou conflito, mas
  produziu resultado incorreto (F1 ≠ repo), enquanto F2 reportou conflito
- Correto: Sem conflito E resultado = repo
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

    def compare_tools_pairwise(
        self,
        f1_name: str,
        f2_name: str
    ) -> Dict:
        """
        Compara duas ferramentas usando comparação par a par com merge commit como gabarito.

        Args:
            f1_name: Nome da ferramenta 1 (ex: 'csdiff_web', 'diff3', 'slow_diff3')
            f2_name: Nome da ferramenta 2 (ex: 'csdiff_web', 'diff3', 'slow_diff3')

        Returns:
            Dict com métricas:
            {
                'pair': str,
                'f1_fp_adicional': int,  # F1 tem FP adicional sobre F2
                'f1_fn_adicional': int,  # F1 tem FN adicional sobre F2
                'f1_correto': int,       # F1 acertou
                'indefinido': int,       # Casos indefinidos
                'total': int
            }
        """
        classifier = ComparisonClassifier()

        # Colunas necessárias
        f1_conflict_col = f'{f1_name}_has_conflict'
        f2_conflict_col = f'{f2_name}_has_conflict'
        f1_output_col = f'{f1_name}_output'
        f2_output_col = f'{f2_name}_output'
        repo_col = 'repo_merged_content'

        # Verificar se colunas existem
        required = [f1_conflict_col, f2_conflict_col, f1_output_col, f2_output_col, repo_col]
        missing = [col for col in required if col not in self.df.columns]
        if missing:
            logger.error(f"Colunas faltando para comparação: {missing}")
            return {
                'pair': f"{f1_name} vs {f2_name}",
                'error': f"Colunas faltando: {missing}"
            }

        # Filtrar linhas válidas
        valid_mask = (
            self.df[f1_conflict_col].notna() &
            self.df[f2_conflict_col].notna() &
            self.df[f1_output_col].notna() &
            self.df[f2_output_col].notna() &
            self.df[repo_col].notna()
        )

        # Classificar cada linha
        for idx in self.df[valid_mask].index:
            row = self.df.loc[idx]

            f1_data = {
                'output': str(row[f1_output_col]),
                'has_conflict': bool(row[f1_conflict_col])
            }
            f2_data = {
                'output': str(row[f2_output_col]),
                'has_conflict': bool(row[f2_conflict_col])
            }
            repo_expected = str(row[repo_col])

            classifier.classify_pair(f1_name, f2_name, f1_data, f2_data, repo_expected)

        # Retornar estatísticas
        stats = classifier.get_statistics()
        return {
            'pair': f"{f1_name} vs {f2_name}",
            'f1_name': f1_name,
            'f2_name': f2_name,
            'f1_fp_adicional': stats['fp_adicional'],
            'f1_fn_adicional': stats['fn_adicional'],
            'f1_correto': stats['corretos'],
            'indefinido': stats['indefinidos'],
            'total': stats['total_comparisons']
        }

    def compare_all_pairs(self, tools: List[str] = None) -> Dict[str, Dict]:
        """
        Compara todos os pares ordenados de ferramentas.

        Args:
            tools: Lista de ferramentas a comparar (padrão: ['csdiff_web', 'diff3', 'slow_diff3'])

        Returns:
            Dict com resultados de todas as comparações:
            {
                'csdiff_web_vs_diff3': {...},
                'csdiff_web_vs_slow_diff3': {...},
                ...
            }
        """
        if tools is None:
            tools = ['csdiff_web', 'diff3', 'slow_diff3']

        results = {}

        # Gerar todos os pares ordenados (F1, F2) onde F1 != F2
        for f1 in tools:
            for f2 in tools:
                if f1 != f2:
                    pair_key = f"{f1}_vs_{f2}"
                    logger.info(f"Comparando par: {pair_key}")
                    results[pair_key] = self.compare_tools_pairwise(f1, f2)

        return results

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
        # NOVA METODOLOGIA: Comparações par a par usando merge commit como gabarito
        pairwise_comparisons = {}
        if 'repo_merged_content' in self.df.columns:
            logger.info("Executando comparações par a par com gabarito do repo...")
            pairwise_comparisons = self.compare_all_pairs()
        else:
            logger.warning("Coluna 'repo_merged_content' não encontrada - pulando comparações par a par")

        # Calcular FP/FN para CSDiff-Web (LEGADO - manter para compatibilidade)
        fp_fn_metrics = {}
        if 'csdiff_web_has_conflict' in self.df.columns and 'slow_diff3_has_conflict' in self.df.columns:
            fp_fn_metrics['csdiff-web'] = self.calculate_fp_fn('csdiff_web_has_conflict', baseline_col='slow_diff3_has_conflict')

        # Outras métricas
        conflict_comparison = self.compare_conflict_rates()
        conflict_distribution = self.analyze_conflict_distribution()
        execution_time = self.analyze_execution_time()

        return {
            'pairwise_comparisons': pairwise_comparisons,  # NOVA METODOLOGIA
            'fp_fn_analysis': fp_fn_metrics,  # LEGADO
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

        # NOVA METODOLOGIA: Comparações par a par
        if summary['pairwise_comparisons']:
            print("=" * 60)
            print("COMPARAÇÕES PAR A PAR (Gabarito: Merge Commit Real)")
            print("=" * 60)

            for pair_key, metrics in summary['pairwise_comparisons'].items():
                if 'error' in metrics:
                    print(f"\n{metrics['pair']}: {metrics['error']}")
                    continue

                print(f"\n{metrics['pair'].upper()}:")
                print(f"  Total de comparações:        {metrics['total']}")
                print(f"  FP Adicionais de {metrics['f1_name']}: {metrics['f1_fp_adicional']}")
                print(f"  FN Adicionais de {metrics['f1_name']}: {metrics['f1_fn_adicional']}")
                print(f"  {metrics['f1_name']} Correto:         {metrics['f1_correto']}")
                print(f"  Indefinidos:                 {metrics['indefinido']}")

                # Calcular taxas
                if metrics['total'] > 0:
                    fp_rate = metrics['f1_fp_adicional'] / metrics['total'] * 100
                    fn_rate = metrics['f1_fn_adicional'] / metrics['total'] * 100
                    correct_rate = metrics['f1_correto'] / metrics['total'] * 100
                    print(f"\n  Taxa FP Adicional: {fp_rate:.1f}%")
                    print(f"  Taxa FN Adicional: {fn_rate:.1f}%")
                    print(f"  Taxa Correto:      {correct_rate:.1f}%")

        # FP/FN (LEGADO - manter para comparação)
        if summary['fp_fn_analysis']:
            print("\n" + "=" * 60)
            print("FALSE POSITIVES / FALSE NEGATIVES (LEGADO - baseline: slow-diff3)")
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
