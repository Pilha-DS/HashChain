tables = {}
inverted_tables = {}

def gerar_cifra(seed, tamanho, indice):
    """
    Gera cifra determinística.
    Começo e fim sempre '#', meio calculado de forma única com seed e índice.
    """
    # Gera um número base baseado na seed e índice
    num = seed + indice * 2654435761
    
    meio = []
    for i in range(tamanho):
        # Escolhe entre '0' ou '1'
        bit = (num >> i) & 1
        meio.append('0' if bit == 0 else '1')
    
    return ''.join(meio)

def gerar_tabelas(seed, tamanhos_especificos:list = None, caracteres=None):
    """
    Gera tabelas de cifra para tamanhos específicos.
    
    Args:
        tamanhos_especificos: Lista de tamanhos específicos para gerar (ex: [32, 15, 20])
        caracteres: Lista de caracteres a serem codificados
    """
    global tables
    global inverted_tables
    
    if not seed:
        raise ValueError("Deve mandar o parametro (seed)")

    # Se não for especificado, usa tamanhos de 9 a 24 (comportamento original)
    if not tamanhos_especificos:
        raise ValueError("Deve mandar o parametro (tamanhos_especificos)")

    if caracteres is None:
        caracteres = [
            "a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t",
            "u","v","w","x","y","z",
            "A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T",
            "U","V","W","X","Y","Z",
            "0","1","2","3","4","5","6","7","8","9",
            "`","´","¨","¯","˘","˙","˚","˝","ˇ","¸","˛"
            "!",",","#","$","%","&","'","(",")","*","+",
            # RETIRAR \ SE DER ERRO "\\"
            " ",",","-",".","/","\\",":",";","<","=",">","?","@","[","]","^","_","`","{","|","}","~",'"',
            "á","à","â","ã","ä","é", "è", "ê", "ë","í", "ì", "î", "ï","ó", "ò", "ô", "õ", "ö",
            "ú","ù","û","ü","ç","Á", "À", "Â", "Ã", "Ä","É", "È", "Ê", "Ë",
            "Í","Ì","Î","Ï","Ó", "Ò", "Ô", "Õ", "Ö","Ú", "Ù", "Û", "Ü","Ç"
        ]

    tables_ = {}

    for tamanho in tamanhos_especificos:
        tabela = {}
        # Gera a cifra dos caracteres usando o índice
        for i, char in enumerate(caracteres):
            tabela[char] = gerar_cifra(seed, tamanho, i)
        tables_[tamanho] = tabela
    
    tables = tables_
    inverted_tables = {k: {v: kk for kk, v in d.items()} for k, d in tables_.items()}
    return tables_, inverted_tables