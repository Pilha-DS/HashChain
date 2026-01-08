"""Gerenciador de configuração."""
from pathlib import Path
from typing import Optional, Dict

from ..utils import Handler


class ConfigManager:
    """Classe para gerenciar configurações do sistema."""
    
    def __init__(self):
        """Inicializa o gerenciador de configuração."""
        self.handler = Handler()
        self.config_path: Optional[Path] = None
        self.config: Dict = {}
    
    def load(self) -> Dict:
        """
        Carrega configuração do arquivo.
        
        Returns:
            Dicionário com configurações
        """
        self.config_path = self.handler.find_config_file()
        self.config = self.handler.load_config(self.config_path)
        return self.config
    
    def save(self) -> None:
        """Salva configuração atual."""
        if self.config_path:
            self.handler.save_config(self.config, self.config_path)
    
    def get(self, key: str, default=None):
        """
        Obtém valor de configuração.
        
        Args:
            key: Chave da configuração
            default: Valor padrão se não encontrado
            
        Returns:
            Valor da configuração ou default
        """
        return self.config.get(key, default)
    
    def set(self, key: str, value) -> None:
        """
        Define valor de configuração.
        
        Args:
            key: Chave da configuração
            value: Valor a ser definido
        """
        self.config[key] = value

