"""
Executor de ferramentas de merge.
Executa CSDiff-Web, diff3 e Mergiraf em triplas.

Este módulo é responsável por:
1. Executar cada ferramenta em uma tripla
2. Capturar saída, tempo de execução e status
3. Detectar conflitos e erros
4. Retornar resultados padronizados
"""

import subprocess
import time
from pathlib import Path
from typing import Dict, Tuple, Optional
import logging

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.csdiff_web import CSDiffWeb

logger = logging.getLogger(__name__)


class ToolExecutor:
    """
    Executor de ferramentas de merge.

    Suporta:
    - CSDiff-Web (Python nativo)
    - diff3 (subprocess)
    - Mergiraf (subprocess, se disponível)
    """

    def __init__(self, timeout: int = 60):
        """
        Inicializa executor.

        Args:
            timeout: Timeout em segundos para cada execução (padrão: 60s)
        """
        self.timeout = timeout
        self.stats = {
            'csdiff_executions': 0,
            'diff3_executions': 0,
            'mergiraf_executions': 0,
            'csdiff_errors': 0,
            'diff3_errors': 0,
            'mergiraf_errors': 0,
        }

    def execute_csdiff_web(
        self,
        base: str,
        left: str,
        right: str,
        extension: str,
        filename: str = ""
    ) -> Dict:
        """
        Executa CSDiff-Web em uma tripla.

        Args:
            base: Conteúdo base
            left: Conteúdo left
            right: Conteúdo right
            extension: Extensão do arquivo (.ts, .tsx, etc)
            filename: Nome do arquivo (opcional)

        Returns:
            Dict com resultados:
            {
                'tool': 'csdiff-web',
                'success': bool,
                'has_conflict': bool,
                'num_conflicts': int,
                'result': str,
                'execution_time': float,
                'error': str (se houver)
            }
        """
        self.stats['csdiff_executions'] += 1

        start_time = time.time()

        try:
            # Criar instância do CSDiff-Web
            csdiff = CSDiffWeb(extension)

            # Executar merge
            result, has_conflict, num_conflicts = csdiff.merge(
                base, left, right, filename
            )

            execution_time = time.time() - start_time

            return {
                'tool': 'csdiff-web',
                'success': True,
                'has_conflict': has_conflict,
                'num_conflicts': num_conflicts,
                'result': result,
                'execution_time': execution_time,
                'error': None
            }

        except Exception as e:
            self.stats['csdiff_errors'] += 1
            execution_time = time.time() - start_time

            logger.error(f"Erro ao executar CSDiff-Web: {e}")

            return {
                'tool': 'csdiff-web',
                'success': False,
                'has_conflict': None,
                'num_conflicts': None,
                'result': None,
                'execution_time': execution_time,
                'error': str(e)
            }

    def execute_diff3(
        self,
        base: str,
        left: str,
        right: str
    ) -> Dict:
        """
        Executa diff3 puro em uma tripla.

        Args:
            base: Conteúdo base
            left: Conteúdo left
            right: Conteúdo right

        Returns:
            Dict com resultados (mesmo formato que execute_csdiff_web)
        """
        self.stats['diff3_executions'] += 1

        start_time = time.time()

        try:
            import tempfile

            # Criar arquivos temporários
            with tempfile.TemporaryDirectory() as tmpdir:
                base_file = Path(tmpdir) / "base"
                left_file = Path(tmpdir) / "left"
                right_file = Path(tmpdir) / "right"

                base_file.write_text(base, encoding='utf-8')
                left_file.write_text(left, encoding='utf-8')
                right_file.write_text(right, encoding='utf-8')

                # Executar diff3
                proc = subprocess.run(
                    ["diff3", "-m", str(left_file), str(base_file), str(right_file)],
                    capture_output=True,
                    text=True,
                    timeout=self.timeout,
                    encoding='utf-8'
                )

                execution_time = time.time() - start_time

                # diff3 retorna 0 se sem conflitos, 1 se com conflitos
                has_conflict = proc.returncode != 0
                result = proc.stdout if proc.stdout else proc.stderr
                num_conflicts = result.count("<<<<<<<")

                return {
                    'tool': 'diff3',
                    'success': True,
                    'has_conflict': has_conflict,
                    'num_conflicts': num_conflicts,
                    'result': result,
                    'execution_time': execution_time,
                    'error': None
                }

        except subprocess.TimeoutExpired:
            self.stats['diff3_errors'] += 1
            execution_time = time.time() - start_time

            logger.error(f"diff3 excedeu timeout de {self.timeout}s")

            return {
                'tool': 'diff3',
                'success': False,
                'has_conflict': None,
                'num_conflicts': None,
                'result': None,
                'execution_time': execution_time,
                'error': f'Timeout ({self.timeout}s)'
            }

        except Exception as e:
            self.stats['diff3_errors'] += 1
            execution_time = time.time() - start_time

            logger.error(f"Erro ao executar diff3: {e}")

            return {
                'tool': 'diff3',
                'success': False,
                'has_conflict': None,
                'num_conflicts': None,
                'result': None,
                'execution_time': execution_time,
                'error': str(e)
            }

    def execute_mergiraf(
        self,
        base_file: Path,
        left_file: Path,
        right_file: Path
    ) -> Dict:
        """
        Executa Mergiraf em uma tripla.

        NOTA: Mergiraf requer arquivos no disco (não strings).

        Args:
            base_file: Path para arquivo base
            left_file: Path para arquivo left
            right_file: Path para arquivo right

        Returns:
            Dict com resultados (mesmo formato)
        """
        self.stats['mergiraf_executions'] += 1

        start_time = time.time()

        try:
            # Verificar se Mergiraf está instalado
            check = subprocess.run(
                ["mergiraf", "--version"],
                capture_output=True,
                timeout=5
            )

            if check.returncode != 0:
                raise FileNotFoundError("Mergiraf não encontrado no PATH")

            # Executar Mergiraf
            # Formato: mergiraf <base> <left> <right>
            proc = subprocess.run(
                ["mergiraf", str(base_file), str(left_file), str(right_file)],
                capture_output=True,
                text=True,
                timeout=self.timeout,
                encoding='utf-8'
            )

            execution_time = time.time() - start_time

            # Mergiraf retorna resultado em stdout
            result = proc.stdout

            # Detectar conflitos (Mergiraf usa marcadores similares)
            has_conflict = "<<<<<<<" in result or "CONFLICT" in result
            num_conflicts = result.count("<<<<<<<")

            return {
                'tool': 'mergiraf',
                'success': True,
                'has_conflict': has_conflict,
                'num_conflicts': num_conflicts,
                'result': result,
                'execution_time': execution_time,
                'error': None
            }

        except FileNotFoundError as e:
            self.stats['mergiraf_errors'] += 1
            execution_time = time.time() - start_time

            logger.warning("Mergiraf não disponível - pulando")

            return {
                'tool': 'mergiraf',
                'success': False,
                'has_conflict': None,
                'num_conflicts': None,
                'result': None,
                'execution_time': execution_time,
                'error': 'Mergiraf não instalado'
            }

        except subprocess.TimeoutExpired:
            self.stats['mergiraf_errors'] += 1
            execution_time = time.time() - start_time

            logger.error(f"Mergiraf excedeu timeout de {self.timeout}s")

            return {
                'tool': 'mergiraf',
                'success': False,
                'has_conflict': None,
                'num_conflicts': None,
                'result': None,
                'execution_time': execution_time,
                'error': f'Timeout ({self.timeout}s)'
            }

        except Exception as e:
            self.stats['mergiraf_errors'] += 1
            execution_time = time.time() - start_time

            logger.error(f"Erro ao executar Mergiraf: {e}")

            return {
                'tool': 'mergiraf',
                'success': False,
                'has_conflict': None,
                'num_conflicts': None,
                'result': None,
                'execution_time': execution_time,
                'error': str(e)
            }

    def execute_all(
        self,
        base: str,
        left: str,
        right: str,
        extension: str,
        filename: str = "",
        base_file: Optional[Path] = None,
        left_file: Optional[Path] = None,
        right_file: Optional[Path] = None
    ) -> Dict[str, Dict]:
        """
        Executa todas as ferramentas em uma tripla.

        Args:
            base, left, right: Conteúdos
            extension: Extensão do arquivo
            filename: Nome do arquivo
            base_file, left_file, right_file: Paths (para Mergiraf)

        Returns:
            Dict mapeando ferramenta → resultado:
            {
                'csdiff-web': {...},
                'diff3': {...},
                'mergiraf': {...}
            }
        """
        results = {}

        # Executar CSDiff-Web
        logger.info("Executando CSDiff-Web...")
        results['csdiff-web'] = self.execute_csdiff_web(
            base, left, right, extension, filename
        )

        # Executar diff3
        logger.info("Executando diff3...")
        results['diff3'] = self.execute_diff3(base, left, right)

        # Executar Mergiraf (se arquivos fornecidos)
        if base_file and left_file and right_file:
            logger.info("Executando Mergiraf...")
            results['mergiraf'] = self.execute_mergiraf(
                base_file, left_file, right_file
            )
        else:
            logger.info("Mergiraf pulado (arquivos não fornecidos)")
            results['mergiraf'] = {
                'tool': 'mergiraf',
                'success': False,
                'error': 'Arquivos não fornecidos'
            }

        return results

    def get_statistics(self) -> Dict:
        """Retorna estatísticas de execuções."""
        return self.stats.copy()

    def print_statistics(self):
        """Imprime estatísticas formatadas."""
        print("\n" + "=" * 60)
        print("ESTATÍSTICAS DO EXECUTOR")
        print("=" * 60)
        print(f"CSDiff-Web:")
        print(f"  Execuções: {self.stats['csdiff_executions']}")
        print(f"  Erros:     {self.stats['csdiff_errors']}")
        print(f"\ndiff3:")
        print(f"  Execuções: {self.stats['diff3_executions']}")
        print(f"  Erros:     {self.stats['diff3_errors']}")
        print(f"\nMergiraf:")
        print(f"  Execuções: {self.stats['mergiraf_executions']}")
        print(f"  Erros:     {self.stats['mergiraf_errors']}")
        print("=" * 60 + "\n")
