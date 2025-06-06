# Jules Todo List

Jules Todo List é um aplicativo web de lista de tarefas moderno, responsivo e otimizado para uso em desktop e mobile, desenvolvido com Flask.

## Funcionalidades

- Criação, edição e exclusão de tarefas
- Organização de tarefas em listas
- Painel de detalhes (drawer) para tarefas e listas
- Filtros por status (hoje, vencidas, concluídas, etc.)
- Busca rápida
- Interface responsiva e experiência mobile aprimorada
- Temas claros e escuros (theme.js)
- Usabilidade otimizada: drawer abre automaticamente ao adicionar/editar

## Instalação

### Pré-requisitos
- Python 3.10+
- pip

### Passos

1. Clone o repositório:
   ```sh
   git clone https://github.com/rodukao/jules-todo-list.git
   cd jules-todo-list
   ```
2. Crie um ambiente virtual (opcional, mas recomendado):
   ```sh
   python -m venv venv
   venv\Scripts\activate  # Windows
   # ou
   source venv/bin/activate  # Linux/Mac
   ```
3. Instale as dependências:
   ```sh
   pip install flask
   ```
4. Execute o app:
   ```sh
   flask run
   ```
   O app estará disponível em http://127.0.0.1:5000

## Estrutura dos Arquivos

- `app.py` — Backend Flask, rotas e lógica principal
- `static/estilo.css` — Estilos modernos e responsivos
- `static/theme.js` — Alternância de tema (claro/escuro)
- `templates/` — Templates HTML (Jinja2)
  - `index.html` — Página principal
  - `add_task.html`, `edit_task.html`, `edit_tasks.html` — Formulários
- `instance/tasks.db` — Banco de dados SQLite (criado automaticamente)

## Observações

- O banco de dados é criado automaticamente na primeira execução.
- Para resetar, basta apagar o arquivo `instance/tasks.db`.
- O app é totalmente responsivo: utilize em desktop ou mobile.
- Arquivos e estilos não utilizados foram removidos para facilitar manutenção.
- O projeto é para uso local/desenvolvimento. Para produção, configure variáveis de ambiente e segurança adequadas.

## Personalização

- Para alterar o tema, edite `static/theme.js`.
- Para customizar estilos, edite `static/estilo.css` (comentários explicativos no arquivo).

## Dúvidas ou Contribuições

Abra uma issue ou envie um pull request!

---

Desenvolvido por Rodukao — 2025
