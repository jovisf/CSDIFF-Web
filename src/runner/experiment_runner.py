"""
Orquestrador de experimentos.
Executa CSDiff-Web + mergiraf + slow-diff3 em triplas mineradas.

Este é o módulo principal do Runner. Ele:
1. Carrega triplas do diretório data/triplets/
2. Executa as 3 ferramentas em cada tripla
3. Coleta resultados e métricas
4. Gera relatórios CSV e resumos
"""

from pathlib import Path
from typing import List, Dict, Optional
from tqdm import tqdm
import logging

from .tool_executor import ToolExecutor
from .result_collector import ResultCollector

logger = logging.getLogger(__name__)


class ExperimentRunner:
    """
    Orquestrador de experimentos.

    Carrega triplas, executa ferramentas, coleta resultados.
    """

    def __init__(
        self,
        triplets_dir: Path,
        results_dir: Path,
        timeout: int = 60
    ):
        """
        Inicializa runner.

        Args:
            triplets_dir: Diretório com triplas (data/triplets/)
            results_dir: Diretório para salvar resultados
            timeout: Timeout por execução (segundos)
        """
        self.triplets_dir = Path(triplets_dir)
        self.results_dir = Path(results_dir)
        self.timeout = timeout

        # Criar diretório de resultados
        self.results_dir.mkdir(parents=True, exist_ok=True)

        # Componentes
        self.executor = ToolExecutor(timeout=timeout)
        self.collector = ResultCollector(output_dir=results_dir)

        self.stats = {
            'triplets_loaded': 0,
            'triplets_processed': 0,
            'triplets_skipped': 0
        }

    def load_triplets(self, max_triplets: Optional[int] = None) -> List[Dict]:
        """
        Carrega triplas do diretório.

        Args:
            max_triplets: Máximo de triplas a carregar (None = todas)

        Returns:
            Lista de triplas.
        """
        triplets = []

        # Listar diretórios triplet_*
        triplet_dirs = sorted(self.triplets_dir.glob("triplet_*"))

        if not triplet_dirs:
            logger.warning(f"Nenhuma tripla encontrada em {self.triplets_dir}")
            return []

        logger.info(f"Encontrados {len(triplet_dirs)} diretórios de triplas")

        # Limitar se necessário
        if max_triplets:
            triplet_dirs = triplet_dirs[:max_triplets]
            logger.info(f"Limitando a {max_triplets} triplas")

        # Carregar cada tripla
        for triplet_dir in triplet_dirs:
            try:
                triplet = self._load_single_triplet(triplet_dir)
                if triplet:
                    triplets.append(triplet)
                    self.stats['triplets_loaded'] += 1
                else:
                    self.stats['triplets_skipped'] += 1

            except Exception as e:
                logger.error(f"Erro ao carregar {triplet_dir.name}: {e}")
                self.stats['triplets_skipped'] += 1

        logger.info(f"Carregadas {len(triplets)} triplas com sucesso")
        return triplets

    def _load_single_triplet(self, triplet_dir: Path) -> Optional[Dict]:
        """
        Carrega uma única tripla.

        Args:
            triplet_dir: Path do diretório da tripla

        Returns:
            Dict com dados da tripla, ou None se erro
        """
        # Procurar arquivos base, left, right, merged
        # Podem ter extensões diferentes (.ts, .tsx, .js, .jsx)
        base_files = list(triplet_dir.glob("base.*"))
        left_files = list(triplet_dir.glob("left.*"))
        right_files = list(triplet_dir.glob("right.*"))
        merged_files = list(triplet_dir.glob("merged.*"))

        if not base_files or not left_files or not right_files:
            logger.warning(f"{triplet_dir.name}: arquivos incompletos")
            return None

        base_file = base_files[0]
        left_file = left_files[0]
        right_file = right_files[0]
        merged_file = merged_files[0] if merged_files else None

        # Extensão
        extension = base_file.suffix

        # Carregar conteúdos (base, left, right, merged)
        try:
            base_content = base_file.read_text(encoding='utf-8')
            left_content = left_file.read_text(encoding='utf-8')
            right_content = right_file.read_text(encoding='utf-8')

            # Carregar merged se existir (GABARITO)
            merged_content = None
            if merged_file and merged_file.exists():
                merged_content = merged_file.read_text(encoding='utf-8')
            else:
                logger.warning(f"{triplet_dir.name}: arquivo merged não encontrado (tripla antiga)")
        except Exception as e:
            logger.error(f"Erro ao ler arquivos de {triplet_dir.name}: {e}")
            return None

        # Carregar metadata se existir
        metadata = {}
        metadata_file = triplet_dir / "metadata.txt"
        if metadata_file.exists():
            metadata = self._parse_metadata(metadata_file)

        return {
            'id': triplet_dir.name,
            'dir': triplet_dir,
            'metadata': metadata,
            'base': base_content,
            'left': left_content,
            'right': right_content,
            'merged': merged_content,  # GABARITO (resultado real do merge)
            'extension': extension,
            'filepath': metadata.get('Original File', ''),
            'base_file': base_file,
            'left_file': left_file,
            'right_file': right_file,
            'merged_file': merged_file
        }

    def _parse_metadata(self, metadata_file: Path) -> Dict:
        """
        Parse arquivo metadata.txt.
        """
        metadata = {}
        try:
            lines = metadata_file.read_text(encoding='utf-8').split('\n')
            for line in lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip()
        except Exception as e:
            logger.warning(f"Erro ao parsear metadata: {e}")
        return metadata

    def run_experiments(
        self,
        max_triplets: Optional[int] = None
    ) -> Dict:
        """
        Executa experimentos em triplas.

        Args:
            max_triplets: Máximo de triplas a processar (None = todas)

        Returns:
            Dict com resultados.
        """

        # Carregar triplas
        logger.info("Carregando triplas...")
        triplets = self.load_triplets(max_triplets=max_triplets)

        if not triplets:
            logger.error("Nenhuma tripla para processar")
            return {
                'triplets_processed': 0,
                'csv_path': None,
                'summary_path': None,
                'metrics': {}
            }

        # Processar cada tripla
        logger.info(f"Processando {len(triplets)} triplas...")

        for triplet in tqdm(triplets, desc="Executando experimentos"):
            try:
                self._process_single_triplet(triplet)
                self.stats['triplets_processed'] += 1

            except Exception as e:
                logger.error(f"Erro ao processar {triplet['id']}: {e}")

        # Gerar relatórios
        logger.info("Gerando relatórios...")
        csv_path = self.collector.generate_csv()
        summary_path = self.collector.generate_summary()
        metrics = self.collector.calculate_metrics()

        logger.info(f"✓ Experimentos concluídos!")
        logger.info(f"  CSV:     {csv_path}")
        logger.info(f"  Resumo:  {summary_path}")

        return {
            'triplets_processed': self.stats['triplets_processed'],
            'csv_path': csv_path,
            'summary_path': summary_path,
            'metrics': metrics
        }

    def _process_single_triplet(self, triplet: Dict):
        """
        Processa uma única tripla com todas as ferramentas.

        Args:
            triplet: Dict com dados da tripla
        """
        # Executar ferramentas (CSDiff, Mergiraf, Slow-diff3)
        tool_results = self.executor.execute_all(
            base=triplet['base'],
            left=triplet['left'],
            right=triplet['right'],
            extension=triplet['extension'],
            filename=triplet['filepath'],
            base_file=triplet.get('base_file'),
            left_file=triplet.get('left_file'),
            right_file=triplet.get('right_file')
        )

        # Coletar resultados (incluindo merged content como gabarito)
        self.collector.add_result(
            triplet_id=triplet['id'],
            triplet_metadata=triplet['metadata'],
            tool_results=tool_results,
            merged_content=triplet.get('merged')  # GABARITO
        )

    def get_statistics(self) -> Dict:
        """Retorna estatísticas globais."""
        return {
            **self.stats,
            'executor': self.executor.get_statistics(),
            'collector': self.collector.get_statistics()
        }

    def print_statistics(self):
        """Imprime estatísticas consolidadas."""
        print("\n" + "=" * 60)
        print("ESTATÍSTICAS DO RUNNER")
        print("=" * 60)
        print(f"Triplas carregadas:   {self.stats['triplets_loaded']}")
        print(f"Triplas processadas:  {self.stats['triplets_processed']}")
        print(f"Triplas puladas:      {self.stats['triplets_skipped']}")
        print("=" * 60)

        self.executor.print_statistics()
        self.collector.print_statistics()