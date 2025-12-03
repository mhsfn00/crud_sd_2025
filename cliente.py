import xmlrpc.client
import os

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    try:
        proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")
    except Exception as e:
        print(f"Erro ao conectar: {e}")
        return

    while True:
        print("\n--- SISTEMA DE CADASTRO UNIVERSITÁRIO ---")
        print("1. Cadastrar Aluno (Criar)")
        print("2. Buscar Aluno (Ler)")
        print("3. Atualizar Aluno (Atualizar)")
        print("4. Remover Aluno (Excluir)")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")

        try:
            if opcao == '1':
                nome = input("Nome do Aluno: ")
                curso = input("Curso: ")
                resultado = proxy.criar(nome, curso)
                print(f"\nServidor: {resultado}")

            elif opcao == '2':
                print("Buscar por: [1] ID  [2] Parte do Nome")
                tipo = input("Opção: ")
                if tipo == '1':
                    valor = int(input("Digite o ID: "))
                    print(f"\n{proxy.ler('id', valor)}")
                elif tipo == '2':
                    valor = input("Digite parte do nome: ")
                    print(f"\n{proxy.ler('nome', valor)}")
                else:
                    print("Opção inválida")

            elif opcao == '3':
                id_alvo = int(input("ID do aluno a atualizar: "))
                novo_nome = input("Novo Nome: ")
                novo_curso = input("Novo Curso: ")
                print(f"\nServidor: {proxy.atualizar(id_alvo, novo_nome, novo_curso)}")

            elif opcao == '4':
                id_alvo = int(input("ID do aluno a excluir: "))
                print(f"\nServidor: {proxy.excluir(id_alvo)}")

            elif opcao == '0':
                print("Saindo")
                break
            else:
                print("Opção inválida")
        
        except ConnectionRefusedError:
            print("\nERRO: Não foi possível conectar ao servidor")
            break
        except Exception as e:
            print(f"\nERRO: {e}")

        input("\nEnter para continuar")
        limpar_tela()

if __name__ == "__main__":
    main()