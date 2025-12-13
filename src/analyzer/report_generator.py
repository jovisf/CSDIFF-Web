"""
Gerador de relatórios científicos.
Gera relatórios formatados para TCC/artigos.

Este módulo cria relatórios prontos para inclusão em trabalhos
acadêmicos, com tabelas formatadas e análise comparativa.
"""

from pathlib import Path
from typing import Dict
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ReportGenerator:
    """
    Gerador de relatórios científicos.

    Cria relatórios em Markdown e texto formatado.
    """

    def __init__(self, output_dir: Path):
        """
        Inicializa gerador.

        Args:
            output_dir: Diretório para salvar relatórios
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_markdown_report(
        self,
        summary: Dict,
        filename: str = None
    ) -> Path:
        """
        Gera relatório em Markdown.

        Args:
            summary: Dict retornado por MetricsAnalyzer.generate_summary_report()
            filename: Nome do arquivo (padrão: analysis_TIMESTAMP.md)

        Returns:
            Path do arquivo gerado
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'analysis_{timestamp}.md'

        report_path = self.output_dir / filename

        with open(report_path, 'w', encoding='utf-8') as f:
            # Cabeçalho
            f.write("# Análise Comparativa - CSDiff-Web vs diff3 vs Mergiraf\n\n")
            f.write(f"**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n")
            f.write(f"**Dataset:** {summary['dataset_info']['total_triplets']} triplas  \n")
            f.write(f"**Ferramentas:** {', '.join(summary['dataset_info']['tools_compared'])}  \n\n")

            f.write("---\n\n")

            # Seção 1: False Positives / False Negatives
            if summary['fp_fn_analysis']:
                f.write("## 1. Análise de False Positives / False Negatives\n\n")
                f.write("Baseline: **diff3** (ground truth)\n\n")

                for tool, metrics in summary['fp_fn_analysis'].items():
                    f.write(f"### {tool.upper()}\n\n")

                    # Tabela de confusão
                    f.write("**Matriz de Confusão:**\n\n")
                    f.write("| Métrica | Valor |\n")
                    f.write("|---------|-------|\n")
                    f.write(f"| True Positives (TP) | {metrics['TP']} |\n")
                    f.write(f"| False Positives (FP) | {metrics['FP']} |\n")
                    f.write(f"| True Negatives (TN) | {metrics['TN']} |\n")
                    f.write(f"| False Negatives (FN) | {metrics['FN']} |\n\n")

                    # Métricas derivadas
                    f.write("**Métricas de Performance:**\n\n")
                    f.write("| Métrica | Valor | Interpretação |\n")
                    f.write("|---------|-------|---------------|\n")
                    f.write(f"| Precision | {metrics['precision']:.3f} | Proporção de conflitos detectados que são reais |\n")
                    f.write(f"| Recall | {metrics['recall']:.3f} | Proporção de conflitos reais que foram detectados |\n")
                    f.write(f"| F1-Score | {metrics['f1_score']:.3f} | Média harmônica entre Precision e Recall |\n")
                    f.write(f"| Accuracy | {metrics['accuracy']:.3f} | Taxa de acertos geral |\n\n")

            # Seção 2: Comparação de Conflitos
            if summary['conflict_comparison']:
                f.write("## 2. Comparação de Taxa de Conflitos\n\n")

                # Tabela comparativa
                f.write("| Ferramenta | Total | Com Conflito | Sem Conflito | Taxa de Conflito |\n")
                f.write("|------------|-------|--------------|--------------|------------------|\n")

                for tool, data in summary['conflict_comparison'].items():
                    if tool == 'reduction':
                        continue

                    f.write(f"| **{tool}** | {data['total']} | {data['with_conflict']} | {data['without_conflict']} | {data['conflict_rate']:.1f}% |\n")

                f.write("\n")

                # Redução
                if 'reduction' in summary['conflict_comparison']:
                    red = summary['conflict_comparison']['reduction']

                    f.write("### Redução de Conflitos (CSDiff-Web vs diff3)\n\n")
                    f.write(f"- **Redução absoluta:** {red['absolute']} conflitos\n")
                    f.write(f"- **Redução relativa:** {red['relative']:.1f}%\n\n")

                    # Interpretação
                    if red['relative'] > 0:
                        f.write(f"✅ **CSDiff-Web reduziu {red['relative']:.1f}% dos conflitos** em relação ao diff3.\n\n")
                    elif red['relative'] < 0:
                        f.write(f"⚠️ CSDiff-Web gerou {abs(red['relative']):.1f}% mais conflitos que diff3.\n\n")
                    else:
                        f.write(f"➡️ CSDiff-Web teve desempenho equivalente ao diff3.\n\n")

            # Seção 3: Distribuição de Conflitos
            if summary['conflict_distribution']:
                f.write("## 3. Distribuição de Conflitos\n\n")

                f.write("Número de conflitos por tripla:\n\n")
                f.write("| Ferramenta | 0 | 1 | 2 | 3+ |\n")
                f.write("|------------|---|---|---|----|\n")

                for tool, dist in summary['conflict_distribution'].items():
                    counts = [str(dist.get(str(i), 0)) for i in range(3)]
                    counts.append(str(dist.get('3+', 0)))
                    f.write(f"| **{tool}** | {' | '.join(counts)} |\n")

                f.write("\n")

            # Seção 4: Tempo de Execução
            if summary['execution_time']:
                f.write("## 4. Análise de Performance (Tempo de Execução)\n\n")

                f.write("| Ferramenta | Média (s) | Mediana (s) | Desvio Padrão | Min/Max (s) |\n")
                f.write("|------------|-----------|-------------|---------------|-------------|\n")

                for tool, data in summary['execution_time'].items():
                    f.write(f"| **{tool}** | {data['mean']:.4f} | {data['median']:.4f} | {data['std']:.4f} | {data['min']:.4f} / {data['max']:.4f} |\n")

                f.write("\n")

                # Comparação de performance
                if 'csdiff-web' in summary['execution_time'] and 'diff3' in summary['execution_time']:
                    csdiff_time = summary['execution_time']['csdiff-web']['mean']
                    diff3_time = summary['execution_time']['diff3']['mean']
                    overhead = ((csdiff_time - diff3_time) / diff3_time * 100) if diff3_time > 0 else 0

                    f.write("### Overhead de Performance\n\n")
                    f.write(f"- **diff3 médio:** {diff3_time:.4f}s\n")
                    f.write(f"- **CSDiff-Web médio:** {csdiff_time:.4f}s\n")
                    f.write(f"- **Overhead:** {overhead:+.1f}%\n\n")

            # Seção 5: Conclusões
            f.write("## 5. Conclusões\n\n")

            # Auto-gerar conclusões baseadas nos dados
            conclusions = []

            # Conclusão 1: Redução de conflitos
            if 'reduction' in summary.get('conflict_comparison', {}):
                red_pct = summary['conflict_comparison']['reduction']['relative']
                if red_pct > 10:
                    conclusions.append(f"1. **CSDiff-Web demonstrou redução significativa de {red_pct:.1f}% nos conflitos** em relação ao diff3, validando a eficácia da abordagem baseada em separadores sintáticos.")
                elif red_pct > 0:
                    conclusions.append(f"1. CSDiff-Web apresentou redução moderada de {red_pct:.1f}% nos conflitos.")
                else:
                    conclusions.append(f"1. CSDiff-Web teve desempenho similar ao diff3 em termos de conflitos ({red_pct:.1f}% de variação).")

            # Conclusão 2: Precisão
            if summary.get('fp_fn_analysis', {}).get('csdiff-web'):
                precision = summary['fp_fn_analysis']['csdiff-web']['precision']
                if precision >= 0.90:
                    conclusions.append(f"2. **Alta precisão** ({precision:.3f}) indica que CSDiff-Web gera poucos falsos positivos.")
                elif precision >= 0.70:
                    conclusions.append(f"2. Precisão moderada ({precision:.3f}) com espaço para melhoria na redução de falsos positivos.")
                else:
                    conclusions.append(f"2. Precisão baixa ({precision:.3f}) indica necessidade de ajustes no algoritmo.")

            # Conclusão 3: Performance
            if 'csdiff-web' in summary.get('execution_time', {}) and 'diff3' in summary.get('execution_time', {}):
                overhead = ((summary['execution_time']['csdiff-web']['mean'] - summary['execution_time']['diff3']['mean']) / summary['execution_time']['diff3']['mean'] * 100)
                if overhead < 50:
                    conclusions.append(f"3. **Overhead de performance aceitável** ({overhead:+.1f}%), tornando CSDiff-Web viável para uso prático.")
                else:
                    conclusions.append(f"3. Overhead de performance significativo ({overhead:+.1f}%) pode limitar uso em cenários críticos.")

            for conclusion in conclusions:
                f.write(f"{conclusion}\n\n")

            # Rodapé
            f.write("---\n\n")
            f.write("**Gerado por:** CSDiff-Web Analyzer  \n")
            f.write("**Projeto:** TCC - Universidade Federal de Pernambuco  \n")
            f.write("**Orientador:** Prof. Paulo Borba  \n")

        logger.info(f"Relatório Markdown gerado: {report_path}")
        return report_path

    def generate_latex_table(self, summary: Dict, filename: str = None) -> Path:
        """
        Gera tabela em LaTeX (para inclusão em artigos/TCC).

        Args:
            summary: Dict de análise
            filename: Nome do arquivo (padrão: table_TIMESTAMP.tex)

        Returns:
            Path do arquivo gerado
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'table_{timestamp}.tex'

        table_path = self.output_dir / filename

        with open(table_path, 'w', encoding='utf-8') as f:
            # Tabela comparativa de conflitos
            f.write("% Tabela comparativa - CSDiff-Web vs diff3\n")
            f.write("\\begin{table}[htbp]\n")
            f.write("\\centering\n")
            f.write("\\caption{Comparação de Conflitos entre Ferramentas}\n")
            f.write("\\label{tab:conflict_comparison}\n")
            f.write("\\begin{tabular}{lrrr}\n")
            f.write("\\hline\n")
            f.write("\\textbf{Ferramenta} & \\textbf{Total} & \\textbf{Com Conflito} & \\textbf{Taxa (\\%)} \\\\\n")
            f.write("\\hline\n")

            if summary.get('conflict_comparison'):
                for tool, data in summary['conflict_comparison'].items():
                    if tool == 'reduction':
                        continue

                    f.write(f"{tool} & {data['total']} & {data['with_conflict']} & {data['conflict_rate']:.1f} \\\\\n")

            f.write("\\hline\n")
            f.write("\\end{tabular}\n")
            f.write("\\end{table}\n")

        logger.info(f"Tabela LaTeX gerada: {table_path}")
        return table_path
