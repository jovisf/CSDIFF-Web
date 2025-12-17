"""
Classificador de resultados por comparação par a par.
Implementa a metodologia correta usando merge commit como gabarito.

METODOLOGIA:
- Gabarito: resultado do merge commit (merged.ts)
- Comparação: Pares ordenados de ferramentas (F1, F2)
- Classificação: Falsos Positivos Adicionais e Falsos Negativos Adicionais

DEFINIÇÕES:
- Falso Positivo Adicional (F1 sobre F2): F1 reportou conflito, mas F2 integrou
  corretamente (F2 = resultado do repo)
- Falso Negativo Adicional (F1 sobre F2): F1 não reportou conflito, mas produziu
  resultado incorreto (F1 ≠ repo), enquanto F2 reportou conflito
- Correto: Sem conflito E resultado = repo
- Indefinido: Ambos com conflito, ou ambos incorretos
"""

from typing import Dict, Tuple, Literal
import logging

logger = logging.getLogger(__name__)

ClassificationType = Literal['fp_adicional', 'fn_adicional', 'correto', 'indefinido']


class ComparisonClassifier:
    """
    Classificador de resultados usando comparação par a par.

    Usa o merge commit real como gabarito ao invés de uma ferramenta baseline.
    """

    def __init__(self):
        """Inicializa classificador."""
        self.stats = {
            'total_comparisons': 0,
            'fp_adicional': 0,
            'fn_adicional': 0,
            'corretos': 0,
            'indefinidos': 0
        }

    def classify_result(
        self,
        f1_output: str,
        f2_output: str,
        repo_expected: str,
        f1_has_conflict: bool,
        f2_has_conflict: bool
    ) -> ClassificationType:
        """
        Classifica resultado de F1 em relação a F2 usando repo como gabarito.

        Args:
            f1_output: Saída da ferramenta 1 (merged text)
            f2_output: Saída da ferramenta 2 (merged text)
            repo_expected: Resultado esperado do repositório (GABARITO)
            f1_has_conflict: Se F1 reportou conflito
            f2_has_conflict: Se F2 reportou conflito

        Returns:
            Classificação: 'fp_adicional' | 'fn_adicional' | 'correto' | 'indefinido'

        Examples:
            >>> classifier = ComparisonClassifier()
            >>> result = classifier.classify_result(
            ...     f1_output="code with conflicts",
            ...     f2_output="merged code",
            ...     repo_expected="merged code",
            ...     f1_has_conflict=True,
            ...     f2_has_conflict=False
            ... )
            >>> result
            'fp_adicional'
        """
        self.stats['total_comparisons'] += 1

        # Normalizar strings para comparação (remover espaços em branco)
        f1_normalized = f1_output.strip()
        f2_normalized = f2_output.strip()
        repo_normalized = repo_expected.strip()

        # Verificar se resultados batem com o gabarito
        f1_matches_repo = (f1_normalized == repo_normalized)
        f2_matches_repo = (f2_normalized == repo_normalized)

        # CASO 1: F1 reportou conflito, F2 não reportou conflito
        if f1_has_conflict and not f2_has_conflict:
            # Se F2 acertou (F2 = repo), então F1 é um Falso Positivo Adicional
            if f2_matches_repo:
                self.stats['fp_adicional'] += 1
                return 'fp_adicional'
            else:
                # F2 também errou, indefinido
                self.stats['indefinidos'] += 1
                return 'indefinido'

        # CASO 2: F1 não reportou conflito, F2 reportou conflito
        if not f1_has_conflict and f2_has_conflict:
            # Se F1 errou (F1 ≠ repo), então F1 é um Falso Negativo Adicional
            if not f1_matches_repo:
                self.stats['fn_adicional'] += 1
                return 'fn_adicional'
            else:
                # F1 acertou, então F2 que é FP
                self.stats['indefinidos'] += 1
                return 'indefinido'

        # CASO 3: Ambos não reportaram conflito
        if not f1_has_conflict and not f2_has_conflict:
            # Se ambos acertaram
            if f1_matches_repo and f2_matches_repo:
                self.stats['corretos'] += 1
                return 'correto'
            else:
                # Pelo menos um errou
                self.stats['indefinidos'] += 1
                return 'indefinido'

        # CASO 4: Ambos reportaram conflito - indefinido
        self.stats['indefinidos'] += 1
        return 'indefinido'

    def classify_pair(
        self,
        f1_name: str,
        f2_name: str,
        f1_data: Dict,
        f2_data: Dict,
        repo_expected: str
    ) -> Tuple[ClassificationType, Dict]:
        """
        Classifica par de ferramentas com dados completos.

        Args:
            f1_name: Nome da ferramenta 1 (ex: 'csdiff-web')
            f2_name: Nome da ferramenta 2 (ex: 'diff3')
            f1_data: Dict com 'output' e 'has_conflict' da ferramenta 1
            f2_data: Dict com 'output' e 'has_conflict' da ferramenta 2
            repo_expected: Resultado esperado do repositório

        Returns:
            Tupla (classificacao, detalhes)

        Examples:
            >>> classifier = ComparisonClassifier()
            >>> classification, details = classifier.classify_pair(
            ...     'csdiff-web', 'diff3',
            ...     {'output': 'merged', 'has_conflict': False},
            ...     {'output': 'conflicts', 'has_conflict': True},
            ...     'merged'
            ... )
            >>> classification
            'correto'
        """
        classification = self.classify_result(
            f1_output=f1_data['output'],
            f2_output=f2_data['output'],
            repo_expected=repo_expected,
            f1_has_conflict=f1_data['has_conflict'],
            f2_has_conflict=f2_data['has_conflict']
        )

        details = {
            'pair': f"{f1_name} vs {f2_name}",
            'f1_name': f1_name,
            'f2_name': f2_name,
            'f1_has_conflict': f1_data['has_conflict'],
            'f2_has_conflict': f2_data['has_conflict'],
            'f1_matches_repo': (f1_data['output'].strip() == repo_expected.strip()),
            'f2_matches_repo': (f2_data['output'].strip() == repo_expected.strip()),
            'classification': classification
        }

        return classification, details

    def get_statistics(self) -> Dict:
        """
        Retorna estatísticas acumuladas.

        Returns:
            Dict com contadores de classificações
        """
        return self.stats.copy()

    def print_statistics(self, pair_name: str = ""):
        """
        Imprime estatísticas formatadas.

        Args:
            pair_name: Nome do par (ex: "CSDiff-Web vs diff3")
        """
        print("\n" + "=" * 60)
        if pair_name:
            print(f"ESTATÍSTICAS: {pair_name}")
        else:
            print("ESTATÍSTICAS DE CLASSIFICAÇÃO")
        print("=" * 60)
        print(f"Total de comparações:      {self.stats['total_comparisons']}")
        print(f"Falsos Positivos Adicionais: {self.stats['fp_adicional']}")
        print(f"Falsos Negativos Adicionais: {self.stats['fn_adicional']}")
        print(f"Corretos:                   {self.stats['corretos']}")
        print(f"Indefinidos:                {self.stats['indefinidos']}")
        print("=" * 60)

        # Calcular taxas
        if self.stats['total_comparisons'] > 0:
            total = self.stats['total_comparisons']
            print(f"\nTaxas:")
            print(f"  FP Adicional: {self.stats['fp_adicional'] / total * 100:.1f}%")
            print(f"  FN Adicional: {self.stats['fn_adicional'] / total * 100:.1f}%")
            print(f"  Correto:      {self.stats['corretos'] / total * 100:.1f}%")
            print(f"  Indefinido:   {self.stats['indefinidos'] / total * 100:.1f}%")
        print()

    def reset_statistics(self):
        """Reseta estatísticas."""
        self.stats = {
            'total_comparisons': 0,
            'fp_adicional': 0,
            'fn_adicional': 0,
            'corretos': 0,
            'indefinidos': 0
        }
