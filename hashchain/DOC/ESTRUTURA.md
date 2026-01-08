# Nova Estrutura do Projeto HashChain

## Visão Geral

O projeto foi completamente reorganizado seguindo padrões de organização modular e Programação Orientada a Objetos (POO). A estrutura agora está separada em módulos bem definidos, facilitando manutenção e extensão.

## Estrutura de Diretórios

```
HashChain---encryption/
├── hashchain/                    # Pacote principal
│   ├── __init__.py              # Exporta classe principal
│   ├── hashchain.py             # Classe principal HashChain
│   ├── core/                    # Módulos principais
│   │   ├── __init__.py
│   │   ├── compression.py       # Compressão/Descompressão
│   │   ├── encryption.py        # Criptografia
│   │   ├── decryption.py       # Descriptografia
│   │   └── key_generator.py    # Geração de chaves
│   ├── tables/                  # Geração de tabelas
│   │   ├── __init__.py
│   │   └── table_generator.py  # Gerador de tabelas
│   ├── utils/                   # Utilitários
│   │   ├── __init__.py
│   │   ├── colors.py           # Formatação de cores
│   │   ├── handler.py          # Operações de sistema
│   │   └── input_collector.py  # Coleta de inputs
│   ├── config/                  # Configuração
│   │   ├── __init__.py
│   │   └── config_manager.py   # Gerenciador de config
│   └── interfaces/              # Interfaces (futuro)
│       └── __init__.py
├── tests/                       # Testes
│   ├── __init__.py
│   ├── test_compression.py
│   ├── test_encryption.py
│   ├── test_decryption.py
│   ├── test_hashchain.py
│   └── test_table_generator.py
├── main.py                      # Main original (legado)
├── main_new.py                  # Main atualizado (nova estrutura)
├── HashChainClass.py           # Classe original (legado)
├── interface.py                # Interface gráfica (legado)
├── utils.py                     # Utilitários originais (legado)
├── tables.py                    # Tabelas originais (legado)
└── config.json                  # Arquivo de configuração
```

## Módulos Principais

### 1. Core (`hashchain/core/`)

#### `compression.py` - Classe `Compression`
- `compress()`: Comprime texto binário
- `decompress()`: Descomprime texto binário

#### `encryption.py` - Classe `Encryption`
- `encrypt()`: Criptografa texto usando tabelas de substituição
- `_create_salt()`: Cria salt para aumentar entropia

#### `decryption.py` - Classe `Decryption`
- `decrypt()`: Descriptografa texto usando chave
- `_parse_key()`: Faz parse da chave de descriptografia

#### `key_generator.py` - Classe `KeyGenerator`
- `generate()`: Gera chave polida para descriptografia

### 2. Tables (`hashchain/tables/`)

#### `table_generator.py` - Classe `TableGenerator`
- `generate_tables()`: Gera tabelas de substituição determinísticas
- `_generate_cipher()`: Gera cifra individual

### 3. Utils (`hashchain/utils/`)

#### `colors.py` - Classe `ColorFormatter`
- `format()`: Formata códigos de cor ANSI
- `c()`: Alias para format()

#### `handler.py` - Classe `Handler`
- `clear_terminal()`: Limpa terminal
- `find_config_file()`: Encontra arquivo de configuração
- `load_config()`: Carrega configuração
- `save_config()`: Salva configuração
- `read_file()`: Lê arquivo de texto
- `save_file()`: Salva arquivo de texto
- `print_menu()`: Imprime menu formatado

#### `input_collector.py` - Classe `InputCollector`
- `get_seed()`: Coleta seed do usuário
- `get_passes()`: Coleta passes do usuário

### 4. Config (`hashchain/config/`)

#### `config_manager.py` - Classe `ConfigManager`
- `load()`: Carrega configuração
- `save()`: Salva configuração
- `get()`: Obtém valor de configuração
- `set()`: Define valor de configuração

### 5. Classe Principal (`hashchain/hashchain.py`)

#### `HashChain` - Classe Principal
- `encrypt()`: Criptografa texto
- `decrypt()`: Descriptografa texto
- `compression()`: Comprime texto
- `decompression()`: Descomprime texto
- `info()`: Retorna informações armazenadas
- `out()`: Imprime informações armazenadas

## Uso da Nova Estrutura

### Exemplo Básico

```python
from hashchain import HashChain

# Criar instância
hc = HashChain()

# Criptografar
hc.encrypt(
    plaintext="Mensagem secreta",
    seed=12345678901234567890,
    pass_=[25, 30, 18],
    no_salt=True,
)

# Obter resultados
ciphertext = hc.info(0)  # texto comprimido
key = hc.info(1)         # chave

# Descriptografar
hc.decrypt(ciphertext=ciphertext, key=key)
plaintext = hc.info(3)  # texto descriptografado
```

### Usando Módulos Individuais

```python
from hashchain.core import Encryption, Decryption, Compression
from hashchain.tables import TableGenerator

# Usar módulos diretamente
encryption = Encryption()
ciphertext, key, info = encryption.encrypt(
    plaintext="Teste",
    seed=12345678901234567890,
    pass_=[20, 25],
)

decryption = Decryption()
plaintext, info = decryption.decrypt(ciphertext=ciphertext, key=key)
```

## Testes

Todos os módulos possuem testes unitários na pasta `tests/`. Para executar:

```bash
python -m unittest discover tests -v
```

### Cobertura de Testes

- ✅ Compressão/Descompressão
- ✅ Criptografia
- ✅ Descriptografia
- ✅ Geração de Tabelas
- ✅ Classe Principal HashChain

## Migração

### Do Código Antigo para o Novo

**Antigo:**
```python
from HashChainClass import HashChainEncryption

H = HashChainEncryption()
H.encrypt(texto, passo, seed, no_salt)
```

**Novo:**
```python
from hashchain import HashChain

hc = HashChain()
hc.encrypt(texto, passo, seed, no_salt)
```

## Benefícios da Nova Estrutura

1. **Modularidade**: Cada funcionalidade está em seu próprio módulo
2. **POO**: Tudo convertido para classes e objetos
3. **Testabilidade**: Fácil de testar cada módulo isoladamente
4. **Manutenibilidade**: Código mais organizado e fácil de entender
5. **Extensibilidade**: Fácil adicionar novas funcionalidades
6. **Reutilização**: Módulos podem ser usados independentemente

## Próximos Passos

1. Atualizar `interface.py` para usar a nova estrutura
2. Adicionar mais testes de integração
3. Criar documentação completa da API
4. Adicionar type hints completos
5. Implementar logging adequado

