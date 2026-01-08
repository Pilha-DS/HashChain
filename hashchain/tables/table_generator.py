"""Gerador de tabelas de substituição determinísticas."""
from typing import Dict, List, Tuple


class TableGenerator:
    """Gera tabelas de cifra determinísticas baseadas em seed."""
    
    DEFAULT_CHARACTERS = [
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
        "u", "v", "w", "x", "y", "z",
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
        "U", "V", "W", "X", "Y", "Z",
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
        "`", "´", "¨", "¯", "˘", "˙", "˚", "˝", "ˇ", "¸", "˛",
        "!", ",", "#", "$", "%", "&", "'", "(", ")", "*", "+",
        " ", ",", "-", ".", "/", "\\", ":", ";", "<", "=", ">", "?", "@", "[", "]", "^", "_", "`", "{", "|", "}", "~", '"',
        "á", "à", "â", "ã", "ä", "é", "è", "ê", "ë", "í", "ì", "î", "ï", "ó", "ò", "ô", "õ", "ö",
        "ú", "ù", "û", "ü", "ç", "Á", "À", "Â", "Ã", "Ä", "É", "È", "Ê", "Ë",
        "Í", "Ì", "Î", "Ï", "Ó", "Ò", "Ô", "Õ", "Ö", "Ú", "Ù", "Û", "Ü", "Ç"
    ]
    
    def __init__(self, seed: int, characters: List[str] = None):
        """
        Inicializa o gerador de tabelas.
        
        Args:
            seed: Seed para geração determinística
            characters: Lista de caracteres a serem codificados (opcional)
        """
        if not seed:
            raise ValueError("Deve fornecer o parâmetro seed")
        
        self.seed = seed
        self.characters = characters or self.DEFAULT_CHARACTERS
        self._tables: Dict[int, Dict[str, str]] = {}
        self._inverted_tables: Dict[int, Dict[str, str]] = {}
    
    def _generate_cipher(self, size: int, index: int) -> str:
        """
        Gera cifra determinística.
        
        Args:
            size: Tamanho da cifra
            index: Índice do caractere
            
        Returns:
            String binária representando a cifra
        """
        num = self.seed + index * 2654435761
        
        middle = []
        for i in range(size):
            bit = (num >> i) & 1
            middle.append('0' if bit == 0 else '1')
        
        return ''.join(middle)
    
    def generate_tables(self, specific_sizes: List[int]) -> Tuple[Dict[int, Dict[str, str]], Dict[int, Dict[str, str]]]:
        """
        Gera tabelas de cifra para tamanhos específicos.
        
        Args:
            specific_sizes: Lista de tamanhos específicos para gerar (ex: [32, 15, 20])
            
        Returns:
            Tupla contendo (tabelas_normais, tabelas_invertidas)
        """
        if not specific_sizes:
            raise ValueError("Deve fornecer o parâmetro specific_sizes")
        
        tables_ = {}
        
        for size in specific_sizes:
            table = {}
            for i, char in enumerate(self.characters):
                table[char] = self._generate_cipher(size, i)
            tables_[size] = table
        
        self._tables = tables_
        self._inverted_tables = {
            k: {v: kk for kk, v in d.items()}
            for k, d in tables_.items()
        }
        
        return self._tables, self._inverted_tables
    
    @property
    def tables(self) -> Dict[int, Dict[str, str]]:
        """Retorna as tabelas normais."""
        return self._tables
    
    @property
    def inverted_tables(self) -> Dict[int, Dict[str, str]]:
        """Retorna as tabelas invertidas."""
        return self._inverted_tables

