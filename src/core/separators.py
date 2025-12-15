"""
Definição de separadores sintáticos por extensão de arquivo.
Seção 2.3 do Plano Técnico.

Este módulo define os separadores que serão usados para "explodir" o código
em múltiplas linhas, permitindo que o diff3 opere em granularidade sintática.
"""

from typing import List, Dict

# Mapeamento de extensões para separadores
# TypeScript/JavaScript: Separadores lógicos (controle de fluxo, estruturas)
# TSX/JSX: Lógicos + Tags de interface (componentes React)
SEPARATORS: Dict[str, List[str]] = {
    # TypeScript/JavaScript - Separadores lógicos
    ".ts": ["{", "}", "[", "]", "(", ")", ";", ",", "=>", "??"],
    ".js": ["{", "}", "[", "]", "(", ")", ";", ",", "=>", "??"],

    # TSX/JSX - Lógicos + Tags de Interface
    ".tsx": [
        "{", "}", "[", "]", "(", ")", ";", ",", "=>", "??",
        "<", ">", "</", "/>", "{}", "className="
    ],
    ".jsx": [
        "{", "}", "[", "]", "(", ")", ";", ",", "=>", "??",
        "<", ">", "</", "/>", "{}", "className="
    ],
}


def get_separators(extension: str) -> List[str]:
    """
    Retorna separadores ordenados por tamanho decrescente.

    A ordenação por tamanho é crítica para evitar matching incorreto.
    Exemplo: "=>" deve ser testado antes de ">" para evitar quebra errada.

    Args:
        extension: Extensão do arquivo (ex: ".ts", ".tsx")

    Returns:
        Lista de separadores ordenados por comprimento (maior primeiro)

    Examples:
        >>> get_separators(".ts")
        ['??', '=>', '{', '}', '[', ']', '(', ')', ';', ',']

        >>> get_separators(".tsx")
        ['className=', '??', '=>', '</>', '{', '}', ...]
    """
    # Normalizar extensão para lowercase
    normalized_ext = extension.lower()

    # Usar separadores de .ts como fallback se extensão não reconhecida
    seps = SEPARATORS.get(normalized_ext, SEPARATORS[".ts"])

    # Ordenar por tamanho decrescente (multi-char antes de single-char)
    return sorted(seps, key=len, reverse=True)


def get_supported_extensions() -> List[str]:
    """
    Retorna lista de extensões suportadas pela ferramenta.

    Returns:
        Lista de extensões (ex: [".ts", ".tsx", ".js", ".jsx"])
    """
    return list(SEPARATORS.keys())


def is_supported_extension(extension: str) -> bool:
    """
    Verifica se uma extensão é suportada.

    Args:
        extension: Extensão a verificar (ex: ".ts")

    Returns:
        True se extensão é suportada, False caso contrário

    Examples:
        >>> is_supported_extension(".ts")
        True

        >>> is_supported_extension(".py")
        False
    """
    return extension.lower() in SEPARATORS
