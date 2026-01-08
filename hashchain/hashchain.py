"""Classe principal HashChain que integra todos os módulos."""
from typing import List, Optional, Dict, Tuple

from .core import Encryption, Decryption, Compression
from .core.key_generator import KeyGenerator


class HashChain:
    """Classe principal para criptografia HashChain."""
    
    def __init__(self):
        """Inicializa a instância HashChain."""
        self._encryption = Encryption(debug_mode=False)
        self._decryption = Decryption()
        self._compression = Compression()
        self._info: List[Optional[str]] = [None, None, None, None, None, None]
    
    def encrypt(
        self,
        plaintext: str,
        pass_: Optional[List[int]] = None,
        seed: int = 0,
        no_salt: bool = False,
        debug_mode: bool = False,
        min_table_leng: int = 20,
        max_table_leng: int = 999,
        compress_text: bool = True,
        retonar: bool = False,
        printar: bool = False,
    ) -> Optional[List[str]]:
        """
        Criptografa texto utilizando tabelas de substituição.
        
        Args:
            plaintext: Texto a ser criptografado
            pass_: Lista de passes (opcional)
            seed: Seed para geração determinística (opcional)
            no_salt: Se True, não usa salt
            debug_mode: Se True, imprime informações de debug
            min_table_leng: Tamanho mínimo da tabela (mínimo 20)
            max_table_leng: Tamanho máximo da tabela (máximo 999)
            compress_text: Se True, comprime o texto cifrado
            retonar: Se True, retorna [ciphertext, key]
            printar: Se True, imprime resultados
            
        Returns:
            Lista [ciphertext, key] se retonar=True, None caso contrário
        """
        if debug_mode:
            self._encryption = Encryption(debug_mode=True)
        
        ciphertext, key, info_dict = self._encryption.encrypt(
            plaintext=plaintext,
            pass_=pass_,
            seed=seed,
            no_salt=no_salt,
            min_table_leng=min_table_leng,
            max_table_leng=max_table_leng,
            compress_text=compress_text,
        )
        
        self._info = [
            info_dict["compressed"],  # 0: texto comprimido
            key,  # 1: chave
            info_dict["ciphertext"],  # 2: texto cifrado não comprimido
            info_dict["plaintext"],  # 3: texto original
            info_dict["passes"],  # 4: passes
            info_dict["seed"],  # 5: seed
        ]
        
        if printar:
            print(f"Ciphertext:\n{ciphertext}")
            print(f"\nKey:\n{key}")
        
        if retonar:
            return [info_dict["ciphertext"], key]
        
        return None
    
    def decrypt(
        self,
        ciphertext: Optional[str] = None,
        key: Optional[str] = None,
        printar: bool = False,
        retonar: bool = False,
    ) -> Optional[str]:
        """
        Descriptografa texto cifrado usando a chave fornecida.
        
        Args:
            ciphertext: Texto cifrado (opcional, usa self._info se não fornecido)
            key: Chave de descriptografia (opcional, usa self._info se não fornecido)
            printar: Se True, imprime o resultado
            retonar: Se True, retorna o plaintext
            
        Returns:
            Plaintext se retonar=True, None caso contrário
        """
        # Usa valores internos se não fornecidos
        if ciphertext is None or ciphertext == "":
            ciphertext = self._info[0]  # texto comprimido
        
        if key is None or key == "":
            key = self._info[1]
        
        if not ciphertext or not key:
            raise ValueError(
                "ciphertext e/ou key ausentes. Gere com encrypt ou forneça valores válidos."
            )
        
        plaintext, info_dict = self._decryption.decrypt(
            ciphertext=ciphertext,
            key=key,
            started_with_compressed=None,
        )
        
        self._info[3] = plaintext
        self._info[1] = key
        self._info[4] = info_dict["passes"]
        self._info[5] = info_dict["seed"]
        
        if printar:
            print(f"Plaintext:\n{plaintext}")
        
        if retonar:
            return plaintext
        
        return None
    
    def compression(self, cipher_text: str, printar: bool = False) -> Optional[str]:
        """
        Comprime texto binário.
        
        Args:
            cipher_text: Texto binário a ser comprimido
            printar: Se True, imprime o resultado
            
        Returns:
            Texto comprimido ou None se houver erro
        """
        return self._compression.compress(cipher_text, print_output=printar)
    
    def decompression(self, compressed_cipher_text: str, printar: bool = False) -> str:
        """
        Descomprime texto binário comprimido.
        
        Args:
            compressed_cipher_text: Texto comprimido
            printar: Se True, imprime o resultado
            
        Returns:
            Texto descomprimido ou mensagem de erro
        """
        return self._compression.decompress(compressed_cipher_text, print_output=printar)
    
    def info(self, *args) -> Optional[str | int | List[int]]:
        """
        Retorna informações armazenadas da última operação.
        
        Args:
            *args: Índices ou aliases (0: compressed, 1: key, 2: ciphertext, 3: plaintext, 4: passes, 5: seed)
            
        Returns:
            Valor solicitado ou lista de valores se múltiplos argumentos
        """
        if not args:
            return None
        
        if all(i is None for i in self._info):
            return None
        
        aliases = {
            "compressed": 0, "cc": 0, "compressed text": 0, "compressed_text": 0,
            "compressed cipher": 0, "compressed_cipher": 0,
            "key": 1, "chave": 1, "k": 1,
            "cipher": 2, "cipher text": 2, "cipher_text": 2, "c": 2,
            "plain": 3, "plain text": 3, "plain_text": 3, "text": 3, "p": 3,
            "passes": 4, "passos": 4, "passe": 4, "pass": 4, "ps": 4, "steps": 4, "step": 4,
            "seed": 5, "s": 5,
        }
        
        data = []
        for arg in args:
            if isinstance(arg, str):
                search = arg.lower()
                idx = aliases.get(search)
                if idx is not None:
                    data.append(self._info[idx])
            elif isinstance(arg, int):
                if 0 <= arg <= 5:
                    data.append(self._info[arg])
        
        if len(data) == 1:
            return data[0]
        return data
    
    def out(self, *args) -> None:
        """
        Imprime informações armazenadas da última operação.
        
        Args:
            *args: Índices ou aliases (0: compressed, 1: key, 2: ciphertext, 3: plaintext, 4: passes, 5: seed)
        """
        name_order = [
            "\nCompressed Text:", "\nKey:", "\nCipher Text:",
            "\nPlain Text:", "\nPasses:", "\nSeed:"
        ]
        
        if self._info is None or all(i is None for i in self._info):
            print(None)
            return
        
        if not args:
            print("\n ----- Complete Info ----- ")
            for i, name in enumerate(name_order):
                if self._info[i] is not None:
                    print(f"{name}")
                    print(self._info[i])
            return
        
        aliases = {
            "compressed": 0, "cc": 0, "compressed text": 0, "compressed_text": 0,
            "compressed cipher": 0, "compressed_cipher": 0,
            "key": 1, "chave": 1, "k": 1,
            "cipher": 2, "cipher text": 2, "cipher_text": 2, "c": 2,
            "plain": 3, "plain text": 3, "plain_text": 3, "text": 3, "p": 3,
            "passes": 4, "passos": 4, "passe": 4, "pass": 4, "ps": 4, "steps": 4, "step": 4,
            "seed": 5, "s": 5,
        }
        
        for arg in args:
            if isinstance(arg, str):
                search = arg.lower()
                idx = aliases.get(search)
                if idx is not None:
                    print(f"{name_order[idx]}")
                    print(self._info[idx])
            elif isinstance(arg, int):
                if 0 <= arg <= 5:
                    print(f"{name_order[arg]}")
                    print(self._info[arg], '\n')

