"""Módulo de compressão e descompressão de texto binário."""
from typing import Optional


class Compression:
    """Classe para compressão e descompressão de texto binário."""
    
    TRANSLATION_DICT = {
        "Z": "0",
        "X": "1",
        "2": "2",
        "3": "3",
        "4": "4",
        "5": "5",
        "6": "6",
        "7": "7",
        "8": "8",
        "9": "9",
    }
    
    def __init__(self):
        """Inicializa o compressor."""
        pass
    
    def compress(self, cipher_text: str, print_output: bool = False) -> Optional[str]:
        """
        Comprime texto binário usando algoritmo de run-length encoding.
        
        Args:
            cipher_text: Texto binário (apenas '0' e '1')
            print_output: Se True, imprime o resultado
            
        Returns:
            Texto comprimido ou None se houver erro
        """
        if not all(char in ["0", "1"] for char in cipher_text):
            print(
                "Erro: Não foi possível comprimir o texto, caractere inválido no texto cifrado. "
                "Apenas '0' e '1' são permitidos, verifique se o texto foi adulterado."
            )
            return None
        
        pairs = []
        consecutive = 0
        last = ''
        cipher_text += " "
        
        for char in cipher_text:
            if not last:
                last = char
                consecutive += 1
            elif char == last:
                consecutive += 1
            else:
                pairs.append([consecutive, last])
                last = char
                consecutive = 1
        
        compressed = []
        
        for pair in pairs:
            count, char = pair
            if count == 1:
                compressed.append(char)
            elif count == 2:
                compressed.append(char * 2)
            elif 3 <= count <= 9:
                compressed.append(self.TRANSLATION_DICT[str(count)] + char)
            else:
                count_str = str(count)
                count_str = count_str.replace("0", "Z")
                count_str = count_str.replace("1", "X")
                compressed.append(count_str + char)
        
        result = ''.join(compressed)
        
        if print_output:
            print(result)
        
        return result
    
    def decompress(self, compressed_cipher_text: str, print_output: bool = False) -> str:
        """
        Descomprime texto binário comprimido.
        
        Args:
            compressed_cipher_text: Texto comprimido
            print_output: Se True, imprime o resultado
            
        Returns:
            Texto descomprimido ou mensagem de erro
        """
        valid_chars = ["0", "1", "Z", "X", "2", "3", "4", "5", "6", "7", "8", "9"]
        for char in compressed_cipher_text:
            if char not in valid_chars:
                return (
                    "Erro: Não foi possível descomprimir o texto, caractere inválido no texto comprimido. "
                    "Apenas '0', '1', 'Z', 'X' e dígitos são permitidos, verifique se o texto foi adulterado."
                )
        
        normalized = compressed_cipher_text
        total: list[str] = []
        aux: list[str] = []
        
        for c in normalized:
            if c in ["0", "1"] and not aux:
                total.append(c)
            elif c in ["Z", "X", "2", "3", "4", "5", "6", "7", "8", "9"]:
                aux.append(self.TRANSLATION_DICT[c])
            else:
                if aux:
                    total.append(c * int("".join(aux)))
                    aux = []
        
        result = "".join(total)
        
        if print_output:
            print("Decompressed text:\n" + result)
        
        return result

