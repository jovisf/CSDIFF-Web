"""
Coletor de resultados de experimentos.
Coleta métricas e gera relatórios CSV.

Este módulo é responsável por:
1. Coletar resultados de múltiplas execuções
2. Calcular métricas (conflitos, FP, FN, tempo)
3. Gerar CSV comparativo
4. Gerar estatísticas agregadas
"""

import csv
from pathlib import Path
from typing import List, Dict
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ResultCollector:
    """
    Coletor de resultados de experimentos.

    Armazena resultados de execuções e gera relatórios.
    """

    def __init__(self, output_dir: Path):
        """
        Inicializa coletor.

        Args:
            output_dir: Diretório para salvar resultados
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.results = []  # Lista de resultados de cada tripla
        self.stats = {
            'total_triplets': 0,
            'successful_triplets': 0,
            'failed_triplets': 0,
        }

    def add_result(
        self,
        triplet_id: str,
        triplet_metadata: Dict,
        tool_results: Dict[str, Dict]
    ):
        """
        Adiciona resultado de uma tripla.

        Args:
            triplet_id: ID da tripla (ex: "triplet_001")
            triplet_metadata: Metadata da tripla (filepath, extension, etc)
            tool_results: Resultados de cada ferramenta:
                {
                    'csdiff-web': {...},
                    'diff3': {...},
                    'slow-diff3': {...}
                }
        """
        self.stats['total_triplets'] += 1

        # Verificar se pelo menos uma ferramenta teve sucesso
        any_success = any(
            result.get('success', False)
            for result in tool_results.values()
        )

        if any_success:
            self.stats['successful_triplets'] += 1
        else:
            self.stats['failed_triplets'] += 1

        # Armazenar resultado
        result_entry = {
            'triplet_id': triplet_id,
            'filepath': triplet_metadata.get('filepath', ''),
            'extension': triplet_metadata.get('extension', ''),
            'commit_sha': triplet_metadata.get('commit_sha', '')[:8],
            **self._flatten_tool_results(tool_results)
        }

        self.results.append(result_entry)

        logger.debug(f"Resultado adicionado: {triplet_id}")

    def _flatten_tool_results(self, tool_results: Dict[str, Dict]) -> Dict:
        """
        Achata resultados de ferramentas para formato CSV.

        Args:
            tool_results: Dict com resultados de cada ferramenta

        Returns:
            Dict com campos planificados:
            {
                'csdiff_success': bool,
                'csdiff_conflicts': int,
                'csdiff_time': float,
                'diff3_success': bool,
                ...
            }
        """
        flattened = {}

        for tool_name, result in tool_results.items():
            # Normalizar nome (remover hífens)
            prefix = tool_name.replace('-', '_')

            flattened[f'{prefix}_success'] = result.get('success', False)
            flattened[f'{prefix}_has_conflict'] = result.get('has_conflict', None)
            flattened[f'{prefix}_num_conflicts'] = result.get('num_conflicts', None)
            flattened[f'{prefix}_time'] = result.get('execution_time', None)
            flattened[f'{prefix}_error'] = result.get('error', None)

        return flattened

    def generate_csv(self, filename: str = None) -> Path:
        """
        Gera relatório CSV com todos os resultados.

        Args:
            filename: Nome do arquivo CSV (padrão: results_TIMESTAMP.csv)

        Returns:
            Path do arquivo CSV gerado
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'results_{timestamp}.csv'

        csv_path = self.output_dir / filename

        if not self.results:
            logger.warning("Nenhum resultado para gerar CSV")
            return csv_path

        # Coletar todos os campos
        fieldnames = set()
        for result in self.results:
            fieldnames.update(result.keys())

        fieldnames = sorted(fieldnames)

        # Escrever CSV
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.results)

        logger.info(f"CSV gerado: {csv_path} ({len(self.results)} linhas)")
        return csv_path

    def calculate_metrics(self) -> Dict:
        """
        Calcula métricas agregadas.

        Returns:
            Dict com métricas por ferramenta:
            {
                'csdiff-web': {
                    'total_executions': int,
                    'successful_executions': int,
                    'avg_conflicts': float,
                    'avg_time': float,
                    ...
                },
                ...
            }
        """
        if not self.results:
            return {}

        metrics = {}

        # Para cada ferramenta
        for tool in ['csdiff_web', 'diff3', 'slow_diff3']:
            tool_metrics = self._calculate_tool_metrics(tool)
            metrics[tool.replace('_', '-')] = tool_metrics

        return metrics

    def _calculate_tool_metrics(self, tool_prefix: str) -> Dict:
        """
        Calcula métricas para uma ferramenta específica.

        Args:
            tool_prefix: Prefixo da ferramenta (ex: 'csdiff_web')

        Returns:
            Dict com métricas agregadas
        """
        successes = []
        conflicts = []
        times = []
        errors = []

        for result in self.results:
            success = result.get(f'{tool_prefix}_success')
            num_conflicts = result.get(f'{tool_prefix}_num_conflicts')
            time_taken = result.get(f'{tool_prefix}_time')
            error = result.get(f'{tool_prefix}_error')

            if success is not None:
                successes.append(success)

            if num_conflicts is not None:
                conflicts.append(num_conflicts)

            if time_taken is not None:
                times.append(time_taken)

            if error:
                errors.append(error)

        # Calcular agregados
        total = len(successes)
        successful = sum(successes) if successes else 0

        return {
            'total_executions': total,
            'successful_executions': successful,
            'failed_executions': total - successful,
            'success_rate': (successful / total * 100) if total > 0 else 0,
            'total_conflicts': sum(conflicts) if conflicts else 0,
            'avg_conflicts': (sum(conflicts) / len(conflicts)) if conflicts else 0,
            'min_conflicts': min(conflicts) if conflicts else 0,
            'max_conflicts': max(conflicts) if conflicts else 0,
            'avg_time': (sum(times) / len(times)) if times else 0,
            'min_time': min(times) if times else 0,
            'max_time': max(times) if times else 0,
            'total_errors': len(errors),
            'unique_errors': len(set(errors)) if errors else 0
        }

    def generate_summary(self, filename: str = None) -> Path:
        """
        Gera resumo textual dos resultados.

        Args:
            filename: Nome do arquivo (padrão: summary_TIMESTAMP.txt)

        Returns:
            Path do arquivo de resumo
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'summary_{timestamp}.txt'

        summary_path = self.output_dir / filename

        metrics = self.calculate_metrics()

        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("RESUMO DOS EXPERIMENTOS - CSDiff-Web\n")
            f.write("=" * 60 + "\n\n")

            f.write(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total de triplas: {self.stats['total_triplets']}\n")
            f.write(f"Triplas bem-sucedidas: {self.stats['successful_triplets']}\n")
            f.write(f"Triplas falhadas: {self.stats['failed_triplets']}\n\n")

            # Métricas por ferramenta
            for tool_name, tool_metrics in metrics.items():
                f.write("=" * 60 + "\n")
                f.write(f"FERRAMENTA: {tool_name.upper()}\n")
                f.write("=" * 60 + "\n")
                f.write(f"Total de execucoes:     {tool_metrics['total_executions']}\n")
                f.write(f"Execucoes bem-sucedidas: {tool_metrics['successful_executions']}\n")
                f.write(f"Execucoes falhadas:      {tool_metrics['failed_executions']}\n")
                f.write(f"Taxa de sucesso:         {tool_metrics['success_rate']:.1f}%\n\n")

                f.write(f"Total de conflitos:      {tool_metrics['total_conflicts']}\n")
                f.write(f"Media de conflitos:      {tool_metrics['avg_conflicts']:.2f}\n")
                f.write(f"Min/Max conflitos:       {tool_metrics['min_conflicts']} / {tool_metrics['max_conflicts']}\n\n")

                f.write(f"Tempo medio:             {tool_metrics['avg_time']:.3f}s\n")
                f.write(f"Min/Max tempo:           {tool_metrics['min_time']:.3f}s / {tool_metrics['max_time']:.3f}s\n\n")

                f.write(f"Total de erros:          {tool_metrics['total_errors']}\n")
                f.write(f"Erros unicos:            {tool_metrics['unique_errors']}\n\n")

            # Comparação
            f.write("=" * 60 + "\n")
            f.write("COMPARACAO\n")
            f.write("=" * 60 + "\n")

            if 'csdiff-web' in metrics and 'diff3' in metrics:
                csdiff_conflicts = metrics['csdiff-web']['total_conflicts']
                diff3_conflicts = metrics['diff3']['total_conflicts']

                reduction = diff3_conflicts - csdiff_conflicts
                reduction_pct = (reduction / diff3_conflicts * 100) if diff3_conflicts > 0 else 0

                f.write(f"Reducao de conflitos (CSDiff-Web vs diff3):\n")
                f.write(f"  diff3:      {diff3_conflicts} conflitos\n")
                f.write(f"  CSDiff-Web: {csdiff_conflicts} conflitos\n")
                f.write(f"  Reducao:    {reduction} ({reduction_pct:.1f}%)\n\n")

        logger.info(f"Resumo gerado: {summary_path}")
        return summary_path

    def get_statistics(self) -> Dict:
        """Retorna estatisticas globais."""
        return self.stats.copy()

    def print_statistics(self):
        """Imprime estatisticas formatadas."""
        print("\n" + "=" * 60)
        print("ESTATISTICAS DO COLETOR")
        print("=" * 60)
        print(f"Total de triplas:        {self.stats['total_triplets']}")
        print(f"Triplas bem-sucedidas:   {self.stats['successful_triplets']}")
        print(f"Triplas falhadas:        {self.stats['failed_triplets']}")
        print("=" * 60 + "\n")
