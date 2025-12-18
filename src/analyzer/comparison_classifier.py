"""
Classificador de resultados.
Implementa a metodologia de avaliação de ferramentas de merge.

METODOLOGIA:
- Gabarito: resultado do merge commit (merged.ts)
- Análise Individual: Classifica cada ferramenta em relação ao gabarito.
- Comparação Par a Par: Identifica melhorias relativas (FP/FN Adicionais).

CLASSIFICAÇÃO INDIVIDUAL (Baseada no Diagrama do TCC):
1. Clean Merge Correct (Sucesso): Ferramenta não reportou conflito E saída igual ao gabarito.
2. Clean Merge Incorrect (Erro de Merge): Ferramenta não reportou conflito MAS saída diferente do gabarito.
3. Conflict (Conflito): Ferramenta reportou conflito (correto ou não, depende da semântica, mas geralmente é aceito como "não conseguiu resolver").
4. Failure (Falha): A ferramenta quebrou/crashou.

DEFINIÇÕES PAR A PAR (Opcional para análise relativa):
- Falso Positivo Adicional (F1 sobre F2): F1 conflitou, F2 resolveu corretamente.
- Falso Negativo Adicional (F1 sobre F2): F1 resolveu incorretamente, F2 conflitou.
"""

from typing import Dict, Tuple, Literal
import logging

logger = logging.getLogger(__name__)

# Tipos de classificação individual
ToolClassification = Literal['clean_correct', 'clean_incorrect', 'conflict', 'failure']

# Tipos de comparação par a par
PairClassification = Literal['fp_adicional', 'fn_adicional', 'correto', 'indefinido']


class ComparisonClassifier:
    """
    Classificador de resultados de merge.
    """

    def __init__(self):
        """Inicializa classificador."""
        # Estatísticas para comparações par a par
        self.pair_stats = {
            'total_comparisons': 0,
            'fp_adicional': 0,
            'fn_adicional': 0,
            'corretos': 0,
            'indefinidos': 0
        }
        
        # Estatísticas individuais por ferramenta
        self.tool_stats = {}

    def classify_tool_result(
        self,
        tool_name: str,
        output: str,
        has_conflict: bool,
        repo_expected: str,
        error: str = None
    ) -> ToolClassification:
        """
        Classifica o resultado de uma ÚNICA ferramenta em relação ao gabarito.
        Segue o fluxo do diagrama padrão de avaliação.

        Args:
            tool_name: Nome da ferramenta
            output: Conteúdo gerado pela ferramenta
            has_conflict: Se houve conflito
            repo_expected: Conteúdo do gabarito (merge commit)
            error: Mensagem de erro se a ferramenta falhou

        Returns:
            Classificação: 'clean_correct' | 'clean_incorrect' | 'conflict' | 'failure'
        """
        # Inicializar stats para a ferramenta se não existir
        if tool_name not in self.tool_stats:
            self.tool_stats[tool_name] = {
                'clean_correct': 0,
                'clean_incorrect': 0,
                'conflict': 0,
                'failure': 0,
                'total': 0
            }
        
        self.tool_stats[tool_name]['total'] += 1

        # 1. Verificar Falha de Execução
        if error:
            self.tool_stats[tool_name]['failure'] += 1
            return 'failure'

        # 2. Verificar Conflito
        if has_conflict:
            # Nota: O diagrama geralmente trata qualquer conflito reportado como "Conflict"
            # independente se o gabarito tinha conflito ou não (embora o ideal seja comparar).
            # Para simplificar e seguir a prática comum: se a ferramenta parou, é conflito.
            self.tool_stats[tool_name]['conflict'] += 1
            return 'conflict'

        # 3. Verificar Clean Merge (Resolução Automática)
        # Normalizar strings (remover espaços extras para evitar falsos erros por formatação)
        output_norm = output.strip()
        expected_norm = repo_expected.strip() if repo_expected else ""

        if output_norm == expected_norm:
            self.tool_stats[tool_name]['clean_correct'] += 1
            return 'clean_correct'
        else:
            self.tool_stats[tool_name]['clean_incorrect'] += 1
            return 'clean_incorrect'

    def classify_pair_result(
        self,
        f1_output: str,
        f2_output: str,
        repo_expected: str,
        f1_has_conflict: bool,
        f2_has_conflict: bool
    ) -> PairClassification:
        """
        Classifica resultado de F1 em relação a F2 (lógica relativa).
        Útil para dizer: "Onde o Mergiraf é melhor que o Slow-diff3?".
        """
        self.pair_stats['total_comparisons'] += 1

        f1_normalized = f1_output.strip()
        f2_normalized = f2_output.strip()
        repo_normalized = repo_expected.strip()

        f1_matches_repo = (f1_normalized == repo_normalized)
        f2_matches_repo = (f2_normalized == repo_normalized)

        # CASO 1: F1 conflitou, F2 resolveu corretamente -> F1 foi pior (FP Adicional relativo)
        if f1_has_conflict and (not f2_has_conflict and f2_matches_repo):
            self.pair_stats['fp_adicional'] += 1
            return 'fp_adicional'

        # CASO 2: F1 resolveu ERRADO, F2 conflitou -> F1 foi perigoso (FN Adicional relativo)
        if (not f1_has_conflict and not f1_matches_repo) and f2_has_conflict:
            self.pair_stats['fn_adicional'] += 1
            return 'fn_adicional'

        # CASO 3: Ambos corretos
        if (not f1_has_conflict and f1_matches_repo) and (not f2_has_conflict and f2_matches_repo):
            self.pair_stats['corretos'] += 1
            return 'correto'

        # Outros casos (ambos erraram, ambos conflitaram, etc)
        self.pair_stats['indefinidos'] += 1
        return 'indefinido'

    def get_tool_statistics(self) -> Dict:
        """Retorna estatísticas individuais."""
        return self.tool_stats.copy()

    def print_statistics(self):
        """Imprime todas as estatísticas."""
        print("\n" + "=" * 60)
        print("ESTATÍSTICAS DE CLASSIFICAÇÃO (INDIVIDUAL)")
        print("=" * 60)
        
        for tool, stats in self.tool_stats.items():
            total = stats['total']
            if total == 0: continue
            
            print(f"\n[{tool.upper()}] (Total: {total})")
            print(f"  Clean Correct (Sucesso):   {stats['clean_correct']} ({stats['clean_correct']/total*100:.1f}%)")
            print(f"  Clean Incorrect (Erro):    {stats['clean_incorrect']} ({stats['clean_incorrect']/total*100:.1f}%)")
            print(f"  Conflicts (Desistência):   {stats['conflict']} ({stats['conflict']/total*100:.1f}%)")
            print(f"  Failures (Crash):          {stats['failure']} ({stats['failure']/total*100:.1f}%)")

        print("\n" + "=" * 60)
        print("ESTATÍSTICAS DE COMPARAÇÃO PAR-A-PAR (ACUMULADO)")
        print("=" * 60)
        print(f"Total comparado: {self.pair_stats['total_comparisons']}")
        print(f"FP Adicional:    {self.pair_stats['fp_adicional']}")
        print(f"FN Adicional:    {self.pair_stats['fn_adicional']}")
        print("=" * 60 + "\n")

    def reset_statistics(self):
        """Reseta todas as estatísticas."""
        self.pair_stats = {k: 0 for k in self.pair_stats}
        self.tool_stats = {}