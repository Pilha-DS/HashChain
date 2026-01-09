# --- Imports ---
import os
import json
import secrets
import datetime
import subprocess
from pathlib import Path
from utils import Handler, InputCollector, c
from HashChainClass import HashChainEncryption

# Global use.
HashChain: HashChainEncryption = HashChainEncryption()
Collector: InputCollector = InputCollector
config_path = Handler.find_config_file()
config = Handler.load_config(config_path)
has_dependencies = None
Stable = True
reinicios = 0
yes_aliases = ["s", "ss", "sim", "y", "yes"]
no_aliases = ["n", "nn", "nao", "não", "no"]

# Terminal colors
r = '\033[0m'      # Reset

# Estilos
bold = '\033[1m'       # Bold
italic = '\033[3m'     # Italic


# --- Functions ---

def close_program():
    global config, config_path
    Handler.save_config(config, config_path)

def restart_program():
    global reinicios
    if reinicios > 100:
        print(f"\n{r}{c('y')}Numero de reinícios consecutivos excedido.{r}")
        close_program()
    else:
        reinicios += 1
        Handler.limpar_terminal()
        main()

def check_action(user_input):
    if user_input == "r": restart_program()
    elif user_input == "e": close_program()

# Will handle user input, function calls and the interface (WiP).
def main():
    global has_dependencies, config
    
    print(f"\nBem-vindo ao sistema de criptografia {bold}HashChain.{r}\n {italic}- Para {bold}usar a interface{r}{italic} você deve ter as bibliotecas {r}{bold}tkinter{r}{italic} e {r}{bold}customtkinter{r}{italic} instaladas.{r}")
    print(f"{italic} - Para {bold}reiniciar{r}{italic} ou {bold}sair{r}{italic} a qualquer momento, digite {bold}'R' {r}{italic}/{bold} 'r'{r}{italic} ou {bold}'E'{r}{italic} /{bold} 'e'{r}.\n")
    has_dependencies = Handler.verify_required_modules()
    
    if config is None:
        print(f"\n{c('r')}O arquivo de configuração não foi carregado corretamente, as opções de criptografia padronizadas {bold}não estarão disponíveis.{r}")
    
    while Stable:
        if config["terminal_mode"]:
            while Stable:
                terminal_mode_input = input(f"\n{c('c', True)}Deseja usar a interface gráfica? Caso contrário o modo terminal será utilizado. {r}{c('w', bold=True)}(s/n){r}: ").strip().lower()
                check_action(terminal_mode_input)
                if terminal_mode_input in yes_aliases + no_aliases:
                    break
                else:
                    print(f"\n{c('y', True)}Ação inválida. Tente novamente.{r}")
                    continue
            config["terminal_mode"] = True if terminal_mode_input in no_aliases else False
            if not config["terminal_mode"]:
                continue
              
            while Stable:
                print(f'\n{bold}Escolha uma ação:{r}\n')
                action_list = ['Criptografar Texto', 'Descriptografar Texto', 'Comprimir Texto', 'Descomprimir Texto', 'Ajuda', 'Sair']
                Handler.print_menu(action_list)
                    
                action = input(f"\n{r}{c('p')}Digite o número da ação desejada:{r}{c(faint=True)} ").strip()
                check_action(action)
                
                if action not in ["1", "2", "3", "4", "5", "6"]:
                    print(f"\n{r}{c('y')}Ação inválida. Tente novamente.{r}")
                    continue
                action = int(action)
                match action:
                    # Criptografar
                    case 1:
                        while Stable:
                            ler_arquivo = input(f"\n{r}{c('c', True)}Deseja ler de um arquivo de texto existente? {r}{bold}(s/n): {r}")
                            check_action(ler_arquivo)
                            if ler_arquivo not in yes_aliases + no_aliases:
                                print(f"\n{r}{c('y')}Ação inválida. Tente novamente.{r}")
                                break
                            else:
                                break
                        texto = ''
                        if ler_arquivo in yes_aliases:
                            texto = Handler.ler_arquivo()
                        else:
                            texto = input(f"\n{r}{c('c', True)}Digite o texto a ser criptografado:{r} ")
                        if not texto:
                            print(f"\n{r}{c('y')}Aviso: Falha ao tentar ler, arquivo vazio, inexistente ou não selecionado.{r}")
                            print(f'{r}{c(faint=True)}\nReiniciando o programa, tente novamente.{r}')
                            restart_program()
                        while Stable:
                            print(f'\n{r}{bold}Tipo de seed desejada:{r}\n')
                            if config_path is None:
                                seed_type_list = ['Manual', 'Automática']
                                Handler.print_menu(seed_type_list)
                                seed_type = input(f"\n{c('p')}Digite o número da ação desejada:{r}{c(faint=True)} ").strip()
                            else:
                                seed_type_list = ['Manual', 'Automática', 'Padronizada']
                                Handler.print_menu(seed_type_list)
                                seed_type = input(f"\n{c('p')}Digite o número da ação desejada:{r}{c(faint=True)} ").strip()
                                
                            check_action(seed_type)
                            
                            if config_path is None:
                                if seed_type not in ["1", "2"]:
                                    print(f"\n{r}{c('y')}Ação inválida. Tente novamente.{r}")
                                    continue
                                else:
                                    break
                            elif config_path is not None:
                                if seed_type not in ["1", "2", "3"]:
                                    print(f"\n{r}{c('y')}Ação inválida. Tente novamente.{r}")
                                    continue
                                else:
                                    break
                                
                        match seed_type:
                            case "1":
                                seed = Collector.get_seed()
                            case "2":
                                num_digits = secrets.randbelow(65) + 64
                                seed = int("".join(str(secrets.randbelow(10)) for _ in range(num_digits)))
                            case "3":
                                seed = int(config["params"]["seed"])
                                
                        print(f"\n{r}{c('b')}Seed escolhida:{r} {c(faint=True, bold=True)}{seed}{r}")
                        
                        while Stable:
                            print(f'\n{r}{bold}Tipo de passo desejado:{r}\n')
                            if config_path is None:
                                passo_type_list = ['Manual', 'Automática']
                                Handler.print_menu(passo_type_list)
                                passo_type = input(f"\n{r}{c('p')}Digite o número da ação desejada:{r}{c(faint=True)} ").strip()
                            elif config_path is not None:
                                passo_type_list = ['Manual', 'Automática', 'Padronizada']
                                Handler.print_menu(passo_type_list)
                                passo_type = input(f"\n{r}{c('p')}Digite o número da ação desejada:{r}{c(faint=True)} ").strip()
                            
                            check_action(passo_type)
                                
                            if config_path is None:
                                if passo_type not in ["1", "2"]:
                                    print(f"\n{r}{c('y')}Ação inválida. Tente novamente.{r}")
                                    continue
                                else:
                                    break
                            elif config_path is not None:
                                if passo_type not in ["1", "2", "3"]:
                                    print(f"\n{r}{c('y')}Ação inválida. Tente novamente.{r}")
                                    continue
                                else:
                                    break
                                
                        match passo_type:
                            case "1":
                                passo = Collector.get_passes()
                            case "2":
                                num_passes = secrets.randbelow(64) + 8
                                passo = [secrets.randbelow(979) + 20 for _ in range(num_passes)]
                            case "3":
                                passo = config["params"]["passes"]
                                
                        print(f"\n{c('b')}Passos escolhidos:{r} {c(faint=True, bold=True)}{passo}{r}")
                        
                        while Stable:
                            print(f"\n{c('p', True, True)} - Salt é uma medida de segurança adicional que pode ser usada durante a criptografia para aumentar a aleatoriedade do processo, que adiciona sequências de caracteres e tamanhos aleatórios ao texto, ele transformara a chave para descriptografia em algo único para cada execução mesmo com os mesmos parâmetros.{r}")
                            no_salt_input = input(f"\n{bold}Deseja usar {c('p', True, True)}salt{r}{bold} na criptografia? (s/n):{r} ").strip().lower()
                            
                            check_action(no_salt_input)
                            
                            if no_salt_input not in yes_aliases + no_aliases:
                                print(f"\n{c('y')}Ação inválida. Tente novamente.{r}")
                                continue
                            else:
                                break
                        no_salt = False if no_salt_input in yes_aliases else True  
                        if len(texto) > 100_000:
                            print(f'\n{r}{c("y", faint=True)}Aviso: O texto fornecido excede 100Kb, a criptografia pode levar alguns instantes. Por favor aguarde...{r}')
                            
                        HashChain.encrypt(texto, passo, seed, no_salt)
                        print(f"\n{c("g", True)}Criptografia realizada com sucesso.{r}")
                        print(f"\n{c('b')}Texto criptografado:{r}")
                        print(f'{c(faint=True)}{HashChain.info(0)}{r}')
                        print(f"\n{c('b')}Chave de descriptografia:{r}")
                        print(f'{c(faint=True)}{HashChain.info(1)}{r}')
                        while Stable:
                            print(f'\n{r}{c('y')}{bold}Aviso: {r}{c('y')}em alguns casos o texto pode ser {bold}grande demais para o terminal exibir.{r}')
                            salvar_input = input(f"{c('c', True, True)} - Deseja salvar os salvar o texto gerado em um arquivo? {r}{bold}(s/n):{r} ").strip().lower()
                            
                            check_action(salvar_input)
                            
                            if salvar_input not in yes_aliases + no_aliases:
                                print(f"\n{r}{c('y')}Ação inválida. Tente novamente.{r}")
                                continue
                            
                            if salvar_input in yes_aliases:
                                while Stable:
                                    print(f"\n{r}{bold}Escolha o tipo de salvamento:{r}\n")
                                    savamento_type_list = ['Texto criptografado e chave', 'Salvar apenas o texto criptografado', 'Salvar apenas a chave']
                                    Handler.print_menu(savamento_type_list)
                                    tipo_salvamento = input(f"\n{r}{c('p')}Digite o número da ação desejada:{r}{c(faint=True)} ").strip()
                                    
                                    check_action(tipo_salvamento)
                                    
                                    if tipo_salvamento not in ["1", "2", "3"]:
                                        print(f"\n{r}{c('y')}Ação inválida. Tente novamente.{r}")
                                        continue
                                    match tipo_salvamento:
                                        # Save the COMPRESSED ciphertext (index 0) into JSON.
                                        # Decrypt will receive the compressed value and
                                        # HashChain.decrypt will detect/decompress as needed.
                                        case "2":
                                            dados = {"texto": HashChain.info(0), "chave": None}
                                        case "3":
                                            dados = {"texto": None, "chave": HashChain.info(1)}
                                        case "1":
                                            dados = {"texto": HashChain.info(0), "chave": HashChain.info(1)}
                                    break

                                try:
                                    project_root = next(
                                        (p for p in Path(__file__).resolve().parents if p.name == "HashChain---encryption"),
                                        None
                                    )

                                    if not project_root:
                                        raise FileNotFoundError(f"{r}{c('r')}Diretório 'HashChain---encryption' não encontrado.{r}")
                                    
                                    outputs_dir = project_root / "outputs"
                                    outputs_dir.mkdir(exist_ok=True)

                                    agora = datetime.datetime.now()
                                    milissegundos = int(agora.microsecond / 1000)
                                    file_name = agora.strftime(f"log_%Y-%m-%d_%H-%M-%S-{milissegundos:03d}.json")
                                    log_path = outputs_dir / file_name

                                    # Cria e escreve o arquivo JSON
                                    with open(log_path, "x", encoding="utf-8") as file:
                                        json.dump(dados, file, ensure_ascii=False, indent=4)

                                    print(f"\n{r}{c('b')}Log salvo em: {r}{c(faint=True)}{log_path}{r}")
                                    
                                except Exception as e:
                                    print(f"{r}{c('r')}Erro: Ocorreu um erro ao tentar criar o arquivo:{r} ", e)
                                    
                                print(f"\n{r}{c('g')}O arquivo foi salvo no seguinte modelo: {bold}log_YYYY-MM-DD_HH-MM-SS-MMM.json,{r}{c('g')} e pode ser encontrado na pasta outputs.{r}")
                                break
                            else:
                                break
                        while Stable:
                            recripto = input(f"\n{r}{c('c', True)}Criptografia finalizada, deseja utilizar o programa novamente? {r}{bold}(s/n):{r} ")
                            check_action(recripto)
                            if recripto not in yes_aliases + no_aliases:
                                print(f"{r}\n{c('y')}Ação inválida. Tente novamente.{r}")
                                continue
                            if recripto in yes_aliases:
                                break
                            else:
                                close_program()
                                break
                                        
                    # Descriptografar
                    case 2:
                        while Stable:
                            log_input = input(f"\n{r}{c('c', True)}Deseja usar um arquivo de log para descriptografia? {r}{bold}(s/n){r}: ").strip().lower()
                            
                            check_action(log_input)
                            
                            if log_input not in yes_aliases + no_aliases:
                                print(f"{r}\n{c('y')}Ação inválida. Tente novamente.{r}")
                                continue 
                            else:
                                break
                        log_input = True if log_input in yes_aliases else False
                        if log_input and Handler.find_outputs_folder() is not None and Handler.list_output_files() is not None and Handler.list_output_files() != []:
                            while Stable:
                                mostrar_logs = input(f"\n{r}{c('c', True)}Deseja ver uma lista dos logs disponíveis? {r}{bold}(s/n):{r} ")
                                check_action(mostrar_logs)
                                if mostrar_logs not in yes_aliases + no_aliases:
                                    print(f"\n{r}{c('y')}Ação inválida. Tente novamente.{r}")
                                    continue
                                else:
                                    break
                            if mostrar_logs in yes_aliases:
                                while Stable:
                                        print(f"\n{bold}Lista dos logs disponíveis:{r}\n")
                                        logs_list = Handler.list_output_files()
                                        Handler.print_menu(logs_list)
                                        log_escolhido = input(f"\n{r}{c('p')}Digite o número do log que deseja usar: {r}{c(faint=True)}")
                                        check_action(log_escolhido)
                                        try:
                                            log_escolhido = int(log_escolhido)
                                        except Exception:
                                            print(f"{r}\n{c('y')}Ação inválida. Tente novamente.{r}")
                                            continue
                                        else:
                                            if log_escolhido >= 1 and log_escolhido <= len(logs_list):
                                                break
                                            else:
                                                print(f"\n{r}{c('y')}Ação inválida. Tente novamente.{r}")
                                                continue
                                nome_log = logs_list[log_escolhido - 1]
                                outputs_path = Handler.find_outputs_folder()
                                log_path = os.path.join(outputs_path, nome_log)
                                
                            else:
                                while Stable:

                                    outputs_path = Handler.find_outputs_folder()

                                    log_name = input(f"\n{r}{c('c', True)}Digite o nome do log (ex: log_2025-10-31_19-40-00-123.json):{r} ").strip()

                                    # Garante que o usuário não colocou caminho indevido
                                    log_path = os.path.join(outputs_path, log_name)

                                    if not os.path.exists(log_path):
                                        print(f"\n{c('r')}Erro: O arquivo '{log_name}' não foi encontrado em '{outputs_path}'.{r}")
                                        print("\nTente novamente.")
                                        continue
                                    else:
                                        break
 
                            try:
                                with open(log_path, "r", encoding="utf-8") as file:
                                    dados = json.load(file)
                                    if dados['texto'] and dados['chave']:
                                        tipo_log = 1
                                    elif dados['texto'] and not dados['chave']:
                                        tipo_log = 2
                                    elif not dados['texto'] and dados['chave']:
                                        tipo_log = 3
                                    else:
                                        tipo_log = None
                                        
                                    match tipo_log:
                                        case 1:
                                            texto = dados["texto"]
                                            key = dados["chave"]
                                        case 2:
                                            print('\nEsse tipo de arquivo contem apenas o texto criptografado.\n')
                                            texto = dados["texto"]
                                            key = input("Digite a chave para descriptografia: ").strip()
                                        case 3:
                                            print('\nEsse tipo de arquivo contem apenas a chave.\n')
                                            texto = input("Digite o texto a ser descriptografado: ").strip()
                                            key = dados["chave"]
                                        
                            except FileNotFoundError:
                                print(f"{c('y')}Arquivo não encontrado. Tente novamente.{r}")
                                continue
                            except json.JSONDecodeError:
                                print(f"{c('r')}Erro: arquivo JSON inválido. Tente novamente com um log gerado pelo programa.{r}")
                                continue
                            try:
                                if len(texto) > 100_000:
                                    print(f'\n{r}{c("y", faint=True)}Aviso: A o texto criptografado fornecido excede 100Kb, a descriptografia pode levar alguns instantes. Por favor aguarde...{r}')
                                HashChain.decrypt(texto, key)
                            except Exception:
                                print(f"\n{c('r')}Erro: Valores para descriptografia {bold}inválidos,{r} {c('r')}verifique de o log foi adulterado.{r}")
                            else:
                                print(f"\n{c('g')}Descriptografia realizada com sucesso.\n{r}")
                                print(f'{r}{c('b')}Texto descriptografado: {r}')
                                print(f'{r}{c(faint=True)}{HashChain.info(3)}{r}')
                                
                                while Stable:
                                    salvar_decrip_txt = input(f'{r}{c('c', True)}\nDeseja salvar o texto descriptografado em um arquivo de texto? {r}{bold}(s/n): {r}')
                                    check_action(salvar_decrip_txt)
                                    if salvar_decrip_txt not in yes_aliases + no_aliases:
                                        print(f"\n{r}{c('y')}Ação inválida. Tente novamente.{r}\n")
                                        continue
                                    if salvar_decrip_txt in no_aliases:
                                        break
                                    else:
                                        Handler.salvar_arquivo(HashChain.info(3))
                                        break
                            
                        else:
                            if log_input:
                                print(f"\n{r}{c('y')}Não é possível usar os arquivos de logs pois, a pasta não foi encontrada ou não possui logs.{r}")
                                while Stable:
                                    continuar = input(f"\n{r}{c('c', True)}Deseja utiliza o metodo normal de descriptografia? {r}{bold}(s/n): {r}")
                                    check_action(continuar)
                                    if continuar not in yes_aliases + no_aliases:
                                        print(f"\n{r}{c('y')}Ação inválida. Tente novamente.{r}\n")
                                        continue
                                    else:
                                        break
                                
                                if continuar in yes_aliases:
                                    pass
                                else:
                                    close_program()
                                    
                                        
                            texto = input(f"\n{r}{c('c', True)}Digite o texto a ser descriptografado: {r}")
                            key = input(f"\n{r}{c('c', True)}Digite a chave para descriptografia: {r}")
                            try:
                                if len(texto) > 100_000:
                                    print(f'\n{r}{c("y", faint=True)}Aviso: A o texto criptografado fornecido excede 100Kb, a descriptografia pode levar alguns instantes. Por favor aguarde...{r}')
                                HashChain.decrypt(texto, key)
                            except Exception:
                                print(f"\n{r}{c('r')}Erro: Valores para descriptografia {bold}inválidos.{r}")
                            else:
                                print(f"\n{r}{c('g')}Descriptografia realizada com sucesso.{r}")
                                print(f'{r}\n{c('b')}Texto descriptografado:{r}')
                                print(f'{r}{c(faint=True)}{HashChain.info(3)}{r}')
                                
                                while Stable:
                                    salvar_decrip_txt = input(f'{r}{c('c', True)}\nDeseja salvar em um arquivo de texto? {r}{bold}(s/n): {r}')
                                    check_action(salvar_decrip_txt)
                                    if salvar_decrip_txt not in yes_aliases + no_aliases:
                                        print(f"\n{r}{c('y')}Ação inválida. Tente novamente.{r}\n")
                                        continue
                                    if salvar_decrip_txt in no_aliases:
                                        break
                                    else:
                                        Handler.salvar_arquivo(HashChain.info(3))
                                        break
                        
                    # Compressão
                    case 3:
                        texto = input(f"\n{r}{c('c', True)}Digite o texto a ser comprimido: {r}")
                        print(f"\n{c('b')}Texto comprimido:{r}")
                        resultado_decompression = HashChain.compression(texto)
                        if resultado_decompression is not None:
                            print(f'{r}{c(faint=True)}{resultado_decompression}{r}')
                        
                    # Descompressão
                    case 4:
                        texto = input(f"\n{r}{c('c', True)}Digite o texto a ser descomprimido: {r}").upper()
                        print(f"\n{c('b')}Texto descomprimido:{r}")
                        resultado_compressao = HashChain.decompression(texto)
                        if resultado_compressao is not None:
                            print(f'{r}{c(faint=True)}{resultado_compressao}{r}')
                        
                    # Ajuda
                    case 5:
                        print(f"\n{r}{bold}Ajuda - HashChain Encryption System{r}")
                        while Stable:
                            print(f'{r}{bold}\nEscolha uma opção de ajuda:{r}\n')
                            ajuda_input_list = ['Sobre o HashChain', 'Como usar o programa', 'Explicação dos parâmetros', 'Explicação da decriptação', 'Explicação da compressão e descompressão', 'Voltar ao menu principal']
                            Handler.print_menu(ajuda_input_list)
                            ajuda_input = input(f"{r}{c('p')}\nDigite o número da ação desejada:{r}{c(faint=True)} ").strip()
                            
                            check_action(ajuda_input)
                            
                            if ajuda_input not in ["1", "2", "3", "4", "5", "6"]:
                                print(f"\n{r}{c('y')}Ação inválida. Tente novamente.{r}")
                                continue
                            print()
                            match ajuda_input:
                                case "1":
                                    print(f"{r}{c('b')}{ajuda_input_list[0]}:{r}")
                                    print(f"{r}{c(faint=True)}{italic} - O HashChain é um sistema de criptografia que utiliza cadeias de funções hash para garantir a segurança dos dados. Ele permite a criptografia e descriptografia de textos, além de oferecer funcionalidades de compressão e descompressão.")
                                case "2":
                                    print(f"{r}{c('b')}{ajuda_input_list[1]}:{r}")
                                    print(f"{r}{c(faint=True)}{italic} - Para usar o programa, escolha entre o modo terminal ou a interface gráfica (se disponível). Siga as instruções na tela para criptografar, descriptografar, comprimir ou descomprimir textos.")
                                case "3":
                                    print(f"{r}{c('b')}{ajuda_input_list[2]}:{r}")
                                    print(f"{r}{italic} - Seed:{c(faint=True)} É um número inteiro de no mínimo 8 dígitos, inicial usado para gerar a cadeia de hash.\n - {r}{italic}Passos:{c(faint=True)} Uma lista de inteiros que define as etapas da cadeia de hash. (Cada inteiro deve estar entre 20 a 999)\n - {r}{italic}Salt:{c(faint=True)} Uma medida de segurança adicional que pode ser usada durante a criptografia para aumentar a aleatoriedade do processo.{r}")
                                case "4":
                                    print(f"{r}{c('b')}{ajuda_input_list[3]}:{r}")
                                    print(f"{r}{c(faint=True)}{italic} - A descriptografia requer o texto criptografado e a chave gerada durante a criptografia. O HashChain utiliza a cadeia de hash inversa para recuperar o texto original. Durante a criptografia, esses dados podem ser salvos em um arquivo de log para facilitar a descriptografia posterior, copiando e colando o seu caminho relativo a pasta atual.")
                                case "5":
                                    print(f"{r}{c('b')}{ajuda_input_list[4]}:{r}")
                                    print(f"{r}{c(faint=True)}{italic} - A compressão reduz o tamanho do texto utilizando algoritmos específicos para compresão de números binários, enquanto a descompressão reverte esse processo para recuperar o texto original.")
                                case "6":
                                    print(f"\n{r}{c(faint=True)}Voltando ao menu principal.{r}")
                                    break
                                        
                    # Sair
                    case 6:
                        close_program()
                        
                    case _:
                        print(f"{c('r', True)}FATAL ERROR")
                        close_program()
            
        elif not config["terminal_mode"]:
            if not has_dependencies:
                print("Não é possível iniciar a interface gráfica, pois as dependências necessárias não estão instaladas, instale-as e tente novamente.")
                config["terminal_mode"] = True
                break

            try:
                subprocess.run(["python", "interface.py"])
            except Exception as e:
                close_program()
                
            print(f'\n{r}{c(faint=True)}Voltando ao terminal...{r}')
            config["terminal_mode"] = True
    
# Handles key actions.
if __name__ == "__main__":
    main()
    close_program()
