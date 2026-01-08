"""Módulo de geração de chaves para descriptografia."""
from typing import List, Optional, Tuple


class KeyGenerator:
    """Classe para geração de chaves polidas para descriptografia."""
    
    def __init__(self, debug_mode: bool = False):
        """
        Inicializa o gerador de chaves.
        
        Args:
            debug_mode: Se True, adiciona cores ANSI na chave detalhada
        """
        self.debug_mode = debug_mode
        self._color_codes = {
            "pad": "\033[0;0m",
            "red": "\033[1;31m",
            "gre": "\033[1;32m",
            "blu": "\033[1;34m",
            "yel": "\033[1;33m",
            "mag": "\033[1;35m",
            "cya": "\033[1;36m",
        }
    
    def generate(
        self,
        passes_list: List[int],
        current_seed: int,
        seeds_passes: Optional[List[int]] = None,
        salt_positions: Optional[List[str]] = None,
        padding: str = "",
        ct_len_before_padding: Optional[int] = None,
    ) -> Tuple[List[str], str, str]:
        """
        Gera chave polida para descriptografia posterior.
        
        Args:
            passes_list: Lista de passes utilizados
            current_seed: Seed principal
            seeds_passes: Lista de seeds por passe (opcional)
            salt_positions: Lista de posições de salt (opcional)
            padding: String de padding (opcional)
            ct_len_before_padding: Comprimento do ciphertext antes do padding (opcional)
            
        Returns:
            Tupla contendo (passes_formatados, chave_polida, chave_detalhada)
        """
        if salt_positions is None:
            salt_positions = []
        if seeds_passes is None:
            seeds_passes = []
        
        # Prepara os passes
        poli_passes = [str(p).zfill(3) for p in passes_list]
        poli_seeds = (
            [str(s).zfill(20) for s in seeds_passes] if seeds_passes else []
        )
        poli_salt = [str(s) for s in salt_positions] if salt_positions else []
        
        # Prepara valores para a chave
        seed_value = str(current_seed)
        pl = str(len(poli_passes))
        lolp = str(len(pl)).zfill(3)
        sl = str(len(seed_value)).zfill(3)
        
        # Comprimento do ciphertext antes do padding
        if ct_len_before_padding is None:
            ct_len_before_padding = 0
        cl_str = str(ct_len_before_padding)
        lcl = str(len(cl_str)).zfill(3)
        
        # Flag de salt explícita (1 = com salt, 0 = sem salt)
        salt_flag = "1" if salt_positions else "0"
        lsf = "001"  # comprimento fixo de 1
        
        # Informações sobre seeds dos passes
        seeds_l = str(len(seeds_passes)) if seeds_passes else "000"
        lol_seeds = str(len(seeds_l)).zfill(3) if seeds_passes else "000"
        
        # Sempre incluir campos de salt, mesmo quando vazio
        salt_count = int(len(salt_positions) / 2) if salt_positions else 0
        salt_l = [str(salt_count)]
        lol_salt = [str(len(salt_l[0])).zfill(3)]
        
        # Aplica cores se estiver em debug mode
        if self.debug_mode:
            seed_value = self._color_codes["blu"] + seed_value + self._color_codes["pad"]
            pl = self._color_codes["mag"] + pl + self._color_codes["pad"]
            lolp = self._color_codes["mag"] + lolp + self._color_codes["pad"]
            sl = self._color_codes["mag"] + sl + self._color_codes["pad"]
            salt_l = [self._color_codes["mag"] + s + self._color_codes["pad"] for s in salt_l]
            lol_salt = [self._color_codes["mag"] + s + self._color_codes["pad"] for s in lol_salt]
            poli_passes = [self._color_codes["gre"] + p + self._color_codes["pad"] for p in poli_passes]
            poli_seeds = [self._color_codes["yel"] + p + self._color_codes["pad"] for p in poli_seeds]
            poli_salt = [self._color_codes["red"] + p + self._color_codes["pad"] for p in poli_salt]
        
        # Gera chave detalhada (apenas para debug)
        crude_key = (
            f"\nseed principal: {seed_value}\n\n"
            f"salt: lol_salt: {', '.join(lol_salt)}, salt_l: {', '.join(salt_l)}, \n"
            f"posições salt: {', '.join(poli_salt)}\n\n"
            f"salt_flag: lsf: {lsf}, sf: {salt_flag}\n\n"
            f"passes: lolp: {lolp}, pl: {pl}, \n"
            f"passes: {', '.join(poli_passes)}\n\n"
            f"ct_len_before_padding: lcl: {lcl}, cl: {cl_str}\n\n"
            f"padding: {padding}"
        )
        
        # Gera chave polida (para uso real)
        polished_key = "".join([
            "".join(lol_salt),
            "".join(salt_l),
            "".join(poli_salt),
            lsf,
            salt_flag,
            "".join(lolp),
            "".join(pl),
            "".join(poli_passes),
            lcl,
            cl_str,
            "".join(sl),
            "".join(seed_value),
            padding,
        ])
        
        return (poli_passes, polished_key, crude_key)

