from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional

app = FastAPI(
    title="Gerenciador de Alunos",
    description="API REST para gerenciamento de alunos - C216",
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# Armazenamento em memória
# ---------------------------------------------------------------------------
alunos: list[dict] = []
contadores: dict[str, int] = {}  # curso -> último número de matrícula

CURSOS_VALIDOS = {"GES", "GEC"}

# ---------------------------------------------------------------------------
# Schemas (Pydantic)
# ---------------------------------------------------------------------------

class AlunoCreate(BaseModel):
    nome: str
    email: str
    curso: str

class AlunoUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    curso: Optional[str] = None

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _gerar_matricula(curso: str) -> tuple[int, str]:
    """Gera matrícula sequencial e ID únicos para o curso."""
    if curso not in contadores:
        contadores[curso] = 0
    contadores[curso] += 1
    matricula = contadores[curso]
    aluno_id = f"{curso}{matricula}"
    return matricula, aluno_id


def _buscar_aluno(aluno_id: str) -> dict | None:
    """Retorna o aluno com o ID informado ou None."""
    for aluno in alunos:
        if aluno["id"] == aluno_id.upper():
            return aluno
    return None

# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.post("/api/v1/alunos/", status_code=201)
def cadastrar_aluno(dados: AlunoCreate):
    """Cadastra um novo aluno."""
    curso = dados.curso.upper()
    if curso not in CURSOS_VALIDOS:
        raise HTTPException(
            status_code=400,
            detail=f"Curso inválido. Cursos válidos: {', '.join(sorted(CURSOS_VALIDOS))}",
        )

    matricula, aluno_id = _gerar_matricula(curso)

    aluno = {
        "id": aluno_id,
        "nome": dados.nome,
        "email": dados.email,
        "curso": curso,
        "matricula": matricula,
    }
    alunos.append(aluno)
    return aluno


@app.get("/api/v1/alunos/")
def listar_alunos():
    """Lista todos os alunos cadastrados."""
    return alunos


@app.get("/api/v1/alunos/{aluno_id}")
def buscar_aluno(aluno_id: str):
    """Busca um aluno pelo ID."""
    aluno = _buscar_aluno(aluno_id)
    if aluno is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return aluno


@app.patch("/api/v1/alunos/{aluno_id}")
def atualizar_aluno(aluno_id: str, dados: AlunoUpdate):
    """Atualiza dados de um aluno."""
    aluno = _buscar_aluno(aluno_id)
    if aluno is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    if dados.nome is not None:
        aluno["nome"] = dados.nome
    if dados.email is not None:
        aluno["email"] = dados.email
    if dados.curso is not None:
        novo_curso = dados.curso.upper()
        if novo_curso not in CURSOS_VALIDOS:
            raise HTTPException(
                status_code=400,
                detail=f"Curso inválido. Cursos válidos: {', '.join(sorted(CURSOS_VALIDOS))}",
            )
        if novo_curso != aluno["curso"]:
            matricula, novo_id = _gerar_matricula(novo_curso)
            aluno["curso"] = novo_curso
            aluno["matricula"] = matricula
            aluno["id"] = novo_id

    return aluno


@app.delete("/api/v1/alunos/{aluno_id}")
def remover_aluno(aluno_id: str):
    """Remove um aluno do sistema."""
    aluno = _buscar_aluno(aluno_id)
    if aluno is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    alunos.remove(aluno)
    return {"detail": f"Aluno {aluno_id.upper()} removido com sucesso"}


@app.delete("/api/v1/alunos/")
def resetar_alunos():
    """Reseta a lista de alunos (remove todos)."""
    alunos.clear()
    contadores.clear()
    return {"detail": "Todos os alunos foram removidos"}
