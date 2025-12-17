"""
Executor de ferramentas de merge.
Executa CSDiff-Web, slow-diff3 e MERGIRAF.
"""

import subprocess
import time
import tempfile
from pathlib import Path
from typing import Dict, Optional
import logging
import sys

# Adicionar raiz ao path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from src.core.csdiff_web import CSDiffWeb

logger = logging.getLogger(__name__)

class ToolExecutor:
    def __init__(self, timeout: int = 60):
        self.timeout = timeout
        self.stats = {
            'csdiff_executions': 0, 'slow_diff3_executions': 0, 'mergiraf_executions': 0,
            'csdiff_errors': 0, 'slow_diff3_errors': 0, 'mergiraf_errors': 0,
        }

    def execute_csdiff_web(self, base, left, right, extension, filename="") -> Dict:
        self.stats['csdiff_executions'] += 1
        start_time = time.time()
        try:
            csdiff = CSDiffWeb(extension)
            # Correção para unpacking: aceita 2 ou 3 valores de retorno
            ret = csdiff.merge(base, left, right, filename)
            
            if isinstance(ret, tuple) and len(ret) == 3:
                result, has_conflict, num_conflicts = ret
            elif isinstance(ret, tuple) and len(ret) == 2:
                result, has_conflict = ret
                num_conflicts = result.count("<<<<<<<") if result else 0
            else:
                result = str(ret)
                num_conflicts = result.count("<<<<<<<")
                has_conflict = num_conflicts > 0

            return {
                'tool': 'csdiff-web', 'success': True, 'has_conflict': has_conflict,
                'num_conflicts': num_conflicts, 'result': result,
                'execution_time': time.time() - start_time
            }
        except Exception as e:
            self.stats['csdiff_errors'] += 1
            return {
                'tool': 'csdiff-web', 'success': False,
                'execution_time': time.time() - start_time, 'error': str(e)
            }

    def execute_mergiraf(self, base, left, right) -> Dict:
        self.stats['mergiraf_executions'] += 1
        start_time = time.time()
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                p_base = Path(tmpdir)/"base"; p_base.write_text(base, encoding='utf-8')
                p_left = Path(tmpdir)/"left"; p_left.write_text(left, encoding='utf-8')
                p_right = Path(tmpdir)/"right"; p_right.write_text(right, encoding='utf-8')

                proc = subprocess.run(
                    ["mergiraf", "merge", str(p_base), str(p_left), str(p_right)],
                    capture_output=True, text=True, timeout=self.timeout, encoding='utf-8'
                )
                
                result = proc.stdout
                return {
                    'tool': 'mergiraf', 'success': True,
                    'has_conflict': "<<<<<<<" in result,
                    'num_conflicts': result.count("<<<<<<<"), 'result': result,
                    'execution_time': time.time() - start_time
                }
        except Exception as e:
            self.stats['mergiraf_errors'] += 1
            return {
                'tool': 'mergiraf', 'success': False,
                'execution_time': time.time() - start_time, 'error': str(e)
            }

    def execute_slow_diff3(self, base_file, left_file, right_file, script_path="./slow-diff3/src/index.js") -> Dict:
        self.stats['slow_diff3_executions'] += 1
        start_time = time.time()
        try:
            # Aumentar stack size para evitar estouro de pilha
            cmd = ["node", "--stack-size=8192", script_path, str(left_file), str(base_file), str(right_file), "-m"]
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=self.timeout, encoding='utf-8')
            
            if proc.returncode != 0 and not proc.stdout:
                raise RuntimeError(f"Stderr: {proc.stderr}")

            result = proc.stdout
            return {
                'tool': 'slow-diff3', 'success': True,
                'has_conflict': "<<<<<<<" in result,
                'num_conflicts': result.count("<<<<<<<"), 'result': result,
                'execution_time': time.time() - start_time
            }
        except Exception as e:
            self.stats['slow_diff3_errors'] += 1
            return {
                'tool': 'slow-diff3', 'success': False,
                'execution_time': time.time() - start_time, 'error': str(e)
            }

    def execute_all(self, base, left, right, extension, filename="", base_file=None, left_file=None, right_file=None):
        return {
            'csdiff-web': self.execute_csdiff_web(base, left, right, extension, filename),
            'mergiraf': self.execute_mergiraf(base, left, right),
            'slow-diff3': self.execute_slow_diff3(base_file, left_file, right_file) if base_file else {'success': False, 'error': 'No files'}
        }

    def get_statistics(self): return self.stats.copy()
    def print_statistics(self): pass