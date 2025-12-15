class Postprocessor:
    """
    Equivalente ao método 'removeMarkers' do SepMerge.
    """
    def reconstruct(self, text: str, extension: str) -> str:
        from .separators import get_separators
        separators = get_separators(extension)
        
        result = text
        for sep in separators:
            # Reverte a explosão: remove os \n em volta do separador
            # Java: result.replace("\n" + separator + "\n", separator)
            token = f"\n{sep}\n"
            result = result.replace(token, sep)
            
        return result

    def count_conflicts(self, text: str) -> int:
        return text.count("<<<<<<<")