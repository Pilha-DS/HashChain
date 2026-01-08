"""Módulo de descriptografia."""
import re
from typing import List, Optional, Tuple, Dict

from ..tables import TableGenerator
from .compression import Compression


class Decryption:
    """Classe para descriptografar texto usando tabelas de substituição."""
    
    def __init__(self):
        """Inicializa o módulo de descriptografia."""
        self.compression = Compression()
    
    @staticmethod
    def _remove_ansi(s: str) -> str:
        """Remove sequências ANSI de uma string."""
        return re.sub(r"\x1b\[[0-9;]*m", "", s)
    
    def decrypt(
        self,
        ciphertext: str,
        key: str,
        started_with_compressed: Optional[bool] = None,
    ) -> Tuple[str, Dict]:
        """
        Descriptografa texto cifrado usando a chave fornecida.
        
        Args:
            ciphertext: Texto cifrado (pode estar comprimido)
            key: Chave de descriptografia
            started_with_compressed: Se True, indica que o texto já estava comprimido
            
        Returns:
            Tupla contendo (plaintext, info_dict)
            
        Raises:
            ValueError: Se ciphertext ou key forem inválidos
        """
        # Remove sequências ANSI se presentes
        ciphertext = self._remove_ansi(ciphertext)
        key = self._remove_ansi(key)
        
        if not ciphertext or not key:
            raise ValueError("ciphertext e/ou key ausentes. Forneça valores válidos.")
        
        if not isinstance(ciphertext, str) or not isinstance(key, str):
            raise ValueError("ciphertext e key devem ser strings.")
        
        # Detecta se está comprimido
        is_compressed = False
        for char in ciphertext:
            if char not in ["0", "1"]:
                is_compressed = True
                break
        
        if started_with_compressed is None:
            started_with_compressed = is_compressed
        
        # Descomprime se necessário
        if is_compressed:
            decompressed = self.compression.decompress(ciphertext)
            if decompressed.startswith("Erro"):
                raise ValueError(decompressed)
            ciphertext = decompressed
        
        # Parse da chave
        parsed_data = self._parse_key(ciphertext, key, started_with_compressed)
        passes, seed, ciphertext_list = parsed_data
        
        # Gera tabelas invertidas para descriptografia
        seeds_por_passe = []
        dict_tables_por_passe = {}
        
        for i, passe in enumerate(passes):
            seed_passe = seed * 1000000 + passe
            seeds_por_passe.append(seed_passe)
            
            table_gen = TableGenerator(seed_passe)
            _, inverted_tables = table_gen.generate_tables([passe])
            dict_tables_por_passe[passe] = inverted_tables[passe]
        
        # Descriptografa
        plaintext = []
        for n, p in enumerate(passes):
            if n < len(ciphertext_list):
                val = ciphertext_list[n]
                inv_table = dict_tables_por_passe[p]
                if val in inv_table:
                    plaintext.append(inv_table[val])
                else:
                    # Caractere não encontrado na tabela
                    pass
        
        plaintext_str = "".join(plaintext)
        
        info_dict = {
            "plaintext": plaintext_str,
            "passes": passes,
            "seed": seed,
            "compressed": is_compressed,
        }
        
        return (plaintext_str, info_dict)
    
    def _parse_key(
        self,
        ciphertext: str,
        key: str,
        started_with_compressed: bool,
    ) -> Tuple[List[int], int, List[str]]:
        """
        Faz parse da chave e retorna dados necessários para descriptografia.
        
        Args:
            ciphertext: Texto cifrado
            key: Chave de descriptografia
            started_with_compressed: Se True, texto estava comprimido
            
        Returns:
            Tupla contendo (passes, seed, ciphertext_list)
        """
        # Tenta primeiro com formato com salt, depois sem salt
        try:
            return self._parse_key_with_salt(ciphertext, key, started_with_compressed)
        except Exception:
            return self._parse_key_without_salt(ciphertext, key, started_with_compressed)
    
    def _parse_key_with_salt(
        self,
        ciphertext: str,
        key: str,
        started_with_compressed: bool,
    ) -> Tuple[List[int], int, List[str]]:
        """Faz parse de chave com formato que inclui salt."""
        ptr = 0
        
        if len(key) < 3:
            raise ValueError("Chave inválida: incompleta (lol_salt)")
        lol_salt = int(key[ptr:ptr + 3])
        ptr += 3
        
        if lol_salt == 0:
            salt_l = 0
        else:
            if len(key) < ptr + lol_salt:
                raise ValueError("Chave inválida: incompleta (salt_l)")
            salt_l = int(key[ptr:ptr + lol_salt])
            ptr += lol_salt
        
        posicoes = []
        for _ in range(salt_l):
            if len(key) < ptr + 3:
                raise ValueError("Chave inválida: incompleta (len posicao)")
            pn_len = int(key[ptr:ptr + 3])
            ptr += 3
            if pn_len < 0:
                raise ValueError("Chave inválida: tamanho de posição negativo")
            if len(key) < ptr + pn_len:
                raise ValueError("Chave inválida: incompleta (posicao)")
            posicoes.append(int(key[ptr:ptr + pn_len]))
            ptr += pn_len
        
        # Lê salt_flag
        if len(key) < ptr + 3:
            raise ValueError("Chave inválida: incompleta (lsf)")
        lsf = int(key[ptr:ptr + 3])
        ptr += 3
        if lsf != 1 or len(key) < ptr + lsf:
            raise ValueError("Chave inválida: incompleta (sf)")
        salt_flag = key[ptr:ptr + lsf]
        ptr += lsf
        
        # Lê passes
        if len(key) < ptr + 3:
            raise ValueError("Chave inválida: incompleta (lol_p)")
        lol_p = int(key[ptr:ptr + 3])
        ptr += 3
        
        if lol_p == 0:
            pl = 0
        else:
            if len(key) < ptr + lol_p:
                raise ValueError("Chave inválida: incompleta (pl)")
            pl = int(key[ptr:ptr + lol_p])
            ptr += lol_p
        
        passes = []
        for _ in range(pl):
            if len(key) < ptr + 3:
                raise ValueError("Chave inválida: incompleta (pass)")
            passes.append(int(key[ptr:ptr + 3]))
            ptr += 3
        
        # Lê comprimento do ciphertext antes do padding
        if len(key) < ptr + 3:
            raise ValueError("Chave inválida: incompleta (lcl)")
        lcl = int(key[ptr:ptr + 3])
        ptr += 3
        if lcl < 0 or len(key) < ptr + lcl:
            raise ValueError("Chave inválida: incompleta (cl)")
        cl = int(key[ptr:ptr + lcl])
        ptr += lcl
        
        # Lê seed
        if len(key) < ptr + 3:
            raise ValueError("Chave inválida: incompleta (sl)")
        sl = int(key[ptr:ptr + 3])
        ptr += 3
        if sl < 0 or len(key) < ptr + sl:
            raise ValueError("Chave inválida: incompleta (seed)")
        seed = int(key[ptr:ptr + sl])
        ptr += sl
        
        # Lê padding
        padding = 0
        if ptr < len(key):
            restante = key[ptr:]
            if restante:
                padding = int(restante)
        
        # Aplica padding e ajusta pelo comprimento declarado
        ct_eff = ciphertext
        if padding > 0:
            if padding > len(ct_eff):
                raise ValueError("Padding maior que o tamanho do ciphertext")
            ct_eff = ct_eff[:len(ct_eff) - padding]
        
        if cl > 0 and len(ct_eff) != cl:
            if len(ct_eff) > cl:
                ct_eff = ct_eff[:cl]
            else:
                if not started_with_compressed:
                    raise ValueError("Ciphertext menor que o comprimento declarado")
        
        # Valida soma e ajusta tolerantemente para entradas comprimidas
        total_len = len(ct_eff)
        sum_passes = sum(passes)
        if sum_passes != total_len:
            if started_with_compressed and passes:
                delta = sum_passes - total_len
                passes[-1] -= delta
                if passes[-1] < 0:
                    passes[-1] = 0
            else:
                raise ValueError("inconsistência entre passes e ciphertext (com salt)")
        
        # Segmenta
        ciphertext_list = []
        resto = ct_eff
        for comp in passes:
            ciphertext_list.append(resto[:comp])
            resto = resto[comp:]
        
        # Remove salt apenas se flag ativa e houver posições
        if salt_flag == "1" and posicoes:
            for pos in reversed(posicoes):
                if 0 <= pos < len(ciphertext_list):
                    del ciphertext_list[pos]
                    del passes[pos]
        
        return passes, seed, ciphertext_list
    
    def _parse_key_without_salt(
        self,
        ciphertext: str,
        key: str,
        started_with_compressed: bool,
    ) -> Tuple[List[int], int, List[str]]:
        """Faz parse de chave com formato sem salt."""
        ptr = 0
        
        # Lê salt_flag (mesmo sem salt, flag deve existir)
        if len(key) < 3:
            raise ValueError("Chave inválida: incompleta (lsf)")
        lsf = int(key[ptr:ptr + 3])
        ptr += 3
        if lsf != 1 or len(key) < ptr + lsf:
            raise ValueError("Chave inválida: incompleta (sf)")
        salt_flag = key[ptr:ptr + lsf]
        ptr += lsf
        
        # Lê passes
        if len(key) < 3:
            raise ValueError("Chave inválida: incompleta (lol_p)")
        lol_p = int(key[ptr:ptr + 3])
        ptr += 3
        
        if lol_p == 0:
            pl = 0
        else:
            if len(key) < ptr + lol_p:
                raise ValueError("Chave inválida: incompleta (pl)")
            pl = int(key[ptr:ptr + lol_p])
            ptr += lol_p
        
        passes = []
        for _ in range(pl):
            if len(key) < ptr + 3:
                raise ValueError("Chave inválida: incompleta (pass)")
            passes.append(int(key[ptr:ptr + 3]))
            ptr += 3
        
        # Lê comprimento do ciphertext antes do padding
        if len(key) < ptr + 3:
            raise ValueError("Chave inválida: incompleta (lcl)")
        lcl = int(key[ptr:ptr + 3])
        ptr += 3
        if lcl < 0 or len(key) < ptr + lcl:
            raise ValueError("Chave inválida: incompleta (cl)")
        cl = int(key[ptr:ptr + lcl])
        ptr += lcl
        
        # Lê seed
        if len(key) < ptr + 3:
            raise ValueError("Chave inválida: incompleta (sl)")
        sl = int(key[ptr:ptr + 3])
        ptr += 3
        if sl < 0 or len(key) < ptr + sl:
            raise ValueError("Chave inválida: incompleta (seed)")
        seed = int(key[ptr:ptr + sl])
        ptr += sl
        
        # Lê padding
        padding = 0
        if ptr < len(key):
            restante = key[ptr:]
            if restante:
                padding = int(restante)
        
        # Aplica padding e ajusta pelo comprimento declarado
        ct_eff = ciphertext
        if padding > 0:
            if padding > len(ct_eff):
                raise ValueError("Padding maior que o tamanho do ciphertext")
            ct_eff = ct_eff[:len(ct_eff) - padding]
        
        if cl > 0 and len(ct_eff) != cl:
            if len(ct_eff) > cl:
                ct_eff = ct_eff[:cl]
            else:
                if not started_with_compressed:
                    raise ValueError("Ciphertext menor que o comprimento declarado")
        
        # Valida soma e ajusta tolerantemente para entradas comprimidas
        total_len = len(ct_eff)
        sum_passes = sum(passes)
        if sum_passes != total_len:
            if started_with_compressed and passes:
                delta = sum_passes - total_len
                passes[-1] -= delta
                if passes[-1] < 0:
                    passes[-1] = 0
            else:
                raise ValueError("inconsistência entre passes e ciphertext (sem salt)")
        
        # Segmenta
        ciphertext_list = []
        resto = ct_eff
        for comp in passes:
            ciphertext_list.append(resto[:comp])
            resto = resto[comp:]
        
        return passes, seed, ciphertext_list

