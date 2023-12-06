import sqlite3
import getpass

# Conexão com o banco de dados SQLite
conn = sqlite3.connect('empresa.db')
cursor = conn.cursor()

# Criação da tabela de funcionários
cursor.execute('''
    CREATE TABLE IF NOT EXISTS funcionarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
''')

# Criação da tabela de itens
cursor.execute('''
    CREATE TABLE IF NOT EXISTS itens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        descricao TEXT
    )
''')

# Função para cadastrar um novo funcionário
def cadastrar_funcionario():
    username = input("Digite o nome de usuário: ")
    password = getpass.getpass("Digite a senha: ")

    cursor.execute('INSERT INTO funcionarios (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    print("Funcionário cadastrado com sucesso!")

# Função para realizar login
def login():
    username = input("Nome de usuário: ")
    password = getpass.getpass("Senha: ")

    cursor.execute('SELECT * FROM funcionarios WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()

    if user:
        print("Login bem-sucedido!")
        return True
    else:
        print("Credenciais inválidas. Tente novamente.")
        return False

# Funções para operações CRUD de itens
def criar_item():
    nome = input("Nome do item: ")
    descricao = input("Descrição do item: ")

    cursor.execute('INSERT INTO itens (nome, descricao) VALUES (?, ?)', (nome, descricao))
    conn.commit()
    print("Item criado com sucesso!")

def listar_itens():
    cursor.execute('SELECT * FROM itens')
    itens = cursor.fetchall()

    if itens:
        for item in itens:
            print(f"ID: {item[0]}, Nome: {item[1]}, Descrição: {item[2]}")
    else:
        print("Nenhum item encontrado.")

def atualizar_item():
    listar_itens()
    item_id = input("Digite o ID do item que deseja atualizar: ")
    novo_nome = input("Novo nome do item: ")
    nova_descricao = input("Nova descrição do item: ")

    cursor.execute('UPDATE itens SET nome = ?, descricao = ? WHERE id = ?', (novo_nome, nova_descricao, item_id))
    conn.commit()
    print("Item atualizado com sucesso!")

def deletar_item():
    listar_itens()
    item_id = input("Digite o ID do item que deseja excluir: ")

    cursor.execute('DELETE FROM itens WHERE id = ?', (item_id,))
    conn.commit()
    print("Item excluído com sucesso!")

# Função para buscar itens por nome utilizando LIKE
def buscar_item():
    nome_item = input("Digite o nome do item que deseja buscar: ")
    cursor.execute('SELECT * FROM itens WHERE nome LIKE ?', ('%' + nome_item + '%',))
    itens_encontrados = cursor.fetchall()

    if itens_encontrados:
        for item in itens_encontrados:
            print(f"ID: {item[0]}, Nome: {item[1]}, Descrição: {item[2]}")
    else:
        print("Nenhum item encontrado com esse nome.")

def buscar_item_descricao():
    descricao_item = input("Digite a descrição do item que deseja buscar: ")
    cursor.execute('SELECT * FROM itens WHERE descricao LIKE ?', ('%' + descricao_item + '%',))
    itens_encontrados = cursor.fetchall()
    if itens_encontrados:
        for item in itens_encontrados:
            print(f"ID: {item[0]}, Nome: {item[1]}, Descrição: {item[2]}")
    else:
        print("Nenhum item encontrado com esse nome.")

# Loop principal do programa
try:
    while True:
        print("\n### Menu ###")
        print("1. Cadastrar funcionário")
        print("2. Login")
        print("3. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            cadastrar_funcionario()
        elif opcao == '2':
            if login():
                while True:
                    print("\n### Menu Logado ###")
                    print("1. Criar item")
                    print("2. Listar itens")
                    print("3. Atualizar item")
                    print("4. Deletar item")
                    print("5. Buscar item por nome")
                    print("6. Buscar item por descrição")
                    print("7. Sair")

                    opcao_logado = input("Escolha uma opção: ")

                    if opcao_logado == '1':
                        criar_item()
                    elif opcao_logado == '2':
                        listar_itens()
                    elif opcao_logado == '3':
                        atualizar_item()
                    elif opcao_logado == '4':
                        deletar_item()
                    elif opcao_logado == '5':
                        buscar_item()
                    elif opcao_logado == '6':
                        buscar_item_descricao()
                    elif opcao_logado == '7':
                        break
                    else:
                        print("Opção inválida.")
        elif opcao == '3':
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida.")

except Exception as e:
    print(f"Ocorreu um erro: {e}")

finally:
    # Encerramento da conexão com o banco de dados
    conn.close()