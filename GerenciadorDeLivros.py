import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
import json
import os

# === CONFIGS GERAIS ===
DB_FILE = "livros.db"
JSON_FILE = "livros_export.json"
modo_escuro = False

# === BANCO DE DADOS ===
def conectar():
    return sqlite3.connect(DB_FILE)

def criar_tabela():
    with conectar() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            autor TEXT NOT NULL,
            editora TEXT NOT NULL
        )
        """)
        conn.commit()

def inserir_livro(nome, autor, editora):
    with conectar() as conn:
        conn.execute("INSERT INTO livros (nome, autor, editora) VALUES (?, ?, ?)", (nome, autor, editora))
        conn.commit()

def buscar_livros(filtro=""):
    with conectar() as conn:
        cursor = conn.cursor()
        if filtro:
            like = f"%{filtro.lower()}%"
            cursor.execute("SELECT * FROM livros WHERE LOWER(nome) LIKE ? OR LOWER(autor) LIKE ? OR LOWER(editora) LIKE ?", (like, like, like))
        else:
            cursor.execute("SELECT * FROM livros")
        return cursor.fetchall()

def editar_livro_db(id_livro, nome, autor, editora):
    with conectar() as conn:
        conn.execute("UPDATE livros SET nome=?, autor=?, editora=? WHERE id=?", (nome, autor, editora, id_livro))
        conn.commit()

def remover_livro_db(id_livro):
    with conectar() as conn:
        conn.execute("DELETE FROM livros WHERE id=?", (id_livro,))
        conn.commit()

def obter_todos_livros():
    return buscar_livros()

# === FUNÇÕES TKINTER ===
def atualizar_listbox(filtro=""):
    listbox.delete(*listbox.get_children())
    for livro in buscar_livros(filtro):
        listbox.insert('', 'end', values=livro)

def on_busca(event):
    texto = campo_busca.get()
    atualizar_listbox(filtro=texto)

def cadastrar_livro():
    nome = simpledialog.askstring("Cadastro", "Nome do livro:")
    if not nome: return
    autor = simpledialog.askstring("Cadastro", "Autor do livro:")
    if not autor: return
    editora = simpledialog.askstring("Cadastro", "Editora do livro:")
    if not editora: return

    inserir_livro(nome, autor, editora)
    atualizar_listbox(campo_busca.get())
    messagebox.showinfo("Sucesso", f"Livro cadastrado!")

def consultar_detalhes():
    item = listbox.focus()
    if not item:
        messagebox.showwarning("Consulta", "Selecione um livro.")
        return
    livro = listbox.item(item, 'values')
    info = f"ID: {livro[0]}\nNome: {livro[1]}\nAutor: {livro[2]}\nEditora: {livro[3]}"
    messagebox.showinfo("Detalhes", info)

def editar_livro():
    item = listbox.focus()
    if not item:
        messagebox.showwarning("Editar", "Selecione um livro.")
        return
    livro = listbox.item(item, 'values')
    id_livro = livro[0]

    novo_nome = simpledialog.askstring("Editar", "Novo nome:", initialvalue=livro[1])
    if not novo_nome: return
    novo_autor = simpledialog.askstring("Editar", "Novo autor:", initialvalue=livro[2])
    if not novo_autor: return
    nova_editora = simpledialog.askstring("Editar", "Nova editora:", initialvalue=livro[3])
    if not nova_editora: return

    editar_livro_db(id_livro, novo_nome, novo_autor, nova_editora)
    atualizar_listbox(campo_busca.get())
    messagebox.showinfo("Editar", "Livro atualizado!")

def remover_livro():
    item = listbox.focus()
    if not item:
        messagebox.showwarning("Remover", "Selecione um livro.")
        return
    livro = listbox.item(item, 'values')
    id_livro = livro[0]
    if messagebox.askyesno("Remover", f"Remover livro ID {id_livro}?"):
        remover_livro_db(id_livro)
        atualizar_listbox(campo_busca.get())
        messagebox.showinfo("Remover", f"Livro removido.")

def salvar_em_json():
    livros = obter_todos_livros()
    lista_dict = [{"id": l[0], "nome": l[1], "autor": l[2], "editora": l[3]} for l in livros]
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(lista_dict, f, indent=4)
    messagebox.showinfo("Exportar JSON", "Livros exportados para JSON com sucesso!")

def alternar_tema():
    global modo_escuro
    modo_escuro = not modo_escuro

    cor_fundo = "#1e1e1e" if modo_escuro else "#f4f4f8"
    cor_texto = "#ffffff" if modo_escuro else "#000000"
    cor_tabela = "#2e2e2e" if modo_escuro else "white"

    root.configure(bg=cor_fundo)
    frame_botoes.configure(bg=cor_fundo)
    campo_busca.configure(bg=cor_tabela, fg=cor_texto, insertbackground=cor_texto)
    titulo.configure(bg=cor_fundo, fg=cor_texto)

    style.configure("Treeview", background=cor_tabela, foreground=cor_texto, fieldbackground=cor_tabela)
    style.configure("Treeview.Heading", background="#333", foreground="#fff" if modo_escuro else "#000")

    for widget in frame_botoes.winfo_children():
        widget.configure(style="TButton")

# === INTERFACE TK ===
root = tk.Tk()
root.title("📚 Gerenciador de Livros - feito por Evilly Rolim")
root.geometry("800x500")
root.configure(bg="#f4f4f8")

style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Arial", 10), padding=6)
style.configure("Treeview", font=("Arial", 10), rowheight=25)
style.configure("Treeview.Heading", font=("Arial", 11, "bold"))

# Título
titulo = tk.Label(root, text="📚 Gerenciador de Livros", bg="#f4f4f8", font=("Helvetica", 16, "bold"), fg="#333")
titulo.pack(pady=10)

# Campo de busca
campo_busca = tk.Entry(root, font=("Arial", 11), width=40)
campo_busca.pack(pady=5)
campo_busca.bind("<KeyRelease>", on_busca)

# Tabela
colunas = ("ID", "Nome", "Autor", "Editora")
listbox = ttk.Treeview(root, columns=colunas, show="headings")
for col in colunas:
    listbox.heading(col, text=col)
    listbox.column(col, anchor=tk.CENTER, width=140)

listbox.pack(pady=8, fill='both', expand=True)

# Botões
frame_botoes = tk.Frame(root, bg="#f4f4f8")
frame_botoes.pack(pady=10)

botoes = [
    ("Cadastrar", cadastrar_livro),
    ("Detalhes", consultar_detalhes),
    ("Editar", editar_livro),
    ("Remover", remover_livro),
    ("Exportar JSON", salvar_em_json),
    ("Modo Claro/Escuro", alternar_tema),
    ("Sair", root.quit)
]

for texto, comando in botoes:
    ttk.Button(frame_botoes, text=texto, command=comando).pack(side=tk.LEFT, padx=5)

# Inicialização
criar_tabela()
atualizar_listbox()
root.mainloop()
