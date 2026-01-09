# Build Tools - HashChain

Esta pasta contém todos os arquivos necessários para construir o executável `.exe` do HashChain.

## Arquivos

- **`build_exe.py`** - Script para construir executável completo (Terminal + GUI)
- **`build_exe_gui.py`** - Script para construir executável apenas GUI (recomendado)
- **`main_gui.py`** - Ponto de entrada alternativo que sempre abre a GUI
- **`HashChain.spec`** - Arquivo de especificação do PyInstaller
- **`BUILD.md`** - Documentação completa sobre como construir o executável
- **`run_gui_wrapper.py`** - Wrapper auxiliar para executar a GUI

## Uso Rápido

Execute a partir da **raiz do projeto**:

```bash
# Versão GUI (recomendado)
python build/build_exe_gui.py

# Versão completa
python build/build_exe.py
```

O executável será criado em `dist/HashChain.exe` na raiz do projeto.

## Requisitos

- Python 3.8+
- PyInstaller (instalado automaticamente pelos scripts)
- Todas as dependências do projeto instaladas

Veja `BUILD.md` para documentação completa.

