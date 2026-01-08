"""Handler para operações de sistema e arquivos."""
import os
import json
import importlib.util
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox
from typing import Optional, List

from .colors import ColorFormatter


class Handler:
    """Classe para operações de sistema, arquivos e configuração."""
    
    EXPECTED_CONFIG_ID = 25599852140000
    
    def __init__(self):
        """Inicializa o handler."""
        self.color = ColorFormatter()
    
    @staticmethod
    def clear_terminal() -> None:
        """Limpa o terminal."""
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
    
    def find_config_file(self) -> Optional[Path]:
        """
        Procura arquivo de configuração no diretório atual e subdiretórios.
        
        Returns:
            Path do arquivo de configuração ou None se não encontrado
        """
        start_path = Path(".")
        for path in start_path.rglob("config.json"):
            try:
                with open(path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    if data.get("idd") == self.EXPECTED_CONFIG_ID:
                        print(
                            f"\n{self.color.c('g')}Arquivo de configuração encontrado em: "
                            f"{self.color.ITALIC}{self.color.BOLD}{path}{self.color.RESET}"
                        )
                        return path
                    else:
                        print(
                            f"{self.color.format(bold=True, faint=True)}Ignorando {path}, "
                            f"id diferente ({data.get('idd')}).{self.color.RESET}"
                        )
            except (json.JSONDecodeError, OSError) as e:
                print(f"{self.color.c('r', True)}Erro ao ler {path}: {e}")
        
        print(
            f"\n{self.color.c('y', bold=True)}Aviso:{self.color.RESET} "
            f"{self.color.c('y', True, faint=True)}O arquivo de configurações "
            f"{self.color.c('y')}'config.json'{self.color.c('y', True, faint=True)} "
            f"não foi encontrado no diretório.{self.color.RESET}"
        )
        print(
            f"{self.color.c('y', italic=True)} - As opções de criptografia padronizadas "
            f"não estarão disponíveis.{self.color.RESET}"
        )
        return None
    
    def load_config(self, config_path: Optional[Path]) -> dict:
        """
        Carrega configuração do arquivo.
        
        Args:
            config_path: Caminho do arquivo de configuração
            
        Returns:
            Dicionário com configurações
        """
        if config_path is None:
            config = {"terminal_mode": True}
            return config
        
        try:
            with open(config_path, "r") as config_file:
                config = json.load(config_file)
                print(f"{self.color.c('g', italic=True)} - Configurações carregadas com sucesso.{self.color.RESET}")
                return config
        except FileNotFoundError:
            print(
                f" - {self.color.ITALIC}Erro: O arquivo de configurações "
                f"{self.color.BOLD}'config.json' não foi encontrado no diretório.{self.color.RESET}"
            )
        except json.JSONDecodeError:
            print(
                f" - {self.color.ITALIC}Erro: Falha ao decodificar o arquivo "
                f"{self.color.BOLD}'config.json'.{self.color.RESET} Verifique sua integridade."
            )
        return {"terminal_mode": True}
    
    @staticmethod
    def verify_required_modules() -> bool:
        """
        Verifica se os módulos necessários estão instalados.
        
        Returns:
            True se todos os módulos estão instalados, False caso contrário
        """
        dependencies = [
            "tkinter", "customtkinter", "os", "json", "secrets",
            "pathlib", "datetime", "subprocess"
        ]
        color = ColorFormatter()
        
        for module in dependencies:
            if importlib.util.find_spec(module) is not None:
                print(f"{color.c('g')}Atualmente o módulo {color.BOLD}{module}{color.RESET}{color.c('g')} está instalado.{color.RESET}")
            else:
                print(
                    f"{color.c('r')}Atualmente o módulo {color.c('r', bold=True)}{module} não está instalado"
                    f"{color.c('r')}, rode o seguinte comando no terminal para instalar:"
                    f" pip install {color.BOLD}{module}{color.RESET}"
                )
        
        has_dependencies = all(
            importlib.util.find_spec(module) is not None for module in dependencies
        )
        
        if not has_dependencies:
            print(
                f"{color.ITALIC}\nPara instalar utilizando o {color.BOLD}pip{color.ITALIC}, "
                f"é necessário ter o pip {color.BOLD}instalado e configurado no PATH do sistema.{color.RESET}"
            )
            print(
                f"\n {color.ITALIC}- Por opção dos criadores, decidimos não forçar a instalação "
                f"do pip e dos módulos necessários para utilização a interface gráfica, pois, "
                f"consideramos essa prática como {color.BOLD}intrusiva{color.RESET},{color.ITALIC} "
                f"e acreditamos que o usuário deve ter controle sobre o que é instalado em seu sistema."
            )
        
        return has_dependencies
    
    def save_config(self, config: dict, config_path: Optional[Path]) -> None:
        """
        Salva configuração em arquivo.
        
        Args:
            config: Dicionário com configurações
            config_path: Caminho do arquivo de configuração
        """
        if config_path is None:
            print("Programa encerrado.")
            raise SystemExit
        
        try:
            with open(config_path, "w") as config_file:
                json.dump(config, config_file, indent=4)
        except FileNotFoundError:
            print(
                f"{self.color.RESET}{self.color.c('y', True)}Aviso: O arquivo de configurações "
                f"'config.json' não foi encontrado no diretório.{self.color.RESET}"
            )
        except json.JSONDecodeError:
            print(
                f"{self.color.RESET}{self.color.c('r', True)}Erro: Falha ao decodificar o arquivo "
                f"'config.json'. Verifique sua integridade.{self.color.RESET}"
            )
        
        print(f"\n{self.color.RESET}{self.color.format(faint=True)}Programa encerrado.{self.color.RESET}\n")
        raise SystemExit
    
    @staticmethod
    def find_outputs_folder() -> Optional[str]:
        """
        Procura a pasta 'outputs' a partir do diretório atual.
        
        Returns:
            Caminho completo da pasta ou None se não encontrada
        """
        current_dir = os.getcwd()
        
        while True:
            for root, dirs, files in os.walk(current_dir):
                if 'outputs' in dirs:
                    return os.path.join(root, 'outputs')
            parent = os.path.dirname(current_dir)
            if parent == current_dir:
                color = ColorFormatter()
                print(f"{color.RESET}{color.c('r')}Erro: Pasta 'outputs' não encontrada.{color.RESET}")
                return None
            current_dir = parent
    
    @staticmethod
    def list_output_files() -> Optional[List[str]]:
        """
        Lista arquivos na pasta 'outputs' do projeto.
        
        Returns:
            Lista de nomes de arquivos ou None se pasta não encontrada
        """
        color = ColorFormatter()
        current_dir = os.getcwd()
        
        while True:
            try:
                if "HashChain---encryption" in os.listdir(current_dir):
                    project_root = os.path.join(current_dir, "HashChain---encryption")
                    break
            except (OSError, PermissionError):
                pass
            
            parent = os.path.dirname(current_dir)
            if parent == current_dir:
                raise FileNotFoundError(
                    f"{color.RESET}{color.c('r')}A pasta 'HashChain---encryption' não foi encontrada.{color.RESET}"
                )
            current_dir = parent
        
        outputs_path = os.path.join(project_root, "outputs")
        
        if not os.path.exists(outputs_path):
            print(
                f"\n{color.RESET}{color.c('r')}A pasta 'outputs' não pode ser encontrada em seu diretório: "
                f"{outputs_path}{color.RESET}"
            )
            print("\nUtilize a encriptação e opte por salvar os resultados em um arquivo de log para que sua pasta seja criada.")
            return None
        
        files = [
            f for f in os.listdir(outputs_path)
            if os.path.isfile(os.path.join(outputs_path, f))
        ]
        
        return files
    
    @staticmethod
    def read_file() -> Optional[str]:
        """
        Abre diálogo para seleção e leitura de arquivo de texto.
        
        Returns:
            Conteúdo do arquivo ou None se cancelado
        """
        color = ColorFormatter()
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        root.update()
        
        file_path = filedialog.askopenfilename(
            title="Selecione um arquivo para ler",
            filetypes=(("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*"))
        )
        
        if file_path:
            print(f"\n{color.RESET}{color.c('g')}Arquivo selecionado: {Path(file_path)}")
            with open(file_path, 'r', encoding='utf-8') as arquivo:
                content = arquivo.read()
            root.destroy()
            return content
        
        root.destroy()
        return None
    
    @staticmethod
    def save_file(text: str) -> None:
        """
        Abre diálogo para salvar texto em arquivo.
        
        Args:
            text: Texto a ser salvo
        """
        color = ColorFormatter()
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        
        path = filedialog.asksaveasfilename(
            title="Escolha onde salvar o arquivo",
            initialfile="output.txt",
            defaultextension=".txt",
            filetypes=(("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*"))
        )
        
        root.destroy()
        
        if path:
            try:
                with open(path, "w", encoding="utf-8") as arquivo:
                    arquivo.write(text)
                messagebox.showinfo("Sucesso", f"Arquivo salvo em:\n{path}")
                print(f'\n{color.RESET}{color.c("g")}Texto salvo com sucesso em: {color.ITALIC}{Path(path)}{color.RESET}')
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar o arquivo:\n{e}")
        else:
            print(f"\n{color.RESET}{color.c('y')}Aviso: O arquivo não foi salvo, nenhum local foi selecionado.{color.RESET}")
    
    @staticmethod
    def print_menu(menu_list: List[str]) -> None:
        """
        Imprime menu formatado.
        
        Args:
            menu_list: Lista de itens do menu
        """
        color = ColorFormatter()
        for i, txt in enumerate(menu_list):
            print(f'{color.format(bold=True, faint=True)}{i + 1}. {color.RESET}{txt}{color.RESET}')

