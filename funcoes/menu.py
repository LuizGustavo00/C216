def criar():
    print("Bem vindo ao menu!\n")
    print("1 - Cadastrar novo aluno")
    print("2 - Listar alunos")
    print("3 - Atualizar cadastro")
    print("4 - Excluir cadastro")
    print("0 - Sair")



def cadastrar(alunos,cursos):
    print("Cadastro de novo aluno\n")

    nome = input("Digite o nome: ")
    email = input("Digite o email: ")
    curso = input("Digite o curso: ").upper()

    if curso not in cursos:
        cursos[curso] = 0
    
    cursos[curso] += 1

    aluno = {"nome": nome, "email": email, "curso": curso, "matricula": curso+str(cursos[curso])}

    alunos.append(aluno)


def mostrarLista(alunos):
    if len(alunos) == 0:
        print("Nenhum aluno cadastrado")

    else:
        print("Lista de alunos\n")

        for aluno in alunos:
            print(f"Nome: {aluno['nome']}")
            print(f"Email: {aluno['email']}")
            print(f"Curso: {aluno['curso']}")
            print(f"Matrícula: {aluno['matricula']}")
            print("-" * 30)

def atualizarCadastro(alunos):
    print("Atualizar cadastro\n")
    matricula = input("Informe a matricula: ").upper()
    for aluno in alunos:
        if aluno["matricula"] == matricula:
            print("Aluno encontrado")
            print(f"Nome: {aluno['nome']}")
            print(f"Email: {aluno['email']}")
            print(f"Curso: {aluno['curso']}")
            print(f"Matrícula: {aluno['matricula']}")

            print("Informe os novos dados: \n")
            nome = input("Digite o nome: ")
            email = input("Digite o email: ")
            curso = input("Digite o curso: ").upper()
            matricula = curso+str(cursos[curso])
            
        else:
            print ("aluno não encontrado")

def excluirCadastro(alunos):
    print("Excluir cadastro\n")

    matricula = input("Informe a matricula do aluno: ").upper()

    for aluno in alunos:
        if aluno["matricula"] == matricula:
            print("Aluno encontrado")
            print(f"Nome: {aluno['nome']}")
            print(f"Matrícula: {aluno['matricula']}")

        conf = input("Confirmar exclusão? (s/n) ").lower()

        if conf == 's':
            alunos.remove(aluno)
            print("Aluno excluido com sucesso")
        elif conf == 'n':
            print("Exclusão cancelada")
            print("-" * 10)
            return
        else:
            print("Opção invalida")
