from funcoes import menu
from funcoes import config

def main():

    alunos = []
    cursos = {}

    des = True

    while des == True:
        
        menu.criar()
        op = input()

        match op:
            case "0":
                print("Finalizando...")
                des = False
            case "1":
                menu.cadastrar(alunos,cursos)
            case "2":
                menu.mostrarLista(alunos)
            case "3":
                menu.atualizarCadastro(alunos,cursos)
            case "4":
                menu.excluirCadastro(alunos)

if __name__ == "__main__":
    main()
