# TeamTasks

[![CI/CD Pipeline](https://github.com/davisakamoto/team-tasks/actions/workflows/tests.yml/badge.svg)](https://github.com/davisakamoto/team-tasks/actions/workflows/tests.yml)

---

## Integrantes do Grupo

* Arthur Pereira Carvalho
* Davi Carvalho dos Santos
* Davi Sakamoto Lamounier

---

## Descrição do Sistema

**TeamTasks** é uma plataforma desenvolvida para centralizar e simplificar a gestão de projetos em equipes pequenas. A aplicação oferece a um gerente ou líder de equipe um painel de controle unificado para visualizar todos os membros, criar e delegar tarefas, e monitorar o status de cada uma em tempo real.

O design da aplicação foi focado na eficiência, permitindo que o usuário filtre e encontre informações cruciais rapidamente, seja buscando por um membro específico ou filtrando tarefas por seu status de conclusão (Pendentes, Atrasadas ou Concluídas).

---

## Tecnologias Utilizadas

O projeto foi construído utilizando um conjunto de tecnologias modernas para garantir qualidade, segurança e manutenibilidade.

| Categoria              | Tecnologias                                                                    |
| ---------------------- | ------------------------------------------------------------------------------ |
| **Backend** | `Python`, `Django`, `SQLite`                                                   |
| **Frontend** | `HTML5`, `Tailwind CSS`, `JavaScript`                                          |
| **Testes & Qualidade** | `Coverage.py` (Cobertura de Testes), `Black` (Formatador), `Flake8` (Linter) |
| **DevOps** | `Git`, `GitHub`, `GitHub Actions` (CI/CD)                                      |

---

## Informações para Desenvolvedores

Esta seção contém informações técnicas sobre como instalar, executar e testar o projeto.

### Como Rodar o Projeto Localmente

Siga os passos abaixo para configurar e executar o projeto em sua máquina local.

**Pré-requisitos:**
* Python 3.10 ou superior
* Git

**Instalação:**

1.  **Clone o repositório:**
    ```sh
    git clone [https://github.com/davisakamoto/team-tasks.git](https://github.com/davisakamoto/team-tasks.git)
    cd team-tasks
    ```

2.  **Crie e ative um ambiente virtual:**
    ```sh
    # Criar venv
    python3 -m venv venv

    # Ativar venv (macOS/Linux)
    source venv/bin/activate
    # No Windows, use: venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Execute as migrações do banco de dados:**
    ```sh
    python manage.py migrate
    ```

5.  **Inicie o servidor de desenvolvimento:**
    ```sh
    python manage.py runserver
    ```

6.  Abra seu navegador e acesse `http://127.0.0.1:8000/`.

### Executando os Testes

Este projeto possui uma suíte de testes completa para garantir a qualidade e a estabilidade do código.

1.  **Executar todos os testes:**
    ```sh
    python manage.py test
    ```

2.  **Verificar a cobertura de testes e gerar o relatório HTML:**
    ```sh
    coverage run manage.py test
    coverage html
    ```
    Após a execução, abra o arquivo `htmlcov/index.html` para ver o relatório detalhado.

### Pipeline de CI/CD

O projeto está configurado com um workflow de Integração e Entrega Contínua utilizando **GitHub Actions**. A cada `push` ou `pull request` para a branch `main`, o pipeline executa automaticamente as seguintes tarefas:

1.  **Verificação de Qualidade:** Executa `flake8` e `black` para garantir a conformidade do código com os padrões de estilo.
2.  **Testes Automatizados:** Roda a suíte de testes completa em uma matriz que inclui os sistemas operacionais **Linux, macOS e Windows**, garantindo a compatibilidade multiplataforma.
3.  **Análise de Cobertura:** O job principal de qualidade também verifica se a cobertura de testes se mantém acima de 95%, falhando o build caso contrário.
