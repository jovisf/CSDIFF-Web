"""
Gerador de relatórios científicos.
Gera relatórios formatados para TCC/artigos.

Este módulo cria relatórios prontos para inclusão em trabalhos
acadêmicos, com tabelas formatadas de performance individual e comparativa.
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
            f.write("# Análise Experimental de Ferramentas de Merge\n\n")
            f.write(f"**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n")
            f.write(f"**Total de Triplas:** {summary['dataset_info']['total_triplets']}  \n")
            f.write(f"**Ferramentas Avaliadas:** {', '.join(summary['dataset_info']['tools'])}  \n\n")

            f.write("---\n\n")

            # ---------------------------------------------------------
            # SEÇÃO 1: PERFORMANCE INDIVIDUAL (TABELA PRINCIPAL DO TCC)
            # ---------------------------------------------------------
            f.write("## 1. Performance Individual (Comparação com Gabarito)\n\n")
            f.write("Esta tabela apresenta o desempenho de cada ferramenta comparada individualmente com o **Merge Commit (Gabarito)**.\n\n")
            
            f.write("| Ferramenta | Sucesso (Clean Correct) | Erro (Clean Incorrect) | Conflito | Falha |\n")
            f.write("|------------|-------------------------|------------------------|----------|-------|\n")

            if 'individual_performance' in summary:
                for tool, stats in summary['individual_performance'].items():
                    total = stats['total'] if stats['total'] > 0 else 1
                    
                    # Formatar valores com porcentagem
                    suc = f"{stats['clean_correct']} ({stats['clean_correct']/total*100:.1f}%)"
                    err = f"{stats['clean_incorrect']} ({stats['clean_incorrect']/total*100:.1f}%)"
                    conf = f"{stats['conflict']} ({stats['conflict']/total*100:.1f}%)"
                    fail = f"{stats['failure']} ({stats['failure']/total*100:.1f}%)"

                    f.write(f"| **{tool.upper()}** | {suc} | {err} | {conf} | {fail} |\n")
            
            f.write("\n**Definições:**\n")
            f.write("- **Sucesso:** A ferramenta realizou o merge automaticamente e o resultado é **idêntico** ao gabarito.\n")
            f.write("- **Erro:** A ferramenta realizou o merge automaticamente, mas o resultado é **diferente** do gabarito (Silent Mismerge).\n")
            f.write("- **Conflito:** A ferramenta não conseguiu resolver e reportou conflito.\n")
            f.write("- **Falha:** A ferramenta quebrou (ex: timeout, crash).\n\n")

            f.write("---\n\n")

            # ---------------------------------------------------------
            # SEÇÃO 2: COMPARAÇÕES PAR A PAR
            # ---------------------------------------------------------
            f.write("## 2. Comparações Par a Par (Análise Relativa)\n\n")
            f.write("Analisa onde uma ferramenta (F1) ganha ou perde em relação a outra (F2).\n\n")

            if 'pairwise_comparisons' in summary:
                for pair_key, metrics in summary['pairwise_comparisons'].items():
                    if metrics['total_comparisons'] == 0: continue

                    # Título do par (ex: CSDIFF-WEB vs MERGIRAF)
                    f1, f2 = pair_key.split('_vs_')
                    f.write(f"### {f1.upper()} vs {f2.upper()}\n\n")

                    f.write("| Métrica | Valor |\n")
                    f.write("|---------|-------|\n")
                    f.write(f"| Total Comparado | {metrics['total_comparisons']} |\n")
                    f.write(f"| **FP Adicional** ({f1} conflita, {f2} acerta) | {metrics['fp_adicional']} |\n")
                    f.write(f"| **FN Adicional** ({f1} erra, {f2} conflita) | {metrics['fn_adicional']} |\n")
                    f.write(f"| Ambos Corretos | {metrics['corretos']} |\n\n")

            f.write("---\n\n")

            # ---------------------------------------------------------
            # SEÇÃO 3: ANÁLISE DE CONFLITOS 
            # ---------------------------------------------------------
            f.write("## 3. Análise de Conflitos\n\n")
            f.write("Esta seção analisa a quantidade de conflitos gerados por cada ferramenta.\n\n")

            if 'conflict_metrics' in summary:
                f.write("### Métricas Gerais\n\n")
                f.write("| Ferramenta | Total Conflitos | Média por Arquivo | Máx. Conflitos |\n")
                f.write("|------------|-----------------|-------------------|----------------|\n")
                
                for tool, metrics in summary['conflict_metrics'].items():
                    f.write(f"| {tool.upper()} | {metrics['total_conflicts']} | {metrics['avg_conflicts']:.2f} | {metrics['max_conflicts']} |\n")
                f.write("\n")

            if 'conflict_distribution' in summary:
                f.write("### Distribuição de Conflitos (Quantidade de Arquivos)\n\n")
                f.write("| Ferramenta | 0 Conflitos (Limpo) | 1 Conflito | 2 Conflitos | 3+ Conflitos |\n")
                f.write("|------------|---------------------|------------|-------------|--------------|\n")

                for tool, dist in summary['conflict_distribution'].items():
                    f.write(f"| {tool.upper()} | {dist['0']} | {dist['1']} | {dist['2']} | {dist['3+']} |\n")
            
            f.write("\n---\n\n")

            # ---------------------------------------------------------
            # SEÇÃO 4: TEMPO DE EXECUÇÃO
            # ---------------------------------------------------------
            f.write("## 4. Tempo de Execução\n\n")
            f.write("| Ferramenta | Média (s) | Min (s) | Max (s) |\n")
            f.write("|------------|-----------|---------|---------|\n")

            if 'execution_time' in summary:
                for tool, times in summary['execution_time'].items():
                    f.write(f"| {tool} | {times['mean']:.4f} | {times['min']:.4f} | {times['max']:.4f} |\n")

            f.write("\n---\n")
            f.write("**Gerado por:** CSDiff-Web Analyzer\n")

        logger.info(f"Relatório Markdown gerado: {report_path}")
        return report_path

    def generate_latex_table(self, summary: Dict, filename: str = None) -> Path:
        """
        Gera tabela em LaTeX da Performance Individual (para TCC).

        Args:
            summary: Dict de análise
            filename: Nome do arquivo (padrão: table_TIMESTAMP.tex)

        Returns:
            Path do arquivo gerado
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'table_individual_performance_{timestamp}.tex'

        table_path = self.output_dir / filename

        with open(table_path, 'w', encoding='utf-8') as f:
            f.write("% Tabela de Performance Individual das Ferramentas\n")
            f.write("\\begin{table}[htbp]\n")
            f.write("\\centering\n")
            f.write("\\caption{Performance das Ferramentas em relação ao Gabarito}\n")
            f.write("\\label{tab:tool_performance}\n")
            f.write("\\begin{tabular}{lrrrr}\n")
            f.write("\\hline\n")
            f.write("\\textbf{Ferramenta} & \\textbf{Sucesso} & \\textbf{Erro} & \\textbf{Conflito} & \\textbf{Falha} \\\\\n")
            f.write("\\hline\n")

            if 'individual_performance' in summary:
                for tool, stats in summary['individual_performance'].items():
                    # Escapar underscores para LaTeX (ex: csdiff_web -> csdiff\_web)
                    tool_name = tool.replace('_', '\\_').upper()
                    
                    f.write(f"{tool_name} & {stats['clean_correct']} & {stats['clean_incorrect']} & {stats['conflict']} & {stats['failure']} \\\\\n")

            f.write("\\hline\n")
            f.write("\\end{tabular}\n")
            f.write("\\end{table}\n")

        logger.info(f"Tabela LaTeX gerada: {table_path}")
        return table_path