"""Módulo de criptografia."""
import os
import random
from typing import List, Optional, Tuple, Dict

from ..tables import TableGenerator
from .key_generator import KeyGenerator
from .compression import Compression


class Encryption:
    """Classe para criptografar texto usando tabelas de substituição."""
    
    def __init__(self, debug_mode: bool = False):
        """
        Inicializa o módulo de criptografia.
        
        Args:
            debug_mode: Se True, imprime informações de debug
        """
        self.debug_mode = debug_mode
        self.key_generator = KeyGenerator(debug_mode=debug_mode)
        self.compression = Compression()
        self._color_codes = {
            "pad": "\033[0;0m",
            "red": "\033[1;31m",
            "gre": "\033[1;32m",
            "blu": "\033[1;34m",
            "yel": "\033[1;33m",
            "mag": "\033[1;35m",
            "cya": "\033[1;36m",
        }
    
    @staticmethod
    def _generate_random_seed(num_digits: int = 64) -> int:
        """
        Gera seed decimal aleatória.
        
        Args:
            num_digits: Número de dígitos da seed
            
        Returns:
            Seed gerada
        """
        bytes_random = os.urandom(num_digits // 2)
        large_number = int.from_bytes(bytes_random, "big")
        seed_str = str(large_number).zfill(num_digits)
        seed_str = seed_str[:num_digits]
        return int(seed_str)
    
    def encrypt(
        self,
        plaintext: str,
        pass_: Optional[List[int]] = None,
        seed: int = 0,
        no_salt: bool = False,
        min_table_leng: int = 20,
        max_table_leng: int = 999,
        compress_text: bool = True,
    ) -> Tuple[str, str, Dict]:
        """
        Criptografa texto utilizando tabelas de substituição geradas deterministicamente.
        
        Args:
            plaintext: Texto a ser criptografado
            pass_: Lista de passes para geração de chave (opcional)
            seed: Seed para geração determinística (opcional)
            no_salt: Se True, não usa salt
            min_table_leng: Tamanho mínimo da tabela (mínimo 20)
            max_table_leng: Tamanho máximo da tabela (máximo 999)
            compress_text: Se True, comprime o texto cifrado
            
        Returns:
            Tupla contendo (ciphertext, key, info_dict)
            
        Raises:
            ValueError: Se o texto plano não for fornecido
        """
        if min_table_leng < 20:
            min_table_leng = 20
        
        if not plaintext:
            raise ValueError("Parâmetro obrigatório: plaintext deve ser uma string não vazia")
        
        if pass_ is None:
            pass_ = []
        
        # Geração de valores padrão se não informados
        if not seed:
            seed = self._generate_random_seed(64)
        
        # Gera passes automaticamente se não fornecidos
        if not pass_:
            p = len(plaintext)
            while p > 0:
                p -= 1
                pass_.append(random.randint(min_table_leng, max_table_leng))
        
        # GERAÇÃO DE SEEDS DIFERENTES PARA CADA PASSE
        seeds_por_passe = []
        dict_tables_por_passe = {}
        
        random.seed(seed)
        for i, passe in enumerate(pass_):
            seed_passe = seed * 1000000 + passe
            seeds_por_passe.append(seed_passe)
            
            table_gen = TableGenerator(seed_passe)
            dict_tables_passe, _ = table_gen.generate_tables([passe])
            dict_tables_por_passe[passe] = dict_tables_passe[passe]
        
        random.seed()
        
        # Variáveis principais
        crude_ciphertext_list = []
        used_passes_sequence: List[int] = []
        invalid_characters_list = []
        control_index = 0
        control_key = len(pass_) - 1
        
        # Processo de criptografia principal
        for caracter in plaintext:
            try:
                passe_atual = pass_[control_index]
                tabela_atual = dict_tables_por_passe[passe_atual]
                cipher_char = tabela_atual[caracter]
                
                if self.debug_mode:
                    crude_ciphertext_list.append(
                        self._color_codes["gre"] + cipher_char + self._color_codes["pad"]
                    )
                else:
                    crude_ciphertext_list.append(cipher_char)
                
                used_passes_sequence.append(passe_atual)
            except KeyError:
                invalid_characters_list.append(caracter)
            
            control_index = 0 if control_index == control_key else control_index + 1
        
        # Aplicação do salt e geração da chave
        if not no_salt:
            salt_result = self._create_salt(
                crude_ciphertext_list, used_passes_sequence, seed, min_table_leng, max_table_leng
            )
            ciphertext = "".join(salt_result[0])
            
            if (len(ciphertext) % 20) == 0:
                key_result = self.key_generator.generate(
                    passes_list=salt_result[1],
                    current_seed=seed,
                    seeds_passes=seeds_por_passe,
                    salt_positions=salt_result[2],
                    ct_len_before_padding=len(ciphertext),
                )
                padding = 0
            else:
                padding = ((len(ciphertext) % 20) - 20) * -1
                ciphertext += padding * "1"
                key_result = self.key_generator.generate(
                    passes_list=salt_result[1],
                    current_seed=seed,
                    seeds_passes=seeds_por_passe,
                    salt_positions=salt_result[2],
                    padding=str(padding),
                    ct_len_before_padding=len(ciphertext) - padding,
                )
        else:
            ciphertext = "".join(crude_ciphertext_list)
            if (len(ciphertext) % 20) == 0:
                key_result = self.key_generator.generate(
                    passes_list=used_passes_sequence,
                    current_seed=seed,
                    seeds_passes=seeds_por_passe,
                    ct_len_before_padding=len(ciphertext),
                )
                padding = 0
            else:
                padding = ((len(ciphertext) % 20) - 20) * -1
                ciphertext += padding * "1"
                key_result = self.key_generator.generate(
                    passes_list=used_passes_sequence,
                    current_seed=seed,
                    seeds_passes=seeds_por_passe,
                    padding=str(padding),
                    ct_len_before_padding=len(ciphertext) - padding,
                )
        
        raw_ciphertext = ciphertext
        compressed = self.compression.compress(ciphertext)
        
        if compress_text:
            ciphertext = compressed
        
        info_dict = {
            "compressed": compressed,
            "key": key_result[1],
            "ciphertext": raw_ciphertext,
            "plaintext": plaintext,
            "passes": pass_,
            "seed": seed,
            "invalid_characters": invalid_characters_list,
        }
        
        if self.debug_mode:
            print(
                f"\nPlaintext: {self._color_codes['blu'] + plaintext + self._color_codes['pad']}\n\n"
                f"Ciphertext_list: {', '.join(p for p in crude_ciphertext_list)}\n\n"
                f"Seeds por passe: {seeds_por_passe}\n\n"
                f"Crude key: {key_result[2]}\n\n"
                f"Polished key: {key_result[1]}\n\n"
                f"Invalid characters: {invalid_characters_list}\n\n"
                f"Ciphertext: {ciphertext}\n\n"
            )
        
        return (ciphertext, key_result[1], info_dict)
    
    def _create_salt(
        self,
        ciphertext_list: List[str],
        current_pass: List[int],
        current_seed: int,
        min_table_leng: int,
        max_table_leng: int,
    ) -> Tuple[List[str], List[int], List[str]]:
        """
        Insere salt no ciphertext para aumentar entropia usando seeds determinísticas.
        
        Args:
            ciphertext_list: Lista de caracteres do ciphertext
            current_pass: Lista de passes atuais
            current_seed: Seed principal
            min_table_leng: Tamanho mínimo da tabela
            max_table_leng: Tamanho máximo da tabela
            
        Returns:
            Tupla contendo (ciphertext_com_salt, passes_com_salt, posicoes)
        """
        salt_ciphertext_list = ciphertext_list.copy()
        salt_passes = current_pass.copy()
        posicoes = []
        salt_leng = random.randint(20, 20 + len(ciphertext_list))
        
        random.seed(current_seed)
        
        for salt_index in range(salt_leng):
            salt_pass = random.randint(min_table_leng, max_table_leng)
            posicao = random.randint(0, len(salt_ciphertext_list) - 1)
            
            seed_salt = current_seed + (salt_index * 100000) + salt_pass + posicao
            
            table_gen = TableGenerator(seed_salt)
            tb, _ = table_gen.generate_tables([salt_pass])
            random_char = chr(random.randint(65, 90))
            
            if self.debug_mode:
                salt_passes.insert(
                    posicao, self._color_codes["red"] + str(salt_pass).zfill(3) + self._color_codes["pad"]
                )
                salt_ciphertext_list.insert(
                    posicao,
                    self._color_codes["red"] + tb[salt_pass][random_char] + self._color_codes["pad"],
                )
                posicoes.append(
                    self._color_codes["cya"] + str(len(str(posicao))).zfill(3) + self._color_codes["pad"]
                )
                posicoes.append(self._color_codes["yel"] + str(posicao) + self._color_codes["pad"])
            else:
                salt_passes.insert(posicao, salt_pass)
                salt_ciphertext_list.insert(posicao, tb[salt_pass][random_char])
                posicoes.append(str(len(str(posicao))).zfill(3))
                posicoes.append(str(posicao))
        
        random.seed()
        
        return (salt_ciphertext_list, salt_passes, posicoes)

