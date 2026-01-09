import sys
import json
import random
import secrets
import customtkinter as ctk
from tkinter import messagebox, scrolledtext, filedialog
from HashChainClass import HashChainEncryption

HashChain: HashChainEncryption = HashChainEncryption()

# Configuração inicial
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Cores
COLOR_BG = "#001f3f"
COLOR_FRAME = "#003366"
COLOR_TEXT = "#f2f2f2"
COLOR_BTN = "#004080"
COLOR_BTN_HOVER = "#0050a0"
COLOR_ENTRY = "#003366"


# Variáveis globais
root = ctk.CTk()
seed_var = ctk.StringVar()
passo_var = ctk.StringVar()
modo_var = ctk.StringVar(value="manual")
cripto_resultado = ""
chave = ""

content_frame = ctk.CTkFrame(root, fg_color=COLOR_BG)
content_frame.pack(side="right", fill="both", expand=True)

menu_frame = ctk.CTkFrame(root, width=200, fg_color=COLOR_FRAME, corner_radius=5)
menu_frame.pack(side="left", fill="y", padx=5, pady=5)


header_label = ctk.CTkLabel(
    content_frame, text="Sistema de Criptografia", font=("Arial", 22, "bold")
)
header_label.pack(pady=(20, 10))


def limpar_content():
    for widget in content_frame.winfo_children():
        widget.destroy()


# INTERFACES
def interface_menu():
    limpar_content()
    ctk.CTkLabel(
        content_frame, text="Sistema de Criptografia", font=("Arial", 20, "bold")
    ).pack(pady=20)
    ctk.CTkLabel(
        content_frame,
        text="Feito por:\nJonathan S. Cardoso\nGabriel M. Tonioli\nGabriel P. Câmara\nVinicius A. Manini",
        font=("Arial", 13),
        anchor="e",
        justify="right"
    ).pack(pady=20, padx=(0, 20), anchor="e")
    
    def close_interface():
        root.quit()
        root.destroy()

    ctk.CTkButton(content_frame, text="Voltar ao terminal", command=close_interface).pack(pady=10, padx=10)



def interface_criptografar():
    limpar_content()

    def carregar_txt():
        path = filedialog.askopenfilename(filetypes=[("TXT", "*.txt")])
        if path:
            with open(path, "r", encoding="utf-8") as f:
                texto_entry.delete("1.0", "end")
                texto_entry.insert("1.0", f.read())

    ctk.CTkLabel(
        content_frame, text="Criptografar Texto", font=("Arial", 16, "bold")
    ).pack(pady=10)

    texto_label = ctk.CTkLabel(content_frame, text="Texto para criptografar:")
    texto_label.pack(anchor="w", padx=20)
    texto_entry = ctk.CTkTextbox(content_frame, height=100)
    texto_entry.pack(padx=20, pady=5, fill="x")

    ctk.CTkButton(
        content_frame, text="Carregar de Arquivo TXT", command=carregar_txt
    ).pack(pady=5, padx=20)

    seed_label = ctk.CTkLabel(
        content_frame, text="Seed (Opcional): Um inteiro de no mínimo 8 digitos. "
    )
    seed_label.pack(anchor="w", padx=20, pady=(10, 0))
    seed_entry = ctk.CTkEntry(content_frame, textvariable=seed_var)
    seed_entry.pack(padx=20, fill="x")

    def gerar_seed():
        seed_var.set(random.randint(10000000, 99999999999999999999999999999999))

    ctk.CTkButton(content_frame, text="Gerar Seed Aleatória", command=gerar_seed).pack(
        pady=5, padx=20
    )

    passo_label = ctk.CTkLabel(
        content_frame,
        text="Passo (Opcional): Inteiros de 20 a 999 separados por espaços. (Exemplo: 20 84 341 999)",
    )
    passo_label.pack(anchor="w", padx=20, pady=(10, 0))
    passo_entry = ctk.CTkEntry(content_frame, textvariable=passo_var)
    passo_entry.pack(padx=20, fill="x")

    has_salt_var = ctk.IntVar(value=0)

    check_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    check_frame.pack(pady=10)

    has_salt_var = ctk.IntVar(value=0)
    ctk.CTkCheckBox(
        check_frame, text="Utilizar Salt", variable=has_salt_var, onvalue=1, offvalue=0
    ).pack(side="left", padx=10)

    usar_config_padrao = ctk.IntVar(value=0)
    ctk.CTkCheckBox(
        check_frame,
        text="Usar parâmetros padronizados",
        variable=usar_config_padrao,
        onvalue=1,
        offvalue=0,
    ).pack(side="left", padx=10)

    ctk.CTkButton(
        content_frame,
        text="Criptografar",
        command=lambda: executar_criptografia(
            texto_entry.get("1.0", "end-1c"),
            seed_var.get(),
            passo_var.get(),
            has_salt_var.get(),
            usar_config_padrao.get(),
        ),
    ).pack(pady=15)


def interface_descriptografar():
    limpar_content()

    ctk.CTkLabel(
        content_frame, text="Descriptografar Texto", font=("Arial", 16, "bold")
    ).pack(pady=10)

    texto_label = ctk.CTkLabel(content_frame, text="Texto para descriptografar:")
    texto_label.pack(anchor="w", padx=20)
    texto_entry = ctk.CTkTextbox(content_frame, height=100)
    texto_entry.pack(padx=20, pady=5, fill="x")

    chave_label = ctk.CTkLabel(content_frame, text="Chave para a descriptografia:")
    chave_label.pack(anchor="w", padx=20)
    chave_entry = ctk.CTkTextbox(content_frame, height=30)
    chave_entry.pack(padx=20, pady=5, fill="x")

    def carregar_json():
        path = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if path:
            with open(path, "r", encoding="utf-8") as f:
                content = json.load(f)
                try:
                    texto_entry.delete("1.0", "end")
                    texto_entry.insert("1.0", content["texto"])
                    chave_entry.delete("1.0", "end")
                    chave_entry.insert("1.0", content["chave"])
                except Exception:
                    messagebox.showerror("Erro", "O arquivo selecionado não foi feito pelo sistema HashChain ou foi adulterado. Tente novamente com outro arquivo.")

    ctk.CTkButton(
        content_frame, text="Carregar de Arquivo JSON", command=carregar_json
    ).pack(pady=5, padx=20)

    ctk.CTkButton(
        content_frame,
        text="Descriptografar",
        command=lambda: executar_descriptografia(
            texto_entry.get("1.0", "end-1c"), chave_entry.get("1.0", "end-1c")
        ),
    ).pack(pady=20)


def mostrar_resultado(titulo, is_cripto=False):
    global cripto_resultado, chave
    limpar_content()

    ctk.CTkLabel(content_frame, text=titulo, font=("Arial", 16, "bold")).pack(pady=10)

    if is_cripto:
        ctk.CTkLabel(content_frame, text="Texto criptografado:", anchor="w").pack(
            pady=(5, 0), padx=(20, 0), fill="x"
        )

        result_box = scrolledtext.ScrolledText(
            content_frame, height=12, font=("Consolas", 12), wrap="word"
        )
        result_box.pack(padx=20, pady=10, fill="both", expand=True)
        result_box.insert("1.0", HashChain.info(0))
        result_box.configure(state="disabled")

        ctk.CTkLabel(content_frame, text="Chave:", anchor="w").pack(
            pady=(5, 0), padx=(20, 0), fill="x"
        )

        result_box2 = scrolledtext.ScrolledText(
            content_frame, height=12, font=("Consolas", 12), wrap="word"
        )
        result_box2.pack(padx=20, pady=10, fill="both", expand=True)
        result_box2.insert("1.0", HashChain.info(1))
        result_box2.configure(state="disabled")

        ctk.CTkButton(
            content_frame, text="Salvar Arquivo", command=salvar_em_arquivos
        ).pack(pady=10)

    else:
        ctk.CTkLabel(content_frame, text="Texto descriptografado:", anchor="w").pack(
            pady=(5, 0), padx=(20, 0), fill="x"
        )

        result_box = scrolledtext.ScrolledText(
            content_frame, height=12, font=("Consolas", 12), wrap="word"
        )

        def salvar_texto():
            path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Arquivo de texto", "*.txt")],
                title="Salvar texto descriptografado",
            )
            if path:
                try:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(HashChain.info(3))
                    messagebox.showinfo("Sucesso", f"Arquivo salvo em:\n{path}")
                except Exception as e:
                    messagebox.showerror(
                        "Erro", f"Não foi possível salvar o arquivo:\n{e}"
                    )

        # Botão de salvar
        result_box.pack(padx=20, pady=10, fill="both", expand=True)
        result_box.insert("1.0", HashChain.info(3))
        result_box.configure(state="disabled")
        ctk.CTkButton(
            content_frame, text="Salvar Texto Descriptografado", command=salvar_texto
        ).pack(pady=10)


# PROCESSAMENTO4
def executar_criptografia(texto, seed, passo_str, has_salt, padronizar):
    if not texto:
        messagebox.showerror("Erro", "Digite um texto.")
        return

    if padronizar == 1:
        passe = [50, 25, 60, 38]
        seed = 2388636226855438390625029635578797980511582675618534009644830601267214645928643288262357364197196387839621331
        HashChain.encrypt(texto, passe, seed, True)
    else:
        try:
            if not seed:
                seed_val = int(
                    "".join(
                        str(secrets.randbelow(10))
                        for _ in range(secrets.randbelow(65) + 64)
                    )
                )
            else:
                if len(seed) < 8:
                    raise Exception(
                        "Tamnho inválido para a seed, digite um número inteiro de no mínimo 8 caracteres"
                    )

                for char in seed:
                    if char not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                        raise Exception(
                            "Caractere inválido para a seed. (Deve ser um número inteiro)"
                        )

                seed_val = int(seed)

        except Exception as e:
            messagebox.showerror("Erro", str(e))
            return

        try:
            if not passo_str:
                passo = [
                    secrets.randbelow(979) + 20 for _ in range(secrets.randbelow(64) + 8)
                ]
            else:
                passo = [int(x) for x in passo_str.split()]
                if min(passo) < 20 or max(passo) > 999:
                    raise Exception

        except Exception as e:
            messagebox.showerror(
                "Erro",
                "O passe deve conter apenas números inteiros de 20 a 999. (Exemplo: 20 30 45 84 341 872 999)",
            )
            return

        try:
            no_salt = True if has_salt == 0 else False
            HashChain.encrypt(texto, passo, seed_val, no_salt)
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro durante a criptografia: {e}")
            return

    mostrar_resultado("Texto Criptografado", True)


def executar_descriptografia(texto, chave):
    if not texto:
        messagebox.showerror("Erro", "Digite o texto para desriptografia.")
        return
    if not chave:
        messagebox.showerror("Erro", "Digite uma chave para descriptografia.")
        return
    try:
        HashChain.decrypt(texto, chave)
    except Exception:
        messagebox.showerror(
            "Erro",
            "A descriptografia não pode ser concluida pois o texto ou a chave estão incorretos, verifique se não foram adulterados.",
        )
        return
    mostrar_resultado("Texto Descriptografado", False)


def salvar_em_arquivos():
    dados = {"texto": HashChain.info(0), "chave": HashChain.info(1)}
    texto_path = filedialog.asksaveasfilename(defaultextension=".json")
    if texto_path:
        with open(texto_path, "x", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)


# MENU
ctk.CTkButton(menu_frame, text="Início", command=interface_menu).pack(
    pady=10, padx=5, fill="x"
)
ctk.CTkButton(menu_frame, text="Criptografar", command=interface_criptografar).pack(
    pady=10, padx=5, fill="x"
)
ctk.CTkButton(
    menu_frame, text="Descriptografar", command=interface_descriptografar
).pack(pady=10, padx=5, fill="x")

# INICIALIZAÇÃO
root.title("Sistema de Criptografia")

screenX, screenY = root.winfo_screenwidth(), root.winfo_screenheight()

screenSizeX = int(screenX * 0.5)
screenSizeY = int(screenY * 0.6)

root.minsize(screenSizeX, screenSizeY)
root.maxsize(screenX, screenY)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

frame = ctk.CTkFrame(root, fg_color="#001f3f")  # azul marinho
label = ctk.CTkLabel(root, text="Título", text_color="#f2f2f2")
button = ctk.CTkButton(root, text="Ação", fg_color="#003366", hover_color="#004080")
entry = ctk.CTkEntry(
    root, fg_color="#003366", text_color="#f2f2f2", placeholder_text_color="#cccccc"
)


interface_menu()
root.mainloop()
