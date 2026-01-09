"""
Ponto de entrada alternativo que sempre abre a GUI.
Use este arquivo para construir um executável que abre diretamente a GUI.
"""
import sys

def is_frozen():
    """Verifica se está rodando como executável PyInstaller."""
    return getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')

if __name__ == "__main__":
    try:
        from hashchain.interfaces import run
        run()
    except Exception as e:
        # Tenta mostrar erro em diálogo se possível
        try:
            import tkinter.messagebox as mb
            mb.showerror("Erro", f"Não foi possível iniciar a interface gráfica.\n\nErro: {e}")
        except:
            # Se não conseguir mostrar diálogo, tenta printar (pode não funcionar sem console)
            try:
                print(f"Erro: {e}")
            except:
                pass


