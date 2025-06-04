# Jules Todo List

Jules Todo List é um gerenciador de tarefas moderno, responsivo e colaborativo, desenvolvido em parceria com a IA Jules e o GitHub Copilot do Visual Studio Code.

## Funcionalidades

- **Adicionar, editar e excluir tarefas** com título, descrição, data de vencimento, prioridade e associação a listas.
- **Marcar tarefas como concluídas ou pendentes** diretamente na lista.
- **Filtros inteligentes** na barra lateral:
  - Pendentes
  - Hoje
  - Próximos 7 Dias
  - Vencidas
  - Concluídas
- **Contadores de tarefas** ao lado de cada filtro e lista, mostrando a quantidade de tarefas correspondente.
- **Listas personalizadas**:
  - Crie, edite e exclua listas.
  - Cada lista pode ter nome, descrição e cor personalizada.
  - Ao excluir uma lista, as tarefas associadas permanecem (ficam sem lista).
- **Visualização de tarefas por lista**: clique em uma lista para filtrar as tarefas e editar suas informações.
- **Pesquisa de tarefas** por título ou descrição.
- **Design responsivo**:
  - No mobile, a coluna central é exibida por padrão, com botão de menu para abrir a barra lateral.
  - Ao clicar em uma tarefa ou lista, a coluna de detalhes aparece como overlay, com botão de voltar.
- **Interface moderna** com ícones, cores e navegação fluida.

## Instalação e uso

1. Clone o repositório:
   ```sh
   git clone https://github.com/seu-usuario/jules-todo-list.git
   cd jules-todo-list
   ```
2. Crie e ative um ambiente virtual:
   ```sh
   python -m venv venv
   venv\Scripts\activate  # Windows
   # ou
   source venv/bin/activate  # Linux/Mac
   ```
3. Instale as dependências:
   ```sh
   pip install -r requirements.txt
   ```
4. Execute a aplicação:
   ```sh
   python app.py
   ```
5. Acesse em [http://localhost:5000](http://localhost:5000)

## Estrutura do Projeto

```
jules-todo-list/
├── app.py                # Backend Flask
├── static/               # CSS, JS, ícones
├── templates/            # Templates HTML
├── instance/tasks.db     # Banco de dados SQLite (criado automaticamente)
├── README.md             # Este arquivo
```

## Observações
- Ao excluir uma lista, as tarefas associadas permanecem (ficam sem lista).
- O banco de dados é criado automaticamente na primeira execução.
- O projeto é para uso local/desenvolvimento. Para produção, configure variáveis de ambiente e segurança adequadas.

---

Desenvolvido por [Seu Nome] em parceria com a IA Jules e o Copilot do Visual Studio Code.
