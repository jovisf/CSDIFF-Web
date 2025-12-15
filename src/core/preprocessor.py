from typing import List

class Preprocessor:
    """
    Equivalente simplificado para o método 'addMarkers' do SepMerge.
    Apenas isola os separadores com quebras de linha.
    """
    def __init__(self, extension: str):
        from .separators import get_separators
        self.separators = get_separators(extension)

    def explode(self, text: str) -> str:
        # Lógica idêntica ao SepMerge (Java):
        # line.replace(separator, String.format("%n%s%n", separator))
        
        # Para evitar substituir separadores que foram inseridos por substituições anteriores,
        # o ideal é uma abordagem cuidadosa, mas o SepMerge original faz um loop simples.
        # Vamos replicar o comportamento do Java.
        
        result = text
        for sep in self.separators:
            # O Python replace é equivalente ao do Java para strings
            result = result.replace(sep, f"\n{sep}\n")
            
        return result