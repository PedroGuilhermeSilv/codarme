import datetime
from rest_framework.test import APIClient
from agenda.models import Agendamento
import pytest


@pytest.fixture
def agendamento() -> Agendamento:
    return Agendamento.objects.create(
        data_horario="2021-10-10T10:00:00Z",
        nome_cliente="Fulano",
        email_cliente="pedro@hotmail.com",
        telefone_cliente="11999999999",
    )


@pytest.mark.django_db
class TestsListAgendamentos:
    def test_list_agendamentos(self):
        client = APIClient()
        response = client.get("/api/agendamentos/")
        assert response.status_code == 200
        data = response.json()
        assert data == []

    def test_listagem_de_agendamentos_criados(self, agendamento):
        client = APIClient()
        response = client.get("/api/agendamentos/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == agendamento.id


@pytest.mark.django_db
class TestCreateAgendamento:
    def test_create_agendamento(self):
        client = APIClient()
        data = {
            "data_horario": "2027-10-10T10:00:00Z",
            "nome_cliente": "Fulano",
            "email_cliente": "test@hotmail.com",
            "telefone_cliente": "11999999999",
        }
        response = client.post("/api/agendamentos/", data=data, format="json")
        assert response.status_code == 201
        assert Agendamento.objects.count() == 1
        agendamento = Agendamento.objects.first()
        assert agendamento.nome_cliente == "Fulano"
        assert agendamento.telefone_cliente == "11999999999"
        assert agendamento.data_horario == datetime.datetime(
            2027, 10, 10, 10, 0, tzinfo=datetime.timezone.utc
        )

    def test_create_agendamento__com_data_invalida(self):
        client = APIClient()
        data = {
            "data_horario": "2021-10-10T10:00:00Z",
            "nome_cliente": "Fulano",
            "email_cliente": "test@hotmail.com",
            "telefone_cliente": "11999999999",
        }
        response = client.post("/api/agendamentos/", data=data, format="json")
        assert response.status_code == 400
        assert Agendamento.objects.count() == 0


@pytest.mark.django_db
class TestAgendamentoDetail:
    def test_agendamento_detail(self, agendamento):
        client = APIClient()
        response = client.get(f"/api/agendamentos/{agendamento.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == agendamento.id
        assert data["nome_cliente"] == agendamento.nome_cliente
        assert data["email_cliente"] == agendamento.email_cliente
        assert data["telefone_cliente"] == agendamento.telefone_cliente

    def test_agendamento_detail__agendamento_nao_existe(self):
        client = APIClient()
        response = client.get("/api/agendamentos/1")
        assert response.status_code == 404

    def test_agendamento_detail__delete(self, agendamento):
        client = APIClient()
        response = client.delete(f"/api/agendamentos/{agendamento.id}")
        assert response.status_code == 204
        agendamento.refresh_from_db()
        assert agendamento.cancelado is True

    def test_agendamento_detail__patch(self, agendamento):
        client = APIClient()
        data = {"nome_cliente": "Ciclano"}
        response = client.patch(f"/api/agendamentos/{agendamento.id}", data=data)
        assert response.status_code == 204
        agendamento.refresh_from_db()
        assert agendamento.nome_cliente == "Ciclano"
