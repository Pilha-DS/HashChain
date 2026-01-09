# ===== HashChainClass =====
#      --- Imports ---
import os
import random
import re
from tables import gerar_tabelas


class HashChainEncryption:
    
    def __init__(self):
        # Will recieve data in: [compressed_text: str, key: str, cipher_text: str, plain_text: str, passes: list[int], seed: int]
        self._info: list[str] | list[None] = [None, None, None, None, None, None]

    # Prints the desired stored encrypted data
    def out(self, *args) -> None:
        """Can only recieve parameters of type int or str.\n
        Prints the stored data based on the parameters given."""
        
        # If no encryption has occurred or all values are None, return None
        name_order = ["\nCompressed Text:", "\nKey:", "\nCipher Text:", "\nPlain Text:", "\nPasses:", "\nSeed:"]
        
        if self._info is None:
            print(None)
            return None

        args = list(args)
        
        if not args:
            print("\n ----- Complete Info ----- ")
            for i, name in enumerate(name_order):
                if self._info[i] is not None:
                    print(f"{name}")
                    print(self._info[i])
            return None
        
        # If the argument is a string interpret it as so
        for i, params in enumerate(args):
            if isinstance(args[i], str):
                # Standardizes the argument
                args[i] = args[i].lower()

                # Aliases for the keywords
                plain_text = ["p", "plain", "plain text", "plain_text", "text"]
                cipher_text = ["c", "cipher", "cipher text", "cipher_text"]
                compressed_text = [
                    "cc",
                    "compressed",
                    "compressed text",
                    "compressed_text",
                    "compressed cipher",
                    "compressed_cipher",
                    "compressed cipher text",
                    "compressed_cipher_text",
                ]
                key = ["key", "chave", "k"]
                passes = [
                    "passes",
                    "passos",
                    "passe",
                    "p",
                    "pass",
                    "ps",
                    "steps",
                    "step",
                ]
                seed = ["seed", "s"]

                # Prints the desired data
                if args[i] in compressed_text:
                    print("Compressed text:\n" + self._info[0])
                elif args[i] in key:
                    print("Key:\n" + self._info[1])
                elif args[i] in cipher_text:
                    print("Cipher text:\n" + self._info[2])
                elif args[i] in plain_text:
                    print("Plain text:\n" + self._info[3])
                elif args[i] in passes:
                    print("Passes:\n" + self._info[4])
                elif args[i] in seed:
                    print("Seed:\n" + self._info[5])

            # Else if the argument is an int
            elif isinstance(args[i], int):
                # If the int is in range print the desired data, if it is out of range print all the info
                if len(args) > 1:
                    if args[i] >= 0 and args[i] <= 5:
                        print(name_order[args[i]])
                        print(self._info[args[i]], '\n')
                    else:
                        print("\n ----- Complete Info: ----- ")
                        print("\nCompressed text:")
                        print(self._info[0])
                        print("\nKey:")
                        print(self._info[1])
                        print("\nCipher text:")
                        print(self._info[2])
                        print("\nPlain text:")
                        print(self._info[3])
                        print("\nPasses:")
                        print(self._info[4])
                        print("\nSeed:")
                        print(self._info[5])
                        break
                else:
                    if args[i] >= 0 and args[i] <= 5:
                        print(name_order[args[i]])
                        print(self._info[args[i]])
                    
    # The stadard get info method, retuns the stored data values from the last encryption
    def info(self, *args) -> str | int | list[int] | None:
        
        """Can only recieve parameters of type int or str.\n\nReturns the stored data based on the parameters given, if mulltiple arguments are given returns a list of the data.\n\n0: Compressed cipher text\n\n1: Key\n\n2: Cipher text\n\n3: Plain text"""
        
        if not args:
            return None
        
        if all(i is None for i in self._info):
            return None
        
        data = []
        for arg in args:
        # If the parameter is a str returns the value using its matching keyword else returns the data by its position in the list
            if isinstance(arg, str):
                search = arg.lower()
                plain_text = ["p", "plain", "plain text", "plain_text", "text"]
                cipher_text = ["c", "cipher", "cipher text", "cipher_text"]
                compressed_text = [
                    "cc",
                    "compressed",
                    "compressed text",
                    "compressed_text",
                    "compressed cipher",
                    "compressed_cipher",
                    "compressed cipher text",
                    "compressed_cipher_text",
                ]
                key = ["key", "chave", "k"]
                passes = [
                    "passes",
                    "passos",
                    "passe",
                    "p",
                    "pass",
                    "ps",
                    "steps",
                    "step",
                ]
                seed = ["seed", "s"]
                if search in compressed_text:
                    data.append(self._info[0])
                elif search in key:
                    data.append(self._info[1])
                elif search in cipher_text:
                    data.append(self._info[2])
                elif search in plain_text:
                    data.append(self._info[3])
                elif search in passes:
                    data.append(self._info[4])
                elif search in seed:
                    data.append(self._info[5])
            elif isinstance(arg, int):
                data.append(self._info[arg])
            else:
                raise ValueError("Argument must be of type int or str.")
                
        if len(data) == 1:
            return data[0]
        return data
    
    # Receives a ciphered text and retuns a compressed ciphered text.
    def compression(self, cipher_text: str, printar: bool = False) -> str:
        
        if not all(char in ["0", "1"] for char in cipher_text):
            print("Erro: Não foi possível comprimir o texto, caractere inválido no texto cifrado. Apenas '0' e '1' são permitidos, verifique se o texto foi adulterado.")
            return None
        
        pares = []
        consecutivos = 0
        last = ''
        cipher_text += " "
        
        for _, char in enumerate(cipher_text):
            if not last:
                last = char
                consecutivos += 1
            elif char == last:
                consecutivos += 1
            else:
                pares.append([consecutivos, last])
                last = char
                consecutivos = 1
                
        trad = {
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

        compressed = []
        
        for par in pares:
            if par[0] == 1:
                compressed.append(par[1])
            elif par[0] == 2:
                compressed.append(par[1] * 2)
            elif par[0] >= 3 and par[0] <= 9:
                compressed.append(trad[str(par[0])] + par[1])
            else:
                par[0] = str(par[0])
                par[0] = par[0].replace("0", "Z")
                par[0] = par[0].replace("1", "X")
                compressed.append(par[0] + par[1])  
                
        if printar:
            print(''.join(compressed))
            
        return ''.join(compressed)
    
    # Receives a compressed ciphered text and retuns the ciphered text.
    def decompression(self, compressed_cipher_text: str, printar: bool = False) -> str:
        
        for char in compressed_cipher_text:
            if char not in ["0", "1", "Z", "X", "2", "3", "4", "5", "6", "7", "8", "9"]:
                return "Erro: Não foi possível descomprimir o texto, caractere inválido no texto comprimido. Apenas '0', '1', 'Z', 'X' e dígitos são permitidos, verifique se o texto foi adulterado."
        
        norm: str = compressed_cipher_text
        trad = {
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

        total: list[str] = []
        aux: list[str] = []

        for c in norm:
            if c in ["0", "1"] and not aux:
                total.append(c)
            elif c in ["Z", "X", "2", "3", "4", "5", "6", "7", "8", "9"]:
                aux.append(trad[c])
            else:
                total.append(c * int("".join(aux)))
                aux = []

        if printar:
            print("Decompressed text:\n" + "".join(total))

        return "".join(total)
    
    # Receives a plain text and returns the compressed cipher text.
    def encrypt(
        self,
        plaintext: str = "",
        pass_: list = None,
        seed: int = 0,
        no_salt: bool = False,
        debug_mode: bool = False,
        min_table_leng: int = 20,
        max_table_leng: int = 999,
        compress_text: bool = True,
        retonar: bool = False,
        printar: bool = False,
    ):
        def gerar_seed_decimal_aleatoria(num_digitos: int = 64) -> int:
            """Gera seed de 64 caracteres por padrão"""
            # Gera bytes aleatórios seguros
            bytes_aleatorios = os.urandom(num_digitos // 2)  # cada byte ≈ 2 dígitos
            # Converte os bytes para inteiro
            large_number = int.from_bytes(bytes_aleatorios, "big")
            # Formata para garantir exatamente num_digitos
            seed_str = str(large_number).zfill(num_digitos)
            seed_str = seed_str[:num_digitos]
            return int(seed_str)

        """
        Criptografa texto utilizando tabelas de substituição geradas deterministicamente.

        Args:
            plaintext (str): Texto a ser criptografado (obrigatorio)
            pass_ (list): Lista de passes para geração de chave (opcional)
            seed (int): Seed para geração determinística (opcional)
            no_salt (bool): Gera o cipher text sem salt (opcional)
            debug_mode (bool): Retornas os valores em modo desenvolvedor a função
            min_table_leng (int): O tamanho minimo da tabela de substituição (opcional). Não pode sere inferior a (20)
            max_table_leng (int): O tamanho maximo da tabela de substituição (opcional). Não pode ultrapassar (999)

        Returns:
            list: Lista contendo [texto cifrado, chave]

        Raises:
            ValueError: Se o texto plano não for fornecido
        """
        # Inicialização de parâmetros opcionais
        if pass_ is None:
            pass_ = []

        cor = {
            "pad": "\033[0;0m",
            "red": "\033[1;31m",
            "gre": "\033[1;32m",
            "blu": "\033[1;34m",
            "yel": "\033[1;33m",
            "mag": "\033[1;35m",
            "cya": "\033[1;36m",
        }

        # Validação dos parâmetros obrigatórios
        if min_table_leng < 20:
            min_table_leng = 20
        if not plaintext:
            raise ValueError(
                "Parâmetro obrigatório: plaintext deve ser uma string não vazia"
            )

        # Geração de valores padrão se não informados
        if not seed:
            seed = gerar_seed_decimal_aleatoria(64)

        # Gera uma seed diferente para cada passe se não houver passes fornecidos
        if not pass_:
            p = len(plaintext)
            while p > 0:
                p -= 1
                pass_.append(random.randint(min_table_leng, max_table_leng))

        # GERAÇÃO DE SEEDS DIFERENTES PARA CADA PASSE
        seeds_por_passe = []
        dict_tables_por_passe = {}

        # Usa a seed principal para gerar seeds únicas para cada passe
        random.seed(seed)
        for i, passe in enumerate(pass_):
            # Gera uma seed única para este passe baseada na seed principal + índice do passe
            seed_passe = seed * 1000000 + passe
            seeds_por_passe.append(seed_passe)

            # Gera tabelas específicas para este passe
            dict_tables_passe = gerar_tabelas(seed_passe, [passe])[0]
            dict_tables_por_passe[passe] = dict_tables_passe[passe]

        # Restaura o estado aleatório
        random.seed()

        # Variáveis principais
        crude_ciphertext_list = []
        used_passes_sequence: list[int] = []
        invalid_characters_list = []
        control_index = 0
        control_key = len(pass_) - 1

        # Funções internas auxiliares
        def enciphering(caracter: str) -> None:
            """Mapeia um caractere para a substituição correspondente"""
            nonlocal control_index
            try:
                # Obtém o passe atual e suas tabelas correspondentes
                passe_atual = pass_[control_index]
                tabela_atual = dict_tables_por_passe[passe_atual]

                cipher_char = tabela_atual[caracter]
                if debug_mode:
                    crude_ciphertext_list.append(cor["gre"] + cipher_char + cor["pad"])
                else:
                    crude_ciphertext_list.append(cipher_char)
                used_passes_sequence.append(passe_atual)
            except KeyError:
                invalid_characters_list.append(caracter)

        def create_salt(
            ciphertext_list: list, current_pass: list, current_seed: int
        ) -> tuple:
            """Insere salt no ciphertext para aumentar entropia usando seeds determinísticas"""
            salt_ciphertext_list = ciphertext_list.copy()
            salt_passes = current_pass.copy()
            posicoes = []
            salt_leng = random.randint(20, 20 + len(ciphertext_list))

            # Usa a seed principal para gerar seeds únicas para cada salt
            random.seed(current_seed)

            for salt_index in range(salt_leng):
                salt_pass = random.randint(min_table_leng, max_table_leng)
                posicao = random.randint(0, len(salt_ciphertext_list) - 1)

                # Gera seed única para este salt baseada na seed principal + índice do salt
                seed_salt = current_seed + (salt_index * 100000) + salt_pass + posicao

                # Gera tabelas específicas para este salt
                tb = gerar_tabelas(seed_salt, [salt_pass])
                random_char = chr(random.randint(65, 90))

                if debug_mode:
                    salt_passes.insert(
                        posicao, cor["red"] + str(salt_pass).zfill(3) + cor["pad"]
                    )
                    salt_ciphertext_list.insert(
                        posicao,
                        cor["red"] + tb[0][salt_pass][random_char] + cor["pad"],
                    )
                    posicoes.append(
                        cor["cya"] + str(len(str(posicao))).zfill(3) + cor["pad"]
                    )
                    posicoes.append(cor["yel"] + str(posicao) + cor["pad"])
                else:
                    salt_passes.insert(posicao, salt_pass)
                    salt_ciphertext_list.insert(posicao, tb[0][salt_pass][random_char])
                    posicoes.append(str(len(str(posicao))).zfill(3))
                    posicoes.append(str(posicao))

            # Restaura o estado aleatório
            random.seed()

            return (salt_ciphertext_list, salt_passes, posicoes)

        def key_generator(
            passes_list: list,
            current_seed: int,
            seeds_passes: list = None,
            salt_positions: list = None,
            padding: str = "",
            ct_len_before_padding: int | None = None,
        ) -> tuple:
            """Gera chave polida para descriptografia posterior"""
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
            if debug_mode:
                seed_value = cor["blu"] + seed_value + cor["pad"]
                pl = cor["mag"] + pl + cor["pad"]
                lolp = cor["mag"] + lolp + cor["pad"]
                sl = cor["mag"] + sl + cor["pad"]
                salt_l = [cor["mag"] + s + cor["pad"] for s in salt_l]
                lol_salt = [cor["mag"] + s + cor["pad"] for s in lol_salt]
                poli_passes = [cor["gre"] + p + cor["pad"] for p in poli_passes]
                poli_seeds = [cor["yel"] + p + cor["pad"] for p in poli_seeds]
                poli_salt = [cor["red"] + p + cor["pad"] for p in poli_salt]

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
            polished_key = "".join(
                [
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
                ]
            )

            return (poli_passes, polished_key, crude_key)

        # Processo de criptografia principal
        for caracter in plaintext:
            enciphering(caracter)
            control_index = 0 if control_index == control_key else control_index + 1

        # Aplicação do salt e geração da chave
        if not no_salt:
            salt_result = create_salt(crude_ciphertext_list, used_passes_sequence, seed)
            ciphertext = "".join(salt_result[0])

            if (len(ciphertext) % 20) == 0:
                key_result = key_generator(
                    passes_list=salt_result[1],
                    current_seed=seed,
                    seeds_passes=seeds_por_passe,
                    salt_positions=salt_result[2],
                    ct_len_before_padding=len(ciphertext),
                )
            else:
                padding = ((len(ciphertext) % 20) - 20) * -1
                ciphertext += padding * "1"
                key_result = key_generator(
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
                key_result = key_generator(
                    passes_list=used_passes_sequence,
                    current_seed=seed,
                    seeds_passes=seeds_por_passe,
                    ct_len_before_padding=len(ciphertext),
                )
            else:
                padding = ((len(ciphertext) % 20) - 20) * -1
                ciphertext += padding * "1"
                key_result = key_generator(
                    passes_list=used_passes_sequence,
                    current_seed=seed,
                    seeds_passes=seeds_por_passe,
                    padding=str(padding),
                    ct_len_before_padding=len(ciphertext) - padding,
                )

        # Saída final
        if debug_mode:
            print(
                f"\nPlaintext: {cor['blu'] + plaintext + cor['pad']}\n\n"
                f"Ciphertext_list: {', '.join(p for p in crude_ciphertext_list) if no_salt else ', '.join(p for p in salt_result[0])}\n\n"
                f"Seeds por passe: {seeds_por_passe}\n\n"
                f"Crude key: {key_result[2]}\n\n"
                f"Polished key: {key_result[1]}\n\n"
                f"Invalid characters: {invalid_characters_list}\n\n"
                f"Ciphertext: {ciphertext}\n\n"
            )
            return
        else:
            raw_ciphertext = ciphertext
            compressed = self.compression(ciphertext)
            self._info = [
                compressed,  # texto comprimido
                key_result[1],  # chave
                ciphertext,  # texto cifrado não comprimido
                plaintext,  # texto original
                pass_,  # passes
                seed,  # seed
            ]

            if compress_text:
                ciphertext = compressed

            if printar:
                print(f"Ciphertext:\n{ciphertext}")
                print(f"\nKey:\n{key_result[1]}")

            if retonar:
                return [raw_ciphertext, key_result[1]]

    # Receives a compressed cipher text and returns the decrypted text (plain text / original message).
    def decrypt(self, ciphertext, key, printar: bool = False, retonar: bool = False):
        self._info[1] = key
        
        is_compressed = False

        for char in ciphertext:
            if char not in ["0", "1"]:
                is_compressed = True
                break
        
        # Ciphertext já é o texto cifrado direto (sem compressão binária)
        # Se valores não vierem, tenta usar estado interno (quando disponível)
        if (ciphertext is None or ciphertext == "") or (key is None or key == ""):
            if self._info is not None:
                if ciphertext is None or ciphertext == "":
                    ciphertext = self._info[0]
                if key is None or key == "":
                    key = self._info[1]
        # Valida após possível fallback
        if ciphertext is None or key is None or ciphertext == "" or key == "":
            raise ValueError(
                "ciphertext e/ou key ausentes. Gere com encrypt_ (sem debug) ou forneça valores válidos."
            )
        if not isinstance(ciphertext, str) or not isinstance(key, str):
            raise ValueError("ciphertext e key devem ser strings.")

        # Remove possíveis sequências ANSI (modo debug) de ciphertext e key
        def _remove_ansi(s: str) -> str:
            return re.sub(r"\x1b\[[0-9;]*m", "", s)

        ciphertext = _remove_ansi(ciphertext)
        key = _remove_ansi(key)

        def dechaveador(ciphertext: str = "", key: str = ""):
            if not ciphertext:
                raise ValueError("Coloque um ciphertext valído")
            if not key:
                raise ValueError("Coloque uma chave valída")

            def parse_com_salt(k: str):
                ptr_local = 0
                if len(k) < 3:
                    raise ValueError("Chave inválida: incompleta (lol_salt)")
                lol_salt_local = int(k[ptr_local : ptr_local + 3])
                ptr_local += 3

                if lol_salt_local == 0:
                    salt_l_local = 0
                else:
                    if len(k) < ptr_local + lol_salt_local:
                        raise ValueError("Chave inválida: incompleta (salt_l)")
                    salt_l_local = int(k[ptr_local : ptr_local + lol_salt_local])
                    ptr_local += lol_salt_local

                posicoes_local = []
                for _ in range(salt_l_local):
                    if len(k) < ptr_local + 3:
                        raise ValueError("Chave inválida: incompleta (len posicao)")
                    pn_len = int(k[ptr_local : ptr_local + 3])
                    ptr_local += 3
                    if pn_len < 0:
                        raise ValueError("Chave inválida: tamanho de posição negativo")
                    if len(k) < ptr_local + pn_len:
                        raise ValueError("Chave inválida: incompleta (posicao)")
                    posicoes_local.append(int(k[ptr_local : ptr_local + pn_len]))
                    ptr_local += pn_len

                # lê salt_flag
                if len(k) < ptr_local + 3:
                    raise ValueError("Chave inválida: incompleta (lsf)")
                lsf_local = int(k[ptr_local : ptr_local + 3])
                ptr_local += 3
                if lsf_local != 1 or len(k) < ptr_local + lsf_local:
                    raise ValueError("Chave inválida: incompleta (sf)")
                salt_flag_local = k[ptr_local : ptr_local + lsf_local]
                ptr_local += lsf_local

                if len(k) < ptr_local + 3:
                    raise ValueError("Chave inválida: incompleta (lol_p)")
                lol_p_local = int(k[ptr_local : ptr_local + 3])
                ptr_local += 3

                if lol_p_local == 0:
                    pl_local = 0
                else:
                    if len(k) < ptr_local + lol_p_local:
                        raise ValueError("Chave inválida: incompleta (pl)")
                    pl_local = int(k[ptr_local : ptr_local + lol_p_local])
                    ptr_local += lol_p_local

                passes_local = []
                for _ in range(pl_local):
                    if len(k) < ptr_local + 3:
                        raise ValueError("Chave inválida: incompleta (pass)")
                    passes_local.append(int(k[ptr_local : ptr_local + 3]))
                    ptr_local += 3

                # novo: comprimento do ciphertext antes do padding
                if len(k) < ptr_local + 3:
                    raise ValueError("Chave inválida: incompleta (lcl)")
                lcl_local = int(k[ptr_local : ptr_local + 3])
                ptr_local += 3
                if lcl_local < 0 or len(k) < ptr_local + lcl_local:
                    raise ValueError("Chave inválida: incompleta (cl)")
                cl_local = int(k[ptr_local : ptr_local + lcl_local])
                ptr_local += lcl_local

                if len(k) < ptr_local + 3:
                    raise ValueError("Chave inválida: incompleta (sl)")
                sl_local = int(k[ptr_local : ptr_local + 3])
                ptr_local += 3
                if sl_local < 0 or len(k) < ptr_local + sl_local:
                    raise ValueError("Chave inválida: incompleta (seed)")
                seed_local = int(k[ptr_local : ptr_local + sl_local])
                ptr_local += sl_local

                padding_local = 0
                if ptr_local < len(k):
                    restante = k[ptr_local:]
                    if restante:
                        padding_local = int(restante)

                # aplica padding e ajusta pelo comprimento declarado
                ct_eff = ciphertext
                if padding_local > 0:
                    if padding_local > len(ct_eff):
                        raise ValueError("Padding maior que o tamanho do ciphertext")
                    ct_eff = ct_eff[: len(ct_eff) - padding_local]
                if 'cl_local' in locals() and cl_local > 0 and len(ct_eff) != cl_local:
                    if len(ct_eff) > cl_local:
                        ct_eff = ct_eff[:cl_local]
                    else:
                        # tolera entradas comprimidas que resultem em ajuste
                        if started_with_compressed:
                            pass
                        else:
                            raise ValueError("Ciphertext menor que o comprimento declarado")

                # valida soma e ajusta tolerantemente para entradas comprimidas
                total_len = len(ct_eff)
                sum_passes = sum(passes_local)
                if sum_passes != total_len:
                    if started_with_compressed and passes_local:
                        delta = sum_passes - total_len
                        passes_local[-1] -= delta
                        if passes_local[-1] < 0:
                            passes_local[-1] = 0
                    else:
                        raise ValueError(
                            "inconsistência entre passes e ciphertext (com salt)"
                        )

                # segmenta
                ciphertext_list_local = []
                resto_local = ct_eff
                for comp in passes_local:
                    ciphertext_list_local.append(resto_local[:comp])
                    resto_local = resto_local[comp:]

                # remove sal apenas se flag ativa e houver posições
                if salt_flag_local == "1" and posicoes_local:
                    for pos in reversed(posicoes_local):
                        if 0 <= pos < len(ciphertext_list_local):
                            del ciphertext_list_local[pos]
                            del passes_local[pos]

                return passes_local, seed_local, ciphertext_list_local

            def parse_sem_salt(k: str):
                ptr_local = 0
                # lê salt_flag (mesmo sem salt, flag deve existir)
                if len(k) < 3:
                    raise ValueError("Chave inválida: incompleta (lsf)")
                lsf_local = int(k[ptr_local : ptr_local + 3])
                ptr_local += 3
                if lsf_local != 1 or len(k) < ptr_local + lsf_local:
                    raise ValueError("Chave inválida: incompleta (sf)")
                salt_flag_local = k[ptr_local : ptr_local + lsf_local]
                ptr_local += lsf_local

                # aqui o início já é lol_p
                if len(k) < 3:
                    raise ValueError("Chave inválida: incompleta (lol_p)")
                lol_p_local = int(k[ptr_local : ptr_local + 3])
                ptr_local += 3

                if lol_p_local == 0:
                    pl_local = 0
                else:
                    if len(k) < ptr_local + lol_p_local:
                        raise ValueError("Chave inválida: incompleta (pl)")
                    pl_local = int(k[ptr_local : ptr_local + lol_p_local])
                    ptr_local += lol_p_local

                passes_local = []
                for _ in range(pl_local):
                    if len(k) < ptr_local + 3:
                        raise ValueError("Chave inválida: incompleta (pass)")
                    passes_local.append(int(k[ptr_local : ptr_local + 3]))
                    ptr_local += 3

                # novo: comprimento do ciphertext antes do padding
                if len(k) < ptr_local + 3:
                    raise ValueError("Chave inválida: incompleta (lcl)")
                lcl_local = int(k[ptr_local : ptr_local + 3])
                ptr_local += 3
                if lcl_local < 0 or len(k) < ptr_local + lcl_local:
                    raise ValueError("Chave inválida: incompleta (cl)")
                cl_local = int(k[ptr_local : ptr_local + lcl_local])
                ptr_local += lcl_local

                if len(k) < ptr_local + 3:
                    raise ValueError("Chave inválida: incompleta (sl)")
                sl_local = int(k[ptr_local : ptr_local + 3])
                ptr_local += 3
                if sl_local < 0 or len(k) < ptr_local + sl_local:
                    raise ValueError("Chave inválida: incompleta (seed)")
                seed_local = int(k[ptr_local : ptr_local + sl_local])
                ptr_local += sl_local

                padding_local = 0
                if ptr_local < len(k):
                    restante = k[ptr_local:]
                    if restante:
                        padding_local = int(restante)

                ct_eff = ciphertext
                if padding_local > 0:
                    if padding_local > len(ct_eff):
                        raise ValueError("Padding maior que o tamanho do ciphertext")
                    ct_eff = ct_eff[: len(ct_eff) - padding_local]
                if 'cl_local' in locals() and cl_local > 0 and len(ct_eff) != cl_local:
                    if len(ct_eff) > cl_local:
                        ct_eff = ct_eff[:cl_local]
                    else:
                        if started_with_compressed:
                            pass
                        else:
                            raise ValueError("Ciphertext menor que o comprimento declarado")

                # valida soma e ajusta tolerantemente para entradas comprimidas
                total_len = len(ct_eff)
                sum_passes = sum(passes_local)
                if sum_passes != total_len:
                    if started_with_compressed and passes_local:
                        delta = sum_passes - total_len
                        passes_local[-1] -= delta
                        if passes_local[-1] < 0:
                            passes_local[-1] = 0
                    else:
                        raise ValueError(
                            "inconsistência entre passes e ciphertext (sem salt)"
                        )


                ciphertext_list_local = []
                resto_local = ct_eff
                for comp in passes_local:
                    ciphertext_list_local.append(resto_local[:comp])
                    resto_local = resto_local[comp:]

                return passes_local, seed_local, ciphertext_list_local

            # Tenta primeiro com o formato que contém seção de salt; se falhar, tenta sem salt
            try:
                return parse_com_salt(key)
            except Exception:
                return parse_sem_salt(key)
        
        # Se o texto está comprimido, descomprime e salva ambas as versões
        if is_compressed:
            self._info[0] = ciphertext  # salva o texto comprimido
            decompressed = self.decompression(ciphertext)
            self._info[2] = decompressed  # salva o texto descomprimido
            ciphertext = decompressed  # atualiza o texto para descriptografia
        else:
            # Se não está comprimido, comprime e salva ambas as versões
            self._info[2] = ciphertext  # salva o texto não comprimido
            self._info[0] = self.compression(ciphertext)  # salva a versão comprimida

        started_with_compressed = is_compressed

        desc = dechaveador(ciphertext, key)

        pass_ = desc[0]
        seed = desc[1]
        cipher = desc[2]

        self._info[4] = pass_
        self._info[5] = seed

        plaintext = []

        # GERAÇÃO DE SEEDS DIFERENTES PARA CADA PASSE
        seeds_por_passe = []
        dict_tables_por_passe = {}

        # Usa a seed principal para gerar seeds únicas para cada passe
        for i, passe in enumerate(pass_):
            # Gera uma seed única para este passe baseada na seed principal + índice do passe
            seed_passe = seed * 1000000 + passe
            seeds_por_passe.append(seed_passe)

            # Gera tabelas específicas para este passe
            dict_tables_passe = gerar_tabelas(seed_passe, [passe])[1]
            dict_tables_por_passe[passe] = dict_tables_passe[passe]
        for n, p in enumerate(pass_):
            val = cipher[n]
            inv = dict_tables_por_passe[p]
            if val in inv:
                plaintext.append(inv[val])
            else:
                print("MISS idx=", n, "pass=", p, "len=", len(val))
                print("invalida: ", val)

        plaintext = "".join(plaintext)

        self._info[3] = plaintext

        if printar:
            print(f"Plaintext:\n{plaintext}")

        if retonar:
            return plaintext
