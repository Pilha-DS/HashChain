"""Coletor de inputs do usuário."""
from typing import List

from .colors import ColorFormatter


class InputCollector:
    """Classe para coletar e validar inputs do usuário."""
    
    def __init__(self):
        """Inicializa o coletor de inputs."""
        self.color = ColorFormatter()
    
    def get_seed(self) -> int:
        """
        Coleta seed do usuário com validação.
        
        Returns:
            Seed válida (int com pelo menos 8 dígitos)
        """
        seed: int = 0
        
        while len(str(seed)) < 8 or not isinstance(seed, int):
            seed_input = input(
                f"\n{self.color.RESET}{self.color.c('c', True)}Digite uma seed de no minimo 8 digitos:{self.color.RESET} "
            )
            try:
                if len(str(seed_input)) < 8:
                    raise ValueError("Seed muito curta")
                seed = int(seed_input)
            except (ValueError, TypeError):
                print(
                    f'\n{self.color.RESET}{self.color.c("y")}A seed deve ser um número inteiro '
                    f'de no minimo 8 digitos. Tente novamente.'
                )
        
        return seed
    
    def get_passes(self) -> List[int]:
        """
        Coleta passes do usuário com validação.
        
        Returns:
            Lista de passes válidos (inteiros entre 20 e 999)
        """
        def is_valid_pass(passes: List[int]) -> bool:
            """Valida lista de passes."""
            if len(passes) <= 0:
                return False
            for passo in passes:
                if not isinstance(passo, int) or passo < 20 or passo > 999:
                    return False
            return True
        
        def convert_input(raw_passes: str) -> List[int]:
            """Converte string de passes em lista de inteiros."""
            valid_chars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", " "]
            raw_passes += " "
            passes: List[int] = []
            aux: List[str] = []
            
            try:
                for char in raw_passes:
                    if char not in valid_chars:
                        raise ValueError("Caractere inválido")
                    if char != " ":
                        aux.append(char)
                    elif char == " " and aux:
                        passes.append(int("".join(aux)))
                        aux = []
            except (ValueError, TypeError):
                return [-1]
            
            return passes
        
        while True:
            raw_passes = input(
                f"\n{self.color.RESET}{self.color.c('c', True)}Digite os passos separados por espaços, "
                f"cada um sendo um inteiro de 20 a 999. {self.color.RESET}{self.color.BOLD}"
                f"(Exemplo: 20 450 999):{self.color.RESET} "
            )
            passes = convert_input(raw_passes)
            
            if is_valid_pass(passes):
                break
            
            print(
                f"\n{self.color.RESET}{self.color.c('y')}Input inválido. Passes devem ser números "
                f"inteiros de 20 a 999. Tente novamente.{self.color.RESET}"
            )
        
        return passes

