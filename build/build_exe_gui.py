"""
Script para construir o executável .exe do HashChain (versão GUI).
Execute: python build_exe_gui.py
"""
import subprocess
import sys
import os
from pathlib import Path

def build_exe_gui():
    """Constrói o executável da GUI usando PyInstaller."""
    
    print("🔨 Iniciando construção do executável HashChain (GUI)...")
    print("=" * 60)
    
    # Verifica se PyInstaller está instalado
    try:
        import PyInstaller
        print("✅ PyInstaller encontrado")
    except ImportError:
        print("❌ PyInstaller não está instalado!")
        print("📦 Instalando PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller instalado com sucesso!")
    
    # Caminhos (ajustados para funcionar a partir da pasta build)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent  # Sobe um nível para a raiz do projeto
    main_gui_script = script_dir / "main_gui.py"  # main_gui.py está na pasta build
    icon_path = project_root / "icon.ico"  # Opcional
    
    if not main_gui_script.exists():
        print("❌ Arquivo main_gui.py não encontrado!")
        print("💡 Criando main_gui.py...")
        main_gui_content = '''"""
Ponto de entrada alternativo que sempre abre a GUI.
"""
import sys

if __name__ == "__main__":
    try:
        from hashchain.interfaces import run
        run()
    except Exception as e:
        try:
            import tkinter.messagebox as mb
            mb.showerror("Erro", f"Não foi possível iniciar a interface gráfica.\\n\\nErro: {e}")
        except:
            pass
'''
        main_gui_script.write_text(main_gui_content, encoding='utf-8')
        print("✅ Arquivo main_gui.py criado")
    
    # Comando PyInstaller
    cmd = [
        "pyinstaller",
        "--name=HashChain",
        "--onefile",  # Arquivo único
        "--windowed",  # Sem console (para GUI)
        "--clean",  # Limpa cache antes de construir
        "--noconfirm",  # Não pergunta para sobrescrever
    ]
    
    # Adiciona ícone se existir
    if icon_path.exists():
        cmd.extend(["--icon", str(icon_path)])
        print(f"✅ Ícone encontrado: {icon_path}")
    else:
        print("ℹ️  Ícone não encontrado (icon.ico), continuando sem ícone...")
    
    # Adiciona dados adicionais
    if (project_root / "config.json").exists():
        config_path = project_root / "config.json"
        cmd.extend(["--add-data", f"{config_path}{os.pathsep}."])
    
    # Hidden imports
    cmd.extend([
        "--hidden-import", "customtkinter",
        "--hidden-import", "tkinter",
        "--hidden-import", "hashchain",
        "--hidden-import", "hashchain.core",
        "--hidden-import", "hashchain.core.encryption",
        "--hidden-import", "hashchain.core.decryption",
        "--hidden-import", "hashchain.core.compression",
        "--hidden-import", "hashchain.core.key_generator",
        "--hidden-import", "hashchain.tables",
        "--hidden-import", "hashchain.tables.table_generator",
        "--hidden-import", "hashchain.utils",
        "--hidden-import", "hashchain.utils.colors",
        "--hidden-import", "hashchain.utils.handler",
        "--hidden-import", "hashchain.utils.input_collector",
        "--hidden-import", "hashchain.config",
        "--hidden-import", "hashchain.config.config_manager",
        "--hidden-import", "hashchain.interfaces",
        "--hidden-import", "hashchain.interfaces.gui",
        "--collect-all", "customtkinter",  # Coleta todos os recursos do customtkinter
    ])
    
    # Script principal (main_gui.py que sempre abre GUI)
    cmd.append(str(main_gui_script))
    
    print("\n📋 Comando PyInstaller:")
    print(" ".join(cmd))
    print("\n" + "=" * 60)
    print("🚀 Iniciando construção...\n")
    
    try:
        # Executa PyInstaller
        subprocess.check_call(cmd)
        
        print("\n" + "=" * 60)
        print("✅ Executável construído com sucesso!")
        dist_path = project_root / 'dist' / 'HashChain.exe'
        print(f"📁 Localização: {dist_path}")
        print("\n💡 Dica: O executável está na pasta 'dist' na raiz do projeto")
        print("💡 Este executável abre diretamente a interface gráfica")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erro ao construir executável: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    build_exe_gui()

