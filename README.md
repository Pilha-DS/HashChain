<img src="https://img.shields.io/badge/Python-3.8+-blue.svg">
<img src="https://img.shields.io/badge/License-MIT-green.svg">

# HashChain Encryption (HCC)

HashChain é um esquema de criptografia por cadeias de substituição determinísticas com inserção opcional de salt, implementado em Python. Ele gera tabelas de substituição por passe a partir de uma seed principal e permite reverter o processo com uma chave compacta que embute toda a informação necessária para a descriptografia.

## 📋 Sumário

- [Visão Geral](#visão-geral)
- [Características](#características)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Uso](#uso)
  - [Interface de Linha de Comando (CLI)](#interface-de-linha-de-comando-cli)
  - [Interface Gráfica (GUI)](#interface-gráfica-gui)
  - [Interface Web](#interface-web)
  - [Uso Programático](#uso-programático)
- [Conceitos-Chave](#conceitos-chave)
- [API Completa](#api-completa)
- [Formato da Chave](#formato-da-chave)
- [Construindo o Executável](#construindo-o-executável)
- [Configuração](#configuração)
- [Boas Práticas](#boas-práticas)
- [Contribuindo](#contribuindo)
- [Licença](#licença)

## 🎯 Visão Geral

HashChain Encryption é um sistema de criptografia que utiliza:

- **Substituição determinística:** Para cada caractere do texto plano, é aplicada uma substituição conforme tabelas geradas a partir de uma seed e dos passes.
- **Múltiplos passes:** O texto é segmentado por uma sequência de comprimentos (passes). Cada parte usa uma tabela específica.
- **Salt opcional:** Itens aleatórios (determinísticos via seed) podem ser inseridos no ciphertext para elevar a entropia e ofuscação. As posições do salt são codificadas na chave.
- **Chave compacta:** A chave gerada guarda comprimentos, passes, seed, e metadados de salt/padding, permitindo a descriptografia completa.

## ✨ Características

- 🔐 Criptografia determinística baseada em seed
- 🔑 Geração automática de chaves compactas
- 🧂 Suporte opcional a salt para maior segurança
- 📦 Compressão de texto binário integrada
- 🖥️ Interface de linha de comando completa
- 🎨 Interface gráfica moderna (CustomTkinter)
- 🌐 Interface web (Flask)
- 📱 Executável standalone (.exe) para Windows
- 🧪 Testes unitários completos
- 📚 Documentação detalhada

## 📦 Requisitos

- **Python 3.8+** (testado em Python 3.11 e 3.13)
- **Bibliotecas externas:**
  - `customtkinter >= 5.2.0` (para interface gráfica)
  - `flask >= 2.3.0` (para interface web, opcional)
  - `pyinstaller >= 5.13.0` (para construir executável, opcional)

## 🚀 Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/SEU-USER/HashChain---encryption.git
cd HashChain---encryption
```

### 2. Instalar dependências

```bash
# Instalar todas as dependências
pip install -r hashchain/Libraries/requirements.txt

# Ou instalar manualmente
pip install customtkinter flask pyinstaller
```

### 3. Verificar instalação

```bash
python main.py
```

## 📁 Estrutura do Projeto

```
HashChain---encryption/
├── hashchain/                    # Pacote principal
│   ├── __init__.py              # Exporta classe HashChain
│   ├── hashchain.py             # Classe principal HashChain
│   ├── core/                    # Módulos principais
│   │   ├── __init__.py
│   │   ├── compression.py       # Compressão/Descompressão
│   │   ├── encryption.py        # Criptografia
│   │   ├── decryption.py        # Descriptografia
│   │   └── key_generator.py     # Geração de chaves
│   ├── tables/                  # Geração de tabelas
│   │   ├── __init__.py
│   │   └── table_generator.py   # Gerador de tabelas determinísticas
│   ├── utils/                   # Utilitários
│   │   ├── __init__.py
│   │   ├── colors.py            # Formatação de cores no terminal
│   │   ├── handler.py           # Operações de sistema e arquivos
│   │   └── input_collector.py   # Coleta de inputs do usuário
│   ├── config/                  # Configuração
│   │   ├── __init__.py
│   │   └── config_manager.py    # Gerenciador de configuração
│   ├── interfaces/              # Interfaces de usuário
│   │   ├── __init__.py
│   │   ├── gui.py               # Interface gráfica (CustomTkinter)
│   │   └── web/                 # Interface web
│   │       ├── __init__.py
│   │       ├── app.py           # Aplicação Flask
│   │       └── templates/       # Templates HTML
│   │           └── index.html
│   └── Libraries/
│       └── requirements.txt     # Dependências do projeto
├── build/                       # Ferramentas de build
│   ├── build_exe.py             # Script para executável completo
│   ├── build_exe_gui.py         # Script para executável GUI
│   ├── main_gui.py             # Ponto de entrada GUI
│   ├── HashChain.spec          # Especificação PyInstaller
│   └── BUILD.md                # Documentação de build
├── main.py                      # Script principal (CLI)
├── config.json                  # Arquivo de configuração
└── README.md                    # Este arquivo
```

## 💻 Uso

### Interface de Linha de Comando (CLI)

Execute o programa principal:

```bash
python main.py
```

O programa oferece um menu interativo com as seguintes opções:

1. **Criptografar Texto** - Criptografa texto com opções de seed, passes e salt
2. **Descriptografar Texto** - Descriptografa usando ciphertext e chave
3. **Comprimir Texto** - Comprime texto binário (0 e 1)
4. **Descomprimir Texto** - Descomprime texto comprimido
5. **Interface Web** - Inicia servidor web local
6. **Ajuda** - Mostra informações de ajuda
7. **Sair** - Encerra o programa

#### Exemplo de uso no terminal:

```
Bem-vindo ao sistema de criptografia HashChain.

Deseja usar a interface gráfica? Caso contrário o modo terminal será utilizado. (s/n): n

Escolha uma ação:
1. Criptografar Texto
2. Descriptografar Texto
3. Comprimir Texto
4. Descomprimir Texto
5. Interface Web
6. Ajuda
7. Sair

Digite o número da ação desejada: 1
```

### Interface Gráfica (GUI)

Para abrir a interface gráfica:

```bash
python main.py
# Escolha 's' quando perguntado sobre interface gráfica
```

Ou execute diretamente:

```python
from hashchain.interfaces import run
run()
```

A interface gráfica oferece:
- ✅ Criptografia com opções visuais
- ✅ Descriptografia intuitiva
- ✅ Compressão/Descompressão
- ✅ Visualização de resultados
- ✅ Salvamento de arquivos

### Interface Web

Para iniciar a interface web:

```bash
python main.py
# Escolha opção 5 - Interface Web
```

Ou execute diretamente:

```python
from hashchain.interfaces import run_web
run_web(host='127.0.0.1', port=5000)
```

A interface web estará disponível em `http://127.0.0.1:5000` no seu navegador.

**Recursos da interface web:**
- 🌐 Acessível via navegador
- 📱 Interface responsiva
- 🔐 Todas as funcionalidades disponíveis
- 🎨 Interface moderna e intuitiva

### Uso Programático

#### Exemplo Básico

```python
from hashchain import HashChain

# Criar instância
hc = HashChain()

# Criptografar
hc.encrypt(
    plaintext="Mensagem secreta",
    seed=12345678901234567890,
    pass_=[25, 30, 18],
    no_salt=False,
)

# Obter resultados
ciphertext = hc.info(0)  # texto comprimido
key = hc.info(1)         # chave

# Descriptografar
hc.decrypt(ciphertext=ciphertext, key=key)
plaintext = hc.info(3)   # texto descriptografado

print(f"Ciphertext: {ciphertext}")
print(f"Key: {key}")
print(f"Plaintext: {plaintext}")
```

#### Exemplo com Retorno Direto

```python
from hashchain import HashChain

hc = HashChain()

# Criptografar e obter resultado diretamente
result = hc.encrypt(
    plaintext="Hello, HashChain!",
    seed=98765432109876543210,
    pass_=[20, 25, 30],
    no_salt=True,
    retonar=True,  # Retorna [ciphertext, key]
)

ciphertext, key = result
print(f"Ciphertext: {ciphertext}")
print(f"Key: {key}")

# Descriptografar
hc.decrypt(ciphertext=ciphertext, key=key)
plaintext = hc.info(3)
print(f"Plaintext: {plaintext}")
```

#### Exemplo com Compressão

```python
from hashchain import HashChain

hc = HashChain()

# Comprimir texto binário
texto_binario = "1010101010101010"
hc.compression(texto_binario)
comprimido = hc.info(4)
print(f"Comprimido: {comprimido}")

# Descomprimir
hc.decompression(comprimido)
descomprimido = hc.info(5)
print(f"Descomprimido: {descomprimido}")
```

## 🔑 Conceitos-Chave

### Passes (`pass_`)
Lista de inteiros (3 dígitos na chave) que define como o ciphertext é segmentado e qual tabela usar por segmento. Cada número representa o tamanho de um segmento.

**Exemplo:**
```python
pass_ = [25, 30, 18]  # Primeiro segmento: 25 caracteres, segundo: 30, terceiro: 18
```

### Seed Principal (`seed`)
Inteiro decimal que determina todas as seeds derivadas por passe e pelo salting. A mesma seed sempre produz os mesmos resultados.

**Exemplo:**
```python
seed = 12345678901234567890  # Seed longa para maior segurança
```

### Salt (Opcional)
Strings inseridas em posições pseudoaleatórias, com base no `seed`. As posições e metadados são codificados na chave. Aumenta a entropia e dificulta análise.

**Uso:**
```python
no_salt=False  # Usa salt (padrão, mais seguro)
no_salt=True   # Não usa salt (mais rápido, menos seguro)
```

### Padding (Opcional)
Número de caracteres '1' adicionados ao final do ciphertext para adequar o comprimento quando necessário. A quantidade é guardada na chave.

## 📚 API Completa

### Classe `HashChain`

#### `encrypt(plaintext, pass_=None, seed=0, no_salt=False, debug_mode=False, min_table_leng=20, max_table_leng=999, compress_text=True, retonar=False, printar=False)`

Criptografa texto utilizando tabelas de substituição.

**Parâmetros:**
- `plaintext` (str): Texto a ser criptografado
- `pass_` (list[int], opcional): Lista de passes. Se None, gera automaticamente
- `seed` (int, opcional): Seed para geração determinística. Se 0, gera automaticamente
- `no_salt` (bool): Se True, não usa salt (padrão: False)
- `debug_mode` (bool): Se True, imprime informações de debug
- `min_table_leng` (int): Tamanho mínimo da tabela (mínimo 20)
- `max_table_leng` (int): Tamanho máximo da tabela (máximo 999)
- `compress_text` (bool): Se True, comprime o texto cifrado
- `retonar` (bool): Se True, retorna [ciphertext, key]
- `printar` (bool): Se True, imprime resultados

**Retorno:**
- Se `retonar=True`: `[ciphertext, key]`
- Caso contrário: `None` (armazena em `self._info`)

#### `decrypt(ciphertext=None, key=None)`

Descriptografa texto usando ciphertext e chave.

**Parâmetros:**
- `ciphertext` (str, opcional): Texto criptografado. Se None, usa `self._info[0]`
- `key` (str, opcional): Chave de descriptografia. Se None, usa `self._info[1]`

**Retorno:**
- `None` (armazena resultado em `self._info[3]`)

#### `compression(texto)`

Comprime texto binário (apenas 0 e 1).

**Parâmetros:**
- `texto` (str): Texto binário a ser comprimido

**Retorno:**
- `None` (armazena resultado em `self._info[4]`)

#### `decompression(texto)`

Descomprime texto comprimido.

**Parâmetros:**
- `texto` (str): Texto comprimido a ser descomprimido

**Retorno:**
- `None` (armazena resultado em `self._info[5]`)

#### `info(search)`

Retorna informações armazenadas da última operação.

**Parâmetros:**
- `search` (int | str): 
  - `0` ou `"compressed"` ou `"cipher"`: Ciphertext
  - `1` ou `"key"`: Chave
  - `2`: Ciphertext (alias)
  - `3` ou `"plain"`: Texto plano
  - `4`: Texto comprimido
  - `5`: Texto descomprimido

**Retorno:**
- `str | None`: Valor armazenado ou None se não houver dados

#### `out(output=0)`

Imprime informações armazenadas.

**Parâmetros:**
- `output` (int | str): Índice ou alias (mesmos valores de `info()`)

## 🔐 Formato da Chave

A chave "polida" concatena campos em sequência. As seções variam conforme o uso de salt.

### Com Salt

```
[lol_salt][salt_l][posicoes][lol_p][pl][passes][sl][seed][padding]
```

- `lol_salt` (3 dígitos): Comprimento do campo `salt_l`
- `salt_l`: Quantidade de posições de salt
- `posicoes`: Para cada posição, 3 dígitos indicando o número de dígitos do índice seguido do índice em si
- `lol_p` (3 dígitos): Comprimento do campo `pl`
- `pl`: Quantidade total de passes
- `passes`: `pl` entradas de 3 dígitos cada
- `sl` (3 dígitos): Comprimento da seed
- `seed`: Valor da seed decimal
- `padding` (opcional): Quantidade de '1' adicionados

### Sem Salt

```
[lol_p][pl][passes][sl][seed][padding]
```

Não inclui `lol_salt`, `salt_l` e `posicoes`.

## 🛠️ Construindo o Executável

Para criar um executável `.exe` do HashChain:

### Método 1: Script Automatizado (Recomendado)

```bash
# Versão GUI (recomendado - sempre abre a interface gráfica)
python build/build_exe_gui.py

# Versão completa (terminal + GUI)
python build/build_exe.py
```

O executável será criado em `dist/HashChain.exe`.

### Método 2: Usando arquivo .spec

```bash
cd build
pyinstaller HashChain.spec
```

### Método 3: Comando Manual

```bash
pyinstaller --name=HashChain --onefile --windowed --clean main.py
```

**Para mais detalhes, consulte:** `build/BUILD.md`

## ⚙️ Configuração

O arquivo `config.json` armazena configurações do programa:

```json
{
    "idd": 25599852140000,
    "terminal_mode": true,
    "params": {
        "passes": [50, 25, 60, 38],
        "seed": 2388636226855438390625029635578797980511582675618534009644830601267214645928643288262357364197196387839621331,
        "no_salt": true
    }
}
```

**Campos:**
- `idd`: ID de identificação do arquivo de configuração
- `terminal_mode`: Se `true`, inicia em modo terminal; se `false`, inicia GUI
- `params`: Parâmetros padrão de criptografia

## 💡 Boas Práticas

1. **Guarde sua chave com segurança:** A chave contém tudo necessário para descriptografar
2. **Use seeds longas:** Para maior variabilidade e segurança
3. **Use salt quando possível:** Aumenta a segurança (padrão: `no_salt=False`)
4. **Validação de parâmetros:**
   - `min_table_leng` não deve ser menor que 20
   - `max_table_leng` não deve exceder 999
5. **Cópia de saída colorida:** O `decrypt()` remove automaticamente sequências ANSI se você copiar ciphertext/key de uma saída colorida

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Padrões de Código

- Use POO (Programação Orientada a Objetos)
- Siga a estrutura modular existente
- Adicione testes para novas funcionalidades
- Documente funções e classes

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para detalhes.

## 📞 Suporte

Para questões, problemas ou sugestões:
- Abra uma issue no GitHub
- Consulte a documentação em `hashchain/DOC/ESTRUTURA.md`
- Veja exemplos em `main.py`

---

**Desenvolvido com ❤️ usando Python**
