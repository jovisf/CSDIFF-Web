from dataclasses import dataclass, field
from typing import List

@dataclass(kw_only=True)
class CodeBlock:
    lines: List[str]
    is_conflict: bool = False

@dataclass(kw_only=True)
class NormalBlock(CodeBlock):
    pass

@dataclass(kw_only=True)
class ConflictBlock(CodeBlock):
    left_lines: List[str]
    base_lines: List[str]
    right_lines: List[str]
    is_conflict: bool = True

class Diff3Parser:
    """
    Equivalente ao CodeBlocksReader.java do SepMerge.
    Lê a saída bruta do diff3 e quebra em blocos.
    """
    
    @staticmethod
    def parse(lines: List[str]) -> List[CodeBlock]:
        blocks = []
        current_lines = []
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            if line.startswith("<<<<<<<"):
                # Se tínhamos linhas normais acumuladas, salva elas
                if current_lines:
                    blocks.append(NormalBlock(lines=list(current_lines)))
                    current_lines = []
                
                # Início de um conflito
                left_res = []
                base_res = []
                right_res = []
                
                # Pula a linha do marcador <<<<<<<
                i += 1
                
                # Lê conteúdo LEFT
                while i < len(lines) and not lines[i].startswith("|||||||") and not lines[i].startswith("======="):
                    left_res.append(lines[i])
                    i += 1
                
                # Se tiver base (|||||||), lê BASE
                if i < len(lines) and lines[i].startswith("|||||||"):
                    i += 1
                    while i < len(lines) and not lines[i].startswith("======="):
                        base_res.append(lines[i])
                        i += 1
                
                # Lê conteúdo RIGHT (após =======)
                if i < len(lines) and lines[i].startswith("======="):
                    i += 1
                    while i < len(lines) and not lines[i].startswith(">>>>>>>"):
                        right_res.append(lines[i])
                        i += 1
                
                # Fecha o bloco de conflito
                # Nota: passamos lines=[] apenas para satisfazer o campo obrigatório da base,
                # embora não seja usado diretamente no ConflictBlock nesta implementação.
                blocks.append(ConflictBlock(
                    lines=[], 
                    left_lines=left_res,
                    base_lines=base_res,
                    right_lines=right_res
                ))
                
                # Pula a linha do marcador >>>>>>>
                # (O loop principal incrementa i no final)
                
            else:
                current_lines.append(line)
            
            i += 1
            
        if current_lines:
            blocks.append(NormalBlock(lines=list(current_lines)))
            
        return blocks