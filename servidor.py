import xmlrpc.server
import socketserver
import threading
import os

class ThreadingXMLRPCServer(socketserver.ThreadingMixIn, xmlrpc.server.SimpleXMLRPCServer):
    pass

DB_FILE = 'alunos.txt'
file_lock = threading.Lock()

def inicializar_banco():
    if not os.path.exists(DB_FILE):
        open(DB_FILE, 'w').close()

def ler_registros():
    registros = []
    if not os.path.exists(DB_FILE):
        return registros
        
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        for linha in f:
            if linha.strip():
                id_str, nome, curso = linha.strip().split('|')
                registros.append({'id': int(id_str), 'nome': nome, 'curso': curso})
    return registros

def salvar_registros(registros):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        for r in registros:
            f.write(f"{r['id']}|{r['nome']}|{r['curso']}\n")

def criar(nome, curso):
    with file_lock:
        registros = ler_registros()
        
        novo_id = 1
        if registros:
            novo_id = max(r['id'] for r in registros) + 1
            
        novo_registro = {'id': novo_id, 'nome': nome, 'curso': curso}
        registros.append(novo_registro)
        
        salvar_registros(registros)
        print(f"[LOG] Criado: ID {novo_id} - {nome}")
        return f"Aluno cadastrado com ID: {novo_id}"

def ler(tipo_busca, valor):
    with file_lock:
        registros = ler_registros()

    resultados = []
    
    if tipo_busca == 'id':
        try:
            id_busca = int(valor)
            for r in registros:
                if r['id'] == id_busca:
                    resultados.append(r)
                    break
        except ValueError:
            return "Erro: ID deve ser um número"
            
    elif tipo_busca == 'nome':
        valor = valor.lower()
        for r in registros:
            if valor in r['nome'].lower():
                resultados.append(r)
    
    if not resultados:
        return "Nenhum resultado encontrado"
    return results_to_string(resultados)

def atualizar(id_alvo, novo_nome, novo_curso):
    with file_lock:
        registros = ler_registros()
        encontrado = False
        
        for r in registros:
            if r['id'] == id_alvo:
                r['nome'] = novo_nome
                r['curso'] = novo_curso
                encontrado = True
                break
        
        if encontrado:
            salvar_registros(registros)
            print(f"[LOG] Atualizado ID {id_alvo}")
            return "Cadastro atualizado"
        else:
            return "Erro: ID não encontrado"

def excluir(id_alvo):
    with file_lock:
        registros = ler_registros()

        novos_registros = [r for r in registros if r['id'] != id_alvo]
        
        if len(novos_registros) < len(registros):
            salvar_registros(novos_registros)
            print(f"[LOG] Excluído ID {id_alvo}")
            return "Cadastro excluído."
        else:
            return "Erro: ID não encontrado"

def results_to_string(lista):
    texto = ""
    for r in lista:
        texto += f"ID: {r['id']} | Nome: {r['nome']} | Curso: {r['curso']}\n"
    return texto

if __name__ == "__main__":
    inicializar_banco()

    PORTA = 8000
    server = ThreadingXMLRPCServer(('localhost', PORTA))
    
    print(f"Servidor rodando na porta {PORTA}")
    print("Ctrl+C para finalizar")

    server.register_function(criar, 'criar')
    server.register_function(ler, 'ler')
    server.register_function(atualizar, 'atualizar')
    server.register_function(excluir, 'excluir')
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado")