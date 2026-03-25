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
    print("Aluno cadastrado com sucesso\n")

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

def atualizarCadastro(alunos, cursos):
    print("Atualizar cadastro\n")
    matricula = input("Informe a matricula: ").upper()

    for aluno in alunos:
        if aluno["matricula"] == matricula:
            print("Aluno encontrado\n")
            print(f"Nome: {aluno['nome']}")
            print(f"Email: {aluno['email']}")
            print(f"Curso: {aluno['curso']}")
            print(f"Matrícula: {aluno['matricula']}")

            print("Informe os novos dados:\n")

            aluno['nome'] = input("Digite o nome: ")
            aluno['email'] = input("Digite o email: ")

            novo_curso = input("Digite o curso: ").upper()
            
            if novo_curso != aluno['curso']:
                if novo_curso not in cursos:
                    cursos[novo_curso] = 0

                cursos[novo_curso] += 1

                aluno['curso'] = novo_curso
                aluno['matricula'] = novo_curso + str(cursos[novo_curso])

            print("Cadastro atualizado com sucesso\n")
            return

    print("Aluno não encontrado\n")

def excluirCadastro(alunos):
    print("Excluir cadastro\n")

    matricula = input("Informe a matricula do aluno: ").upper()

    for aluno in alunos:
        if aluno["matricula"] == matricula:
            print("Aluno encontrado\n")
            print(f"Nome: {aluno['nome']}")
            print(f"Matrícula: {aluno['matricula']}")

        conf = input("Confirmar exclusão? (s/n) ").lower()

        if conf == 's':
            alunos.remove(aluno)
            print("Aluno excluido com sucesso\n")
        elif conf == 'n':
            print("Exclusão cancelada")
            print("-" * 10)
            return
        else:
            print("Opção invalida\n")
