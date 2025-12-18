"""
Extrator de triplas (base, left, right) de merge commits.
Seção 3.2 do Plano Técnico.

Este módulo extrai as três versões de cada arquivo modificado em um merge:
- BASE: versão do ancestral comum
- LEFT: versão do primeiro pai do merge
- RIGHT: versão do segundo pai do merge

CRITÉRIO DE SELEÇÃO:
Apenas arquivos modificados por AMBOS os pais (mudanças conflitantes potenciais)
"""

from git import Repo, Commit
from pathlib import Path
from typing import List, Dict, Set, Optional
import logging

logger = logging.getLogger(__name__)


class TripletExtractor:
    """
    Extrai triplas de arquivos modificados em merge commits.

    Uma tripla válida contém:
    - Arquivo com extensão suportada (.ts, .tsx, .js, .jsx)
    - Modificado em AMBOS os pais do merge (não apenas em um)
    - Presente nas três versões (base, left, right)
    """

    VALID_EXTENSIONS = {'.ts', '.tsx', '.js', '.jsx'}

    def __init__(self, output_dir: Path):
        """
        Inicializa extrator.

        Args:
            output_dir: Diretório onde triplas serão salvas
        """
        self.output_dir = Path(output_dir)
        self.stats = {
            'total_files': 0,
            'unsupported_extension': 0,
            'modified_one_side_only': 0,
            'file_not_in_all_versions': 0,
            'extraction_errors': 0,
            'valid_triplets': 0
        }

    def get_modified_files(
        self,
        repo: Repo,
        base: Commit,
        target: Commit
    ) -> Set[str]:
        """
        Retorna conjunto de arquivos modificados entre dois commits.

        Args:
            repo: Repositório Git
            base: Commit base
            target: Commit alvo

        Returns:
            Set com caminhos dos arquivos modificados

        Examples:
            >>> extractor = TripletExtractor(Path('/tmp'))
            >>> files = extractor.get_modified_files(repo, base, left)
            >>> isinstance(files, set)
            True
        """
        try:
            # Diff entre base e target
            diffs = base.diff(target)

            modified_files = set()
            for diff in diffs:
                # Pegar caminho do arquivo (a_path ou b_path dependendo do tipo)
                if diff.a_path:
                    modified_files.add(diff.a_path)
                if diff.b_path and diff.b_path != diff.a_path:
                    modified_files.add(diff.b_path)

            return modified_files

        except Exception as e:
            logger.error(f"Erro ao buscar arquivos modificados: {e}")
            return set()

    def is_supported_file(self, filepath: str) -> bool:
        """
        Verifica se arquivo tem extensão suportada.

        Args:
            filepath: Caminho do arquivo

        Returns:
            True se extensão é suportada

        Examples:
            >>> extractor = TripletExtractor(Path('/tmp'))
            >>> extractor.is_supported_file("src/index.ts")
            True
            >>> extractor.is_supported_file("README.md")
            False
        """
        extension = Path(filepath).suffix.lower()
        return extension in self.VALID_EXTENSIONS

    def extract_file_content(
        self,
        commit: Commit,
        filepath: str
    ) -> Optional[str]:
        """
        Extrai conteúdo de um arquivo em um commit específico.

        Args:
            commit: Commit do qual extrair o arquivo
            filepath: Caminho do arquivo

        Returns:
            Conteúdo do arquivo como string, ou None se não existir

        Examples:
            >>> extractor = TripletExtractor(Path('/tmp'))
            >>> content = extractor.extract_file_content(commit, "src/index.ts")
            >>> content is not None
            True
        """
        try:
            # Tentar obter blob do arquivo no commit
            blob = commit.tree / filepath

            # Decodificar conteúdo
            content = blob.data_stream.read().decode('utf-8', errors='ignore')
            return content

        except KeyError:
            # Arquivo não existe neste commit
            logger.debug(f"Arquivo {filepath} não existe em {commit.hexsha[:8]}")
            return None
        except Exception as e:
            logger.error(f"Erro ao extrair {filepath} de {commit.hexsha[:8]}: {e}")
            return None

    def extract_triplet(
        self,
        repo: Repo,
        merge_info: Dict
    ) -> List[Dict]:
        """
        Extrai triplas de um merge commit.

        Args:
            repo: Repositório Git
            merge_info: Dict com keys 'commit', 'base', 'left', 'right'

        Returns:
            Lista de triplas extraídas, cada uma um dict com:
            {
                'filepath': str,
                'extension': str,
                'base_content': str,
                'left_content': str,
                'right_content': str,
                'merged_content': str, 
                'commit_sha': str
            }

        Examples:
            >>> extractor = TripletExtractor(Path('/tmp'))
            >>> triplets = extractor.extract_triplet(repo, merge_info)
            >>> all('base_content' in t for t in triplets)
            True
        """
        base = merge_info['base']
        left = merge_info['left']
        right = merge_info['right']
        commit = merge_info['commit']

        # Encontrar arquivos modificados em cada lado
        files_left = self.get_modified_files(repo, base, left)
        files_right = self.get_modified_files(repo, base, right)

        # Interseção: arquivos modificados por AMBOS os lados
        files_both = files_left.intersection(files_right)

        logger.info(
            f"Merge {commit.hexsha[:8]}: "
            f"{len(files_left)} arquivos em left, "
            f"{len(files_right)} em right, "
            f"{len(files_both)} em ambos"
        )

        triplets = []

        for filepath in files_both:
            self.stats['total_files'] += 1

            # Filtro 1: Extensão suportada
            if not self.is_supported_file(filepath):
                self.stats['unsupported_extension'] += 1
                logger.debug(f"Ignorando {filepath}: extensão não suportada")
                continue

            # Extrair conteúdo das quatro versões (base, left, right, merged)
            base_content = self.extract_file_content(base, filepath)
            left_content = self.extract_file_content(left, filepath)
            right_content = self.extract_file_content(right, filepath)
            merged_content = self.extract_file_content(commit, filepath)  # GABARITO

            # Filtro 2: Arquivo deve existir em todas as versões (incluindo merge result)
            if base_content is None or left_content is None or right_content is None or merged_content is None:
                self.stats['file_not_in_all_versions'] += 1
                logger.debug(
                    f"Ignorando {filepath}: não existe em todas as versões "
                    f"(base={base_content is not None}, "
                    f"left={left_content is not None}, "
                    f"right={right_content is not None}, "
                    f"merged={merged_content is not None})"
                )
                continue

            # Tripla válida!
            extension = Path(filepath).suffix.lower()
            triplet = {
                'filepath': filepath,
                'extension': extension,
                'base_content': base_content,
                'left_content': left_content,
                'right_content': right_content,
                'merged_content': merged_content,  # GABARITO (resultado real do merge)
                'commit_sha': commit.hexsha,
                'base_sha': base.hexsha,
                'left_sha': left.hexsha,
                'right_sha': right.hexsha
            }

            triplets.append(triplet)
            self.stats['valid_triplets'] += 1

            logger.info(
                f"✓ Tripla extraída: {filepath} "
                f"({len(base_content)} / {len(left_content)} / {len(right_content)} / {len(merged_content)} bytes)"
            )

        return triplets

    def save_triplet(
        self,
        triplet: Dict,
        triplet_id: int
    ) -> Path:
        """
        Salva tripla em arquivos no disco.

        Estrutura:
        output_dir/
          triplet_001/
            base.ts
            left.ts
            right.ts
            merged.ts      # ⭐ GABARITO (resultado real do merge)
            metadata.txt

        Args:
            triplet: Dict com conteúdos da tripla
            triplet_id: ID numérico da tripla

        Returns:
            Path do diretório da tripla

        Examples:
            >>> extractor = TripletExtractor(Path('/tmp/triplets'))
            >>> dir_path = extractor.save_triplet(triplet, 1)
            >>> dir_path.exists()
            True
        """
        # Criar diretório da tripla
        triplet_dir = self.output_dir / f"triplet_{triplet_id:03d}"
        triplet_dir.mkdir(parents=True, exist_ok=True)

        # Nome base do arquivo (preservar extensão)
        extension = triplet['extension']

        # Salvar quatro versões (base, left, right, merged)
        (triplet_dir / f"base{extension}").write_text(
            triplet['base_content'], encoding='utf-8'
        )
        (triplet_dir / f"left{extension}").write_text(
            triplet['left_content'], encoding='utf-8'
        )
        (triplet_dir / f"right{extension}").write_text(
            triplet['right_content'], encoding='utf-8'
        )
        (triplet_dir / f"merged{extension}").write_text(
            triplet['merged_content'], encoding='utf-8'
        )

        # Salvar metadados
        metadata = f"""Triplet ID: {triplet_id}
Original File: {triplet['filepath']}
Extension: {triplet['extension']}
Commit SHA: {triplet['commit_sha']}
Base SHA: {triplet['base_sha']}
Left SHA: {triplet['left_sha']}
Right SHA: {triplet['right_sha']}

File Sizes:
  Base:   {len(triplet['base_content'])} bytes
  Left:   {len(triplet['left_content'])} bytes
  Right:  {len(triplet['right_content'])} bytes
  Merged: {len(triplet['merged_content'])} bytes (GABARITO)
"""
        (triplet_dir / "metadata.txt").write_text(metadata, encoding='utf-8')

        logger.info(f"Tripla salva em: {triplet_dir}")
        return triplet_dir

    def get_statistics(self) -> Dict:
        """Retorna estatísticas do extrator."""
        return self.stats.copy()

    def print_statistics(self):
        """Imprime estatísticas formatadas."""
        print("\n" + "=" * 60)
        print("ESTATÍSTICAS DO EXTRATOR DE TRIPLAS")
        print("=" * 60)
        print(f"Total de arquivos analisados: {self.stats['total_files']}")
        print(f"  └─ Extensão não suportada:   {self.stats['unsupported_extension']}")
        print(f"  └─ Modificado em só um lado: {self.stats['modified_one_side_only']}")
        print(f"  └─ Ausente em alguma versão: {self.stats['file_not_in_all_versions']}")
        print(f"  └─ Erros de extração:        {self.stats['extraction_errors']}")
        print(f"\n✓ TRIPLAS VÁLIDAS:             {self.stats['valid_triplets']}")
        print("=" * 60)

        if self.stats['total_files'] > 0:
            success_rate = (self.stats['valid_triplets'] /
                          self.stats['total_files'] * 100)
            print(f"Taxa de aprovação: {success_rate:.1f}%")
        print()
