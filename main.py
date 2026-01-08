"""Main atualizado usando a nova estrutura modular."""
import os
import json
import secrets
import datetime
import subprocess
from pathlib import Path

from hashchain import HashChain
from hashchain.utils import Handler, InputCollector, ColorFormatter
from hashchain.config import ConfigManager

# Global use.
hashchain = HashChain()
collector = InputCollector()
config_manager = ConfigManager()
config = config_manager.load()
has_dependencies = None
Stable = True
reinicios = 0
yes_aliases = ["s", "ss", "sim", "y", "yes"]
no_aliases = ["n", "nn", "nao", "não", "no"]

# Terminal colors
color = ColorFormatter()
r = color.RESET
bold = color.BOLD
italic = color.ITALIC


# --- Functions ---

def close_program():
    """Fecha o programa e salva configurações."""
    global config_manager
    config_manager.save()


def restart_program():
    """Reinicia o programa."""
    global reinicios
    if reinicios > 100:
        print(f"\n{r}{color.c('y')}Numero de reinícios consecutivos excedido.{r}")
        close_program()
    else:
        reinicios += 1
        Handler.clear_terminal()
        main()


def check_action(user_input):
    """Verifica ações do usuário."""
    if user_input == "r":
        restart_program()
    elif user_input == "e":
        close_program()


def main():
    """Função principal."""
    global has_dependencies, config
    
    print(f"\nBem-vindo ao sistema de criptografia {bold}HashChain.{r}\n "
          f"{italic}- Para {bold}usar a interface{r}{italic} você deve ter as bibliotecas "
          f"{r}{bold}tkinter{r}{italic} e {r}{bold}customtkinter{r}{italic} instaladas.{r}")
    print(f"{italic} - Para {bold}reiniciar{r}{italic} ou {bold}sair{r}{italic} a qualquer momento, "
          f"digite {bold}'R' {r}{italic}/{bold} 'r'{r}{italic} ou {bold}'E'{r}{italic} /{bold} 'e'{r}.\n")
    
    has_dependencies = Handler.verify_required_modules()
    
    if config is None:
        print(f"\n{color.c('r')}O arquivo de configuração não foi carregado corretamente, "
              f"as opções de criptografia padronizadas {bold}não estarão disponíveis.{r}")
    
    while Stable:
        if config.get("terminal_mode", True):
            while Stable:
                terminal_mode_input = input(
                    f"\n{color.c('c', True)}Deseja usar a interface gráfica? "
                    f"Caso contrário o modo terminal será utilizado. "
                    f"{r}{color.c('w', bold=True)}(s/n){r}: "
                ).strip().lower()
                
                check_action(terminal_mode_input)
                
                if terminal_mode_input in yes_aliases + no_aliases:
                    break
                else:
                    print(f"\n{color.c('y', True)}Ação inválida. Tente novamente.{r}")
                    continue
            
            config["terminal_mode"] = True if terminal_mode_input in no_aliases else False
            config_manager.set("terminal_mode", config["terminal_mode"])
            
            if not config["terminal_mode"]:
                continue
            
            while Stable:
                print(f'\n{bold}Escolha uma ação:{r}\n')
                action_list = [
                    'Criptografar Texto', 'Descriptografar Texto',
                    'Comprimir Texto', 'Descomprimir Texto', 
                    'Interface Web', 'Ajuda', 'Sair'
                ]
                Handler.print_menu(action_list)
                
                action = input(f"\n{r}{color.c('p')}Digite o número da ação desejada:"
                              f"{r}{color.format(faint=True)} ").strip()
                check_action(action)
                
                if action not in ["1", "2", "3", "4", "5", "6", "7"]:
                    print(f"\n{r}{color.c('y')}Ação inválida. Tente novamente.{r}")
                    continue
                
                action = int(action)
                match action:
                    # Criptografar
                    case 1:
                        handle_encrypt()
                    
                    # Descriptografar
                    case 2:
                        handle_decrypt()
                    
                    # Compressão
                    case 3:
                        handle_compress()
                    
                    # Descompressão
                    case 4:
                        handle_decompress()
                    
                    # Interface Web
                    case 5:
                        handle_web_interface()
                    
                    # Ajuda
                    case 6:
                        handle_help()
                    
                    # Sair
                    case 7:
                        close_program()
                    
                    case _:
                        print(f"{color.c('r', True)}FATAL ERROR")
                        close_program()
        
        elif not config.get("terminal_mode", True):
            if not has_dependencies:
                print("Não é possível iniciar a interface gráfica, pois as dependências "
                      "necessárias não estão instaladas, instale-as e tente novamente.")
                config["terminal_mode"] = True
                config_manager.set("terminal_mode", True)
                break
            
            try:
                from hashchain.interfaces import run
                run()
            except Exception as e:
                close_program()
            
            print(f'\n{r}{color.format(faint=True)}Voltando ao terminal...{r}')
            config["terminal_mode"] = True
            config_manager.set("terminal_mode", True)


def handle_encrypt():
    """Lida com a criptografia."""
    global hashchain, config_manager, config
    
    handler = Handler()
    
    # Ler texto
    ler_arquivo = None
    while Stable:
        ler_arquivo_input = input(
            f"\n{r}{color.c('c', True)}Deseja ler de um arquivo de texto existente? "
            f"{r}{bold}(s/n): {r}"
        ).strip().lower()
        
        check_action(ler_arquivo_input)
        
        if ler_arquivo_input in yes_aliases + no_aliases:
            ler_arquivo = ler_arquivo_input
            break
        else:
            print(f"\n{r}{color.c('y')}Ação inválida. Tente novamente.{r}")
            continue
    
    texto = ''
    if ler_arquivo in yes_aliases:
        texto = handler.read_file()
    else:
        texto = input(f"\n{r}{color.c('c', True)}Digite o texto a ser criptografado:{r} ")
    
    if not texto:
        print(f"\n{r}{color.c('y')}Aviso: Falha ao tentar ler, arquivo vazio, inexistente ou não selecionado.{r}")
        print(f'{r}{color.format(faint=True)}\nReiniciando o programa, tente novamente.{r}')
        restart_program()
        return
    
    # Escolher seed
    seed = choose_seed()
    
    # Escolher passes
    passo = choose_passes()
    
    # Escolher salt
    no_salt = choose_salt()
    
    # Criptografar
    if len(texto) > 100_000:
        print(f'\n{r}{color.c("y", faint=True)}Aviso: O texto fornecido excede 100Kb, '
              f'a criptografia pode levar alguns instantes. Por favor aguarde...{r}')
    
    hashchain.encrypt(texto, passo, seed, no_salt)
    print(f"\n{color.c('g', True)}Criptografia realizada com sucesso.{r}")
    print(f"\n{color.c('b')}Texto criptografado:{r}")
    print(f'{color.format(faint=True)}{hashchain.info(0)}{r}')
    print(f"\n{color.c('b')}Chave de descriptografia:{r}")
    print(f'{color.format(faint=True)}{hashchain.info(1)}{r}')
    
    # Salvar opcional
    handle_save_encrypted()
    
    # Continuar?
    while Stable:
        recripto = input(
            f"\n{r}{color.c('c', True)}Criptografia finalizada, deseja utilizar o programa novamente? "
            f"{r}{bold}(s/n):{r} "
        )
        check_action(recripto)
        
        if recripto not in yes_aliases + no_aliases:
            print(f"{r}\n{color.c('y')}Ação inválida. Tente novamente.{r}")
            continue
        
        if recripto in yes_aliases:
            break
        else:
            close_program()
            break


def choose_seed():
    """Escolhe seed para criptografia."""
    global config
    
    config_path = config_manager.config_path
    
    while Stable:
        print(f'\n{r}{bold}Tipo de seed desejada:{r}\n')
        
        if config_path is None:
            seed_type_list = ['Manual', 'Automática']
        else:
            seed_type_list = ['Manual', 'Automática', 'Padronizada']
        
        Handler.print_menu(seed_type_list)
        seed_type = input(f"\n{color.c('p')}Digite o número da ação desejada:"
                         f"{r}{color.format(faint=True)} ").strip()
        
        check_action(seed_type)
        
        if config_path is None:
            if seed_type not in ["1", "2"]:
                print(f"\n{r}{color.c('y')}Ação inválida. Tente novamente.{r}")
                continue
            else:
                break
        else:
            if seed_type not in ["1", "2", "3"]:
                print(f"\n{r}{color.c('y')}Ação inválida. Tente novamente.{r}")
                continue
            else:
                break
    
    match seed_type:
        case "1":
            return collector.get_seed()
        case "2":
            num_digits = secrets.randbelow(65) + 64
            return int("".join(str(secrets.randbelow(10)) for _ in range(num_digits)))
        case "3":
            return int(config["params"]["seed"])
    
    return 0


def choose_passes():
    """Escolhe passes para criptografia."""
    global config
    
    config_path = config_manager.config_path
    
    while Stable:
        print(f'\n{r}{bold}Tipo de passo desejado:{r}\n')
        
        if config_path is None:
            passo_type_list = ['Manual', 'Automática']
        else:
            passo_type_list = ['Manual', 'Automática', 'Padronizada']
        
        Handler.print_menu(passo_type_list)
        passo_type = input(f"\n{r}{color.c('p')}Digite o número da ação desejada:"
                          f"{r}{color.format(faint=True)} ").strip()
        
        check_action(passo_type)
        
        if config_path is None:
            if passo_type not in ["1", "2"]:
                print(f"\n{r}{color.c('y')}Ação inválida. Tente novamente.{r}")
                continue
            else:
                break
        else:
            if passo_type not in ["1", "2", "3"]:
                print(f"\n{r}{color.c('y')}Ação inválida. Tente novamente.{r}")
                continue
            else:
                break
    
    match passo_type:
        case "1":
            return collector.get_passes()
        case "2":
            num_passes = secrets.randbelow(64) + 8
            return [secrets.randbelow(979) + 20 for _ in range(num_passes)]
        case "3":
            return config["params"]["passes"]
    
    return []


def choose_salt():
    """Escolhe se usa salt."""
    while Stable:
        print(f"\n{color.c('p', True, True)} - Salt é uma medida de segurança adicional que pode ser "
              f"usada durante a criptografia para aumentar a aleatoriedade do processo, que adiciona "
              f"sequências de caracteres e tamanhos aleatórios ao texto, ele transformara a chave para "
              f"descriptografia em algo único para cada execução mesmo com os mesmos parâmetros.{r}")
        
        no_salt_input = input(
            f"\n{bold}Deseja usar {color.c('p', True, True)}salt{r}{bold} na criptografia? (s/n):{r} "
        ).strip().lower()
        
        check_action(no_salt_input)
        
        if no_salt_input not in yes_aliases + no_aliases:
            print(f"\n{color.c('y')}Ação inválida. Tente novamente.{r}")
            continue
        else:
            break
    
    return False if no_salt_input in yes_aliases else True


def handle_save_encrypted():
    """Lida com salvamento de texto criptografado."""
    global hashchain
    
    while Stable:
        print(f'\n{r}{color.c('y')}{bold}Aviso: {r}{color.c('y')}em alguns casos o texto pode ser '
              f'{bold}grande demais para o terminal exibir.{r}')
        
        salvar_input = input(
            f"{color.c('c', True, True)} - Deseja salvar os salvar o texto gerado em um arquivo? "
            f"{r}{bold}(s/n):{r} "
        ).strip().lower()
        
        check_action(salvar_input)
        
        if salvar_input not in yes_aliases + no_aliases:
            print(f"\n{r}{color.c('y')}Ação inválida. Tente novamente.{r}")
            continue
        
        if salvar_input in yes_aliases:
            while Stable:
                print(f"\n{r}{bold}Escolha o tipo de salvamento:{r}\n")
                savamento_type_list = [
                    'Texto criptografado e chave',
                    'Salvar apenas o texto criptografado',
                    'Salvar apenas a chave'
                ]
                Handler.print_menu(savamento_type_list)
                tipo_salvamento = input(
                    f"\n{r}{color.c('p')}Digite o número da ação desejada:"
                    f"{r}{color.format(faint=True)} "
                ).strip()
                
                check_action(tipo_salvamento)
                
                if tipo_salvamento not in ["1", "2", "3"]:
                    print(f"\n{r}{color.c('y')}Ação inválida. Tente novamente.{r}")
                    continue
                
                match tipo_salvamento:
                    case "2":
                        dados = {"texto": hashchain.info(0), "chave": None}
                    case "3":
                        dados = {"texto": None, "chave": hashchain.info(1)}
                    case "1":
                        dados = {"texto": hashchain.info(0), "chave": hashchain.info(1)}
                
                break
            
            try:
                project_root = next(
                    (p for p in Path(__file__).resolve().parents
                     if p.name == "HashChain---encryption"),
                    None
                )
                
                if not project_root:
                    raise FileNotFoundError(
                        f"{r}{color.c('r')}Diretório 'HashChain---encryption' não encontrado.{r}"
                    )
                
                outputs_dir = project_root / "outputs"
                outputs_dir.mkdir(exist_ok=True)
                
                agora = datetime.datetime.now()
                milissegundos = int(agora.microsecond / 1000)
                file_name = agora.strftime(f"log_%Y-%m-%d_%H-%M-%S-{milissegundos:03d}.json")
                log_path = outputs_dir / file_name
                
                with open(log_path, "x", encoding="utf-8") as file:
                    json.dump(dados, file, ensure_ascii=False, indent=4)
                
                print(f"\n{r}{color.c('b')}Log salvo em: {r}{color.format(faint=True)}{log_path}{r}")
                
            except Exception as e:
                print(f"{r}{color.c('r')}Erro: Ocorreu um erro ao tentar criar o arquivo:{r} ", e)
            
            print(f"\n{r}{color.c('g')}O arquivo foi salvo no seguinte modelo: "
                  f"{bold}log_YYYY-MM-DD_HH-MM-SS-MMM.json,{r}{color.c('g')} "
                  f"e pode ser encontrado na pasta outputs.{r}")
            break
        else:
            break


def handle_decrypt():
    """Lida com a descriptografia."""
    global hashchain
    
    handler = Handler()
    
    # Escolher fonte
    while Stable:
        log_input = input(
            f"\n{r}{color.c('c', True)}Deseja usar um arquivo de log para descriptografia? "
            f"{r}{bold}(s/n){r}: "
        ).strip().lower()
        
        check_action(log_input)
        
        if log_input not in yes_aliases + no_aliases:
            print(f"{r}\n{color.c('y')}Ação inválida. Tente novamente.{r}")
            continue
        else:
            break
    
    log_input_bool = True if log_input in yes_aliases else False
    
    if log_input_bool and handler.find_outputs_folder() is not None and handler.list_output_files() is not None:
        # Usar log
        texto, key = load_from_log(handler)
    else:
        if log_input_bool:
            print(f"\n{r}{color.c('y')}Não é possível usar os arquivos de logs pois, "
                  f"a pasta não foi encontrada ou não possui logs.{r}")
            while Stable:
                continuar = input(
                    f"\n{r}{color.c('c', True)}Deseja utiliza o metodo normal de descriptografia? "
                    f"{r}{bold}(s/n): {r}"
                )
                check_action(continuar)
                
                if continuar not in yes_aliases + no_aliases:
                    print(f"\n{r}{color.c('y')}Ação inválida. Tente novamente.{r}\n")
                    continue
                else:
                    break
            
            if continuar not in yes_aliases:
                close_program()
                return
        
        # Entrada manual
        texto = input(f"\n{r}{color.c('c', True)}Digite o texto a ser descriptografado: {r}")
        key = input(f"\n{r}{color.c('c', True)}Digite a chave para descriptografia: {r}")
    
    # Descriptografar
    try:
        if len(texto) > 100_000:
            print(f'\n{r}{color.c("y", faint=True)}Aviso: A o texto criptografado fornecido '
                  f'excede 100Kb, a descriptografia pode levar alguns instantes. Por favor aguarde...{r}')
        
        hashchain.decrypt(texto, key)
    except Exception:
        print(f"\n{color.c('r')}Erro: Valores para descriptografia {bold}inválidos,{r} "
              f"{color.c('r')}verifique de o log foi adulterado.{r}")
    else:
        print(f"\n{color.c('g')}Descriptografia realizada com sucesso.\n{r}")
        print(f'{r}{color.c('b')}Texto descriptografado: {r}')
        print(f'{r}{color.format(faint=True)}{hashchain.info(3)}{r}')
        
        # Salvar opcional
        while Stable:
            salvar_decrip_txt = input(
                f'{r}{color.c('c', True)}\nDeseja salvar o texto descriptografado em um arquivo de texto? '
                f"{r}{bold}(s/n): {r}"
            )
            check_action(salvar_decrip_txt)
            
            if salvar_decrip_txt not in yes_aliases + no_aliases:
                print(f"\n{r}{color.c('y')}Ação inválida. Tente novamente.{r}\n")
                continue
            
            if salvar_decrip_txt in no_aliases:
                break
            else:
                handler.save_file(hashchain.info(3))
                break


def load_from_log(handler):
    """Carrega texto e chave de um arquivo de log."""
    global yes_aliases, no_aliases
    
    while Stable:
        mostrar_logs = input(
            f"\n{r}{color.c('c', True)}Deseja ver uma lista dos logs disponíveis? "
            f"{r}{bold}(s/n):{r} "
        )
        check_action(mostrar_logs)
        
        if mostrar_logs not in yes_aliases + no_aliases:
            print(f"\n{r}{color.c('y')}Ação inválida. Tente novamente.{r}")
            continue
        else:
            break
    
    if mostrar_logs in yes_aliases:
        logs_list = handler.list_output_files()
        if logs_list:
            while Stable:
                print(f"\n{bold}Lista dos logs disponíveis:{r}\n")
                Handler.print_menu(logs_list)
                log_escolhido = input(
                    f"\n{r}{color.c('p')}Digite o número do log que deseja usar: "
                    f"{r}{color.format(faint=True)}"
                )
                check_action(log_escolhido)
                
                try:
                    log_escolhido = int(log_escolhido)
                except Exception:
                    print(f"{r}\n{color.c('y')}Ação inválida. Tente novamente.{r}")
                    continue
                else:
                    if 1 <= log_escolhido <= len(logs_list):
                        break
                    else:
                        print(f"\n{r}{color.c('y')}Ação inválida. Tente novamente.{r}")
                        continue
            
            nome_log = logs_list[log_escolhido - 1]
            outputs_path = handler.find_outputs_folder()
            log_path = os.path.join(outputs_path, nome_log)
        else:
            texto = input(f"\n{r}{color.c('c', True)}Digite o texto a ser descriptografado: {r}")
            key = input(f"\n{r}{color.c('c', True)}Digite a chave para descriptografia: {r}")
            return texto, key
    else:
        outputs_path = handler.find_outputs_folder()
        while Stable:
            log_name = input(
                f"\n{r}{color.c('c', True)}Digite o nome do log "
                f"(ex: log_2025-10-31_19-40-00-123.json):{r} "
            ).strip()
            
            log_path = os.path.join(outputs_path, log_name)
            
            if not os.path.exists(log_path):
                print(f"\n{color.c('r')}Erro: O arquivo '{log_name}' não foi encontrado em '{outputs_path}'.{r}")
                print("\nTente novamente.")
                continue
            else:
                break
    
    try:
        with open(log_path, "r", encoding="utf-8") as file:
            dados = json.load(file)
            
            if dados.get('texto') and dados.get('chave'):
                tipo_log = 1
            elif dados.get('texto') and not dados.get('chave'):
                tipo_log = 2
            elif not dados.get('texto') and dados.get('chave'):
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
                case _:
                    raise ValueError("Log inválido")
            
            return texto, key
            
    except FileNotFoundError:
        print(f"{color.c('y')}Arquivo não encontrado. Tente novamente.{r}")
        texto = input(f"\n{r}{color.c('c', True)}Digite o texto a ser descriptografado: {r}")
        key = input(f"\n{r}{color.c('c', True)}Digite a chave para descriptografia: {r}")
        return texto, key
    except json.JSONDecodeError:
        print(f"{color.c('r')}Erro: arquivo JSON inválido. Tente novamente com um log gerado pelo programa.{r}")
        texto = input(f"\n{r}{color.c('c', True)}Digite o texto a ser descriptografado: {r}")
        key = input(f"\n{r}{color.c('c', True)}Digite a chave para descriptografia: {r}")
        return texto, key


def handle_compress():
    """Lida com compressão."""
    global hashchain
    
    texto = input(f"\n{r}{color.c('c', True)}Digite o texto a ser comprimido: {r}")
    print(f"\n{color.c('b')}Texto comprimido:{r}")
    resultado = hashchain.compression(texto)
    if resultado is not None:
        print(f'{r}{color.format(faint=True)}{resultado}{r}')


def handle_decompress():
    """Lida com descompressão."""
    global hashchain
    
    texto = input(f"\n{r}{color.c('c', True)}Digite o texto a ser descomprimido: {r}").upper()
    print(f"\n{color.c('b')}Texto descomprimido:{r}")
    resultado = hashchain.decompression(texto)
    if resultado is not None and not resultado.startswith("Erro"):
        print(f'{r}{color.format(faint=True)}{resultado}{r}')


def handle_web_interface():
    """Inicia a interface web."""
    # Verifica se Flask está disponível antes de continuar
    try:
        from hashchain.interfaces.web import FLASK_AVAILABLE, run_web
        
        if not FLASK_AVAILABLE:
            print(f"\n{r}{color.c('r')}Erro: Flask não está instalado!{r}")
            print(f"{r}{color.c('y')}Instale com: pip install Flask{r}")
            print(f"{r}{color.format(faint=True)}Voltando ao menu principal...{r}\n")
            return
    except ImportError as e:
        print(f"\n{r}{color.c('r')}Erro: Flask não está instalado!{r}")
        print(f"{r}{color.c('y')}Instale com: pip install Flask{r}")
        print(f"{r}{color.format(faint=True)}Voltando ao menu principal...{r}\n")
        return
    
    print(f"\n{r}{color.c('c', True)}Iniciando interface web...{r}")
    print(f"{r}{color.format(faint=True)}A interface web será aberta no seu navegador.{r}")
    print(f"{r}{color.format(faint=True)}Pressione Ctrl+C no terminal para parar o servidor.{r}\n")
    
    # Pergunta sobre host e porta
    while Stable:
        host_input = input(
            f"{r}{color.c('c', True)}Digite o host (Enter para 127.0.0.1):{r} "
        ).strip()
        
        check_action(host_input)
        
        if not host_input:
            host = '127.0.0.1'
            break
        else:
            host = host_input
            break
    
    while Stable:
        port_input = input(
            f"{r}{color.c('c', True)}Digite a porta (Enter para 5000):{r} "
        ).strip()
        
        check_action(port_input)
        
        if not port_input:
            port = 5000
            break
        else:
            try:
                port = int(port_input)
                if port < 1 or port > 65535:
                    print(f"\n{r}{color.c('y')}Porta inválida. Use um número entre 1 e 65535.{r}")
                    continue
                break
            except ValueError:
                print(f"\n{r}{color.c('y')}Porta inválida. Digite um número.{r}")
                continue
    
    # Inicia o servidor web
    try:
        run_web(host=host, port=port, debug=False)
        # Após fechar o servidor, volta ao menu
        print(f"\n{r}{color.format(faint=True)}Voltando ao menu principal...{r}\n")
    except KeyboardInterrupt:
        print(f"\n{r}{color.format(faint=True)}Servidor web interrompido.{r}")
        print(f"{r}{color.format(faint=True)}Voltando ao menu principal...{r}\n")
    except Exception as e:
        print(f"\n{r}{color.c('r')}Erro ao iniciar interface web: {e}{r}")
        print(f"{r}{color.format(faint=True)}Voltando ao menu principal...{r}\n")


def handle_help():
    """Mostra ajuda."""
    print(f"\n{r}{bold}Ajuda - HashChain Encryption System{r}")
    
    while Stable:
        print(f'{r}{bold}\nEscolha uma opção de ajuda:{r}\n')
        ajuda_input_list = [
            'Sobre o HashChain', 'Como usar o programa', 'Explicação dos parâmetros',
            'Explicação da decriptação', 'Explicação da compressão e descompressão',
            'Voltar ao menu principal'
        ]
        Handler.print_menu(ajuda_input_list)
        ajuda_input = input(
            f"{r}{color.c('p')}\nDigite o número da ação desejada:"
            f"{r}{color.format(faint=True)} "
        ).strip()
        
        check_action(ajuda_input)
        
        if ajuda_input not in ["1", "2", "3", "4", "5", "6"]:
            print(f"\n{r}{color.c('y')}Ação inválida. Tente novamente.{r}")
            continue
        
        print()
        match ajuda_input:
            case "1":
                print(f"{r}{color.c('b')}{ajuda_input_list[0]}:{r}")
                print(f"{r}{color.format(faint=True)}{italic} - O HashChain é um sistema de criptografia "
                      f"que utiliza cadeias de funções hash para garantir a segurança dos dados. "
                      f"Ele permite a criptografia e descriptografia de textos, além de oferecer "
                      f"funcionalidades de compressão e descompressão.")
            case "2":
                print(f"{r}{color.c('b')}{ajuda_input_list[1]}:{r}")
                print(f"{r}{color.format(faint=True)}{italic} - Para usar o programa, escolha entre o modo "
                      f"terminal ou a interface gráfica (se disponível). Siga as instruções na tela para "
                      f"criptografar, descriptografar, comprimir ou descomprimir textos.")
            case "3":
                print(f"{r}{color.c('b')}{ajuda_input_list[2]}:{r}")
                print(f"{r}{italic} - Seed:{color.format(faint=True)} É um número inteiro de no mínimo 8 "
                      f"dígitos, inicial usado para gerar a cadeia de hash.\n - {r}{italic}Passos:"
                      f"{color.format(faint=True)} Uma lista de inteiros que define as etapas da cadeia "
                      f"de hash. (Cada inteiro deve estar entre 20 a 999)\n - {r}{italic}Salt:"
                      f"{color.format(faint=True)} Uma medida de segurança adicional que pode ser usada "
                      f"durante a criptografia para aumentar a aleatoriedade do processo.{r}")
            case "4":
                print(f"{r}{color.c('b')}{ajuda_input_list[3]}:{r}")
                print(f"{r}{color.format(faint=True)}{italic} - A descriptografia requer o texto criptografado "
                      f"e a chave gerada durante a criptografia. O HashChain utiliza a cadeia de hash "
                      f"inversa para recuperar o texto original. Durante a criptografia, esses dados podem "
                      f"ser salvos em um arquivo de log para facilitar a descriptografia posterior, "
                      f"copiando e colando o seu caminho relativo a pasta atual.")
            case "5":
                print(f"{r}{color.c('b')}{ajuda_input_list[4]}:{r}")
                print(f"{r}{color.format(faint=True)}{italic} - A compressão reduz o tamanho do texto "
                      f"utilizando algoritmos específicos para compresão de números binários, enquanto a "
                      f"descompressão reverte esse processo para recuperar o texto original.")
            case "6":
                print(f"\n{r}{color.format(faint=True)}Voltando ao menu principal.{r}")
                break


if __name__ == "__main__":
    main()
    close_program()
