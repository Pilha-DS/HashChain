# Guia de Construção do Executável HashChain

Este guia explica como criar um executável `.exe` do HashChain para Windows.

## Pré-requisitos

1. **Python 3.8+** instalado
2. **Todas as dependências instaladas**:
   ```bash
   pip install -r requirements.txt
   ```

## Método 1: Script Automatizado (Recomendado)

**Nota:** Os scripts de build estão na pasta `build/`. Execute a partir da raiz do projeto:

### Para versão completa (Terminal + GUI):

```bash
python build/build_exe.py
```

### Para versão apenas GUI (recomendado para .exe):

```bash
python build/build_exe_gui.py
```

**Nota:** Esta versão sempre abre a interface gráfica diretamente, ideal para distribuição como executável.

## Método 2: Usando arquivo .spec

1. Instale o PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Execute a partir da pasta build:
   ```bash
   cd build
   pyinstaller HashChain.spec
   ```

   Ou da raiz do projeto:
   ```bash
   pyinstaller build/HashChain.spec
   ```

## Método 3: Comando Manual

Execute a partir da raiz do projeto:

```bash
pyinstaller --name=HashChain --onefile --windowed --clean main.py
```

## Opções de Build

### Com console (para debug):
```bash
pyinstaller --name=HashChain --onefile --console --clean main.py
```

### Sem console (apenas GUI):
```bash
pyinstaller --name=HashChain --onefile --windowed --clean main.py
```

### Com ícone personalizado:
```bash
pyinstaller --name=HashChain --onefile --windowed --icon=icon.ico --clean main.py
```

## Resultado

Após a construção, o executável estará em:
```
dist/HashChain.exe
```

## Solução de Problemas

### Erro: "RuntimeError: lost sys.stdin"
**Causa:** O executável foi construído com `--windowed` (sem console), mas o código tenta usar `input()`.

**Solução:** 
- Use `build_exe_gui.py` que cria um executável que sempre abre a GUI diretamente
- Ou o código já detecta automaticamente e abre a GUI quando não há console disponível

### Erro: "ModuleNotFoundError"
- Adicione o módulo faltante com `--hidden-import`:
  ```bash
  pyinstaller --hidden-import=nome_do_modulo --onefile main.py
  ```

### Executável muito grande
- Use `--exclude-module` para excluir módulos desnecessários:
  ```bash
  pyinstaller --exclude-module=matplotlib --onefile main.py
  ```

### Erro ao executar
- Tente construir com `--console` primeiro para ver os erros
- Verifique se todos os arquivos de dados estão incluídos
- Para debug, construa com `--console` temporariamente:
  ```bash
  pyinstaller --name=HashChain --onefile --console --clean main.py
  ```

## Estrutura de Arquivos Necessários

O executável precisa incluir:
- `hashchain/` (todo o módulo)
- `config.json` (se existir)
- Templates da web (se usar interface web)

## Notas

- O executável será um arquivo único (--onefile)
- Primeira execução pode ser mais lenta (extração temporária)
- Antivírus pode alertar (falso positivo comum com PyInstaller)

