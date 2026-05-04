"""
Testes automatizados para a API de Gerenciador de Alunos.

Cobertura:
- Cadastro de pelo menos 3 alunos por curso (GES e GEC)
- Listagem de alunos
- Busca por ID
- Atualização de dados
- Remoção de alunos
- Reset da lista
- Verificação de que IDs deletados não são reutilizados
"""

import pytest
from fastapi.testclient import TestClient
from main import app, alunos, contadores


@pytest.fixture(autouse=True)
def _reset_state():
    """Limpa o estado antes de cada teste."""
    alunos.clear()
    contadores.clear()
    yield
    alunos.clear()
    contadores.clear()


client = TestClient(app)


# ============================================================================
# Helpers
# ============================================================================

def _cadastrar(nome: str, email: str, curso: str) -> dict:
    """Helper para cadastrar um aluno e retornar o JSON de resposta."""
    resp = client.post("/api/v1/alunos/", json={
        "nome": nome,
        "email": email,
        "curso": curso,
    })
    assert resp.status_code == 201
    return resp.json()


# ============================================================================
# 1. Cadastro de alunos (3+ por curso)
# ============================================================================

class TestCadastro:
    def test_cadastrar_3_alunos_ges(self):
        """Cadastrar pelo menos 3 alunos no curso GES."""
        a1 = _cadastrar("Ana Silva", "ana@email.com", "GES")
        a2 = _cadastrar("Bruno Costa", "bruno@email.com", "GES")
        a3 = _cadastrar("Carlos Lima", "carlos@email.com", "GES")

        assert a1["id"] == "GES1"
        assert a2["id"] == "GES2"
        assert a3["id"] == "GES3"

        assert a1["matricula"] == 1
        assert a2["matricula"] == 2
        assert a3["matricula"] == 3

    def test_cadastrar_3_alunos_gec(self):
        """Cadastrar pelo menos 3 alunos no curso GEC."""
        a1 = _cadastrar("Diana Souza", "diana@email.com", "GEC")
        a2 = _cadastrar("Eduardo Reis", "eduardo@email.com", "GEC")
        a3 = _cadastrar("Fernanda Lopes", "fernanda@email.com", "GEC")

        assert a1["id"] == "GEC1"
        assert a2["id"] == "GEC2"
        assert a3["id"] == "GEC3"

    def test_curso_invalido(self):
        """Deve rejeitar cursos que não são GES nem GEC."""
        resp = client.post("/api/v1/alunos/", json={
            "nome": "Teste",
            "email": "teste@email.com",
            "curso": "XYZ",
        })
        assert resp.status_code == 400

    def test_campos_obrigatorios(self):
        """Deve exigir nome, email e curso."""
        resp = client.post("/api/v1/alunos/", json={"nome": "Teste"})
        assert resp.status_code == 422


# ============================================================================
# 2. Listagem de alunos
# ============================================================================

class TestListagem:
    def test_listar_vazio(self):
        """Lista vazia quando não há alunos."""
        resp = client.get("/api/v1/alunos/")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_listar_todos(self):
        """Deve retornar todos os alunos cadastrados."""
        _cadastrar("Ana", "ana@email.com", "GES")
        _cadastrar("Bruno", "bruno@email.com", "GEC")
        _cadastrar("Carlos", "carlos@email.com", "GES")

        resp = client.get("/api/v1/alunos/")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 3


# ============================================================================
# 3. Busca por ID
# ============================================================================

class TestBuscaPorId:
    def test_buscar_existente(self):
        """Deve encontrar um aluno pelo ID."""
        _cadastrar("Ana Silva", "ana@email.com", "GES")

        resp = client.get("/api/v1/alunos/GES1")
        assert resp.status_code == 200
        data = resp.json()
        assert data["nome"] == "Ana Silva"
        assert data["id"] == "GES1"

    def test_buscar_inexistente(self):
        """Deve retornar 404 para ID que não existe."""
        resp = client.get("/api/v1/alunos/GES999")
        assert resp.status_code == 404

    def test_buscar_case_insensitive(self):
        """A busca por ID deve funcionar independente de maiúsculas/minúsculas."""
        _cadastrar("Ana", "ana@email.com", "GES")

        resp = client.get("/api/v1/alunos/ges1")
        assert resp.status_code == 200
        assert resp.json()["id"] == "GES1"


# ============================================================================
# 4. Atualização de dados
# ============================================================================

class TestAtualizacao:
    def test_atualizar_nome_email(self):
        """Deve atualizar nome e email do aluno."""
        _cadastrar("Ana", "ana@email.com", "GES")

        resp = client.patch("/api/v1/alunos/GES1", json={
            "nome": "Ana Maria",
            "email": "ana.maria@email.com",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["nome"] == "Ana Maria"
        assert data["email"] == "ana.maria@email.com"
        assert data["id"] == "GES1"  # ID não muda

    def test_atualizar_curso(self):
        """Ao trocar de curso, deve gerar novo ID e matrícula."""
        _cadastrar("Ana", "ana@email.com", "GES")

        resp = client.patch("/api/v1/alunos/GES1", json={"curso": "GEC"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["curso"] == "GEC"
        assert data["id"] == "GEC1"
        assert data["matricula"] == 1

    def test_atualizar_inexistente(self):
        """Deve retornar 404 ao atualizar aluno que não existe."""
        resp = client.patch("/api/v1/alunos/GES999", json={"nome": "Teste"})
        assert resp.status_code == 404


# ============================================================================
# 5. Remoção de alunos
# ============================================================================

class TestRemocao:
    def test_remover_aluno(self):
        """Deve remover um aluno e não encontrá-lo mais."""
        _cadastrar("Ana", "ana@email.com", "GES")

        resp = client.delete("/api/v1/alunos/GES1")
        assert resp.status_code == 200

        # Confirmar que não existe mais
        resp = client.get("/api/v1/alunos/GES1")
        assert resp.status_code == 404

    def test_remover_inexistente(self):
        """Deve retornar 404 ao remover aluno que não existe."""
        resp = client.delete("/api/v1/alunos/GES999")
        assert resp.status_code == 404

    def test_id_nao_reutilizado(self):
        """Ao deletar e criar novo, o ID não deve ser reutilizado."""
        _cadastrar("Ana", "ana@email.com", "GES")
        _cadastrar("Bruno", "bruno@email.com", "GES")

        # Deletar GES1
        client.delete("/api/v1/alunos/GES1")

        # Criar novo aluno GES — deve ser GES3, não GES1
        a3 = _cadastrar("Carlos", "carlos@email.com", "GES")
        assert a3["id"] == "GES3"
        assert a3["matricula"] == 3


# ============================================================================
# 6. Reset da lista
# ============================================================================

class TestReset:
    def test_resetar_lista(self):
        """Deve remover todos os alunos."""
        _cadastrar("Ana", "ana@email.com", "GES")
        _cadastrar("Bruno", "bruno@email.com", "GEC")
        _cadastrar("Carlos", "carlos@email.com", "GES")

        resp = client.delete("/api/v1/alunos/")
        assert resp.status_code == 200

        resp = client.get("/api/v1/alunos/")
        assert resp.json() == []


# ============================================================================
# 7. Teste integrado completo
# ============================================================================

class TestIntegrado:
    def test_fluxo_completo(self):
        """Fluxo completo: cadastrar, listar, buscar, atualizar, remover."""
        # Cadastrar 3 GES + 3 GEC
        for i in range(1, 4):
            _cadastrar(f"Aluno GES {i}", f"ges{i}@email.com", "GES")
            _cadastrar(f"Aluno GEC {i}", f"gec{i}@email.com", "GEC")

        # Listar — 6 alunos
        resp = client.get("/api/v1/alunos/")
        assert len(resp.json()) == 6

        # Buscar por ID
        resp = client.get("/api/v1/alunos/GES2")
        assert resp.json()["nome"] == "Aluno GES 2"

        # Atualizar
        resp = client.patch("/api/v1/alunos/GEC1", json={
            "nome": "Atualizado",
            "email": "novo@email.com",
        })
        assert resp.json()["nome"] == "Atualizado"

        # Remover
        resp = client.delete("/api/v1/alunos/GES3")
        assert resp.status_code == 200

        # Listar — 5 alunos
        resp = client.get("/api/v1/alunos/")
        assert len(resp.json()) == 5

        # ID não reutilizado — próximo GES deve ser GES4
        a = _cadastrar("Novo GES", "novo@email.com", "GES")
        assert a["id"] == "GES4"
