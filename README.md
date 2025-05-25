# 📚 Gerenciador de Livros

Um aplicativo de desktop feito em **Python** com **Tkinter** e **SQLite** para gerenciamento de livros. Permite cadastrar, consultar, editar, remover e exportar livros para JSON. Também conta com busca rápida e alternância entre modo claro e escuro.

![image](https://github.com/user-attachments/assets/623b417f-e1b2-4ee3-a8c3-bc918cacf672)

## ✨ Funcionalidades

- ✅ Cadastrar novos livros (nome, autor e editora)
- 🔍 Buscar por nome, autor ou editora em tempo real
- ✏️ Editar informações de livros existentes
- 🗑️ Remover livros da lista
- 📄 Exportar todos os livros para um arquivo `.json`
- 🌙 Alternar entre **modo claro** e **modo escuro**

---

## 💻 Tecnologias Utilizadas

- Python 3
- Tkinter (interface gráfica)
- SQLite (banco de dados)
- JSON (exportação)
- `ttk` para componentes visuais

---

## 📂 Organização do Projeto
📁 gerenciador-livros/

├── livros.db # Banco de dados SQLite

![image](https://github.com/user-attachments/assets/4abd4179-ed42-49e6-84aa-18e034e7e03b)

├── livros_export.json # Exportação de livros em JSON

![image](https://github.com/user-attachments/assets/e234be29-8db9-43b1-b933-f0d788c32d22)

├── main.py # Código principal da aplicação

├── README.md # Documentação do projeto

└── docs/

📝 Exemplo de Uso

    Digite no campo de busca para filtrar livros instantaneamente.

    Clique em Cadastrar para adicionar um novo livro.

    Selecione um item na lista e use os botões para editar, remover ou consultar detalhes.

    Clique em Exportar JSON para salvar todos os livros em livros_export.json.

    Use Modo Claro/Escuro para alternar entre os temas da interface.

📸 Imagem da Interface

![image](https://github.com/user-attachments/assets/835968cb-41ae-4799-8231-1395388b3b6e)
