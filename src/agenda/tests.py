import datetime
import unittest.mock
from rest_framework.test import APIClient
from agenda.models import Agendamento
import pytest
from django.contrib.auth.models import User


@pytest.fixture
def prestador() -> User:
    return User.objects.create_user(
        username="prestador", email="prestador@gmail.com", password="password"
    )


def is_feriado_simulado(data):
    return True


@pytest.fixture
def agendamento(prestador) -> Agendamento:
    return Agendamento.objects.create(
        prestador=prestador,
        data_horario="2021-10-10T10:00:00Z",
        nome_cliente="Fulano",
        email_cliente="pedro@hotmail.com",
        telefone_cliente="11999999999",
    )


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.mark.django_db
class TestsListAgendamentos:
    def test_list_agendamentos(self, api_client, agendamento):
        api_client.login(username="prestador", password="password")
        response = api_client.get("/api/agendamentos/?username=prestador")
        assert response.status_code == 200
        data = response.json()
        assert data == [
            {
                "id": agendamento.id,
                "data_horario": agendamento.data_horario,
                "nome_cliente": agendamento.nome_cliente,
                "email_cliente": agendamento.email_cliente,
                "telefone_cliente": agendamento.telefone_cliente,
                "cancelado": agendamento.cancelado,
                "prestador": agendamento.prestador.username,
            }
        ]


@pytest.mark.django_db
class TestCreateAgendamento:
    def test_create_agendamento(self, api_client, prestador):
        data = {
            "prestador": prestador.username,
            "data_horario": "2027-10-10T10:00:00Z",
            "nome_cliente": "Fulano",
            "email_cliente": "test@hotmail.com",
            "telefone_cliente": "11999999999",
        }
        response = api_client.post("/api/agendamentos/", data=data, format="json")
        assert response.status_code == 201
        assert Agendamento.objects.count() == 1
        agendamento = Agendamento.objects.first()
        assert agendamento.nome_cliente == "Fulano"
        assert agendamento.telefone_cliente == "11999999999"
        assert agendamento.data_horario == datetime.datetime(
            2027, 10, 10, 10, 0, tzinfo=datetime.timezone.utc
        )

    def test_create_agendamento__com_data_invalida(self, api_client):
        data = {
            "data_horario": "2021-10-10T10:00:00Z",
            "nome_cliente": "Fulano",
            "email_cliente": "test@hotmail.com",
            "telefone_cliente": "11999999999",
        }
        response = api_client.post("/api/agendamentos/", data=data, format="json")
        assert response.status_code == 400
        assert Agendamento.objects.count() == 0


@pytest.mark.django_db
class TestAgendamentoDetail:
    def test_agendamento_detail(self, agendamento, prestador):
        client = APIClient()
        client.login(username=agendamento.prestador.username, password="password")
        response = client.get(f"/api/agendamentos/{agendamento.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == agendamento.id
        assert data["nome_cliente"] == agendamento.nome_cliente
        assert data["email_cliente"] == agendamento.email_cliente
        assert data["telefone_cliente"] == agendamento.telefone_cliente

    def test_agendamento_detail__agendamento_nao_existe(self, api_client, agendamento):
        api_client.login(username="prestador", password="password")

        response = api_client.delete(f"/api/agendamentos/{agendamento.id}")
        assert response.status_code == 204
        agendamento = Agendamento.objects.get(id=agendamento.id)
        assert agendamento.cancelado is True

    def test_agendamento_detail__patch(self, agendamento):
        client = APIClient()
        client.login(username=agendamento.prestador.username, password="password")
        data = {"nome_cliente": "Ciclano"}
        response = client.patch(f"/api/agendamentos/{agendamento.id}", data=data)
        assert response.status_code == 200
        agendamento.refresh_from_db()
        assert agendamento.nome_cliente == "Ciclano"


@pytest.mark.django_db
class TestGetHorarios:
    def test_when_date_is_holiday(self, api_client, monkeypatch):
        monkeypatch.setattr("agenda.utils.feriados.is_feriado", is_feriado_simulado)
        response = api_client.get("/api/horarios/?data=2025-12-25")
        assert response.status_code == 200
        assert response.json() == []

    def test_when_date_return_list_of_available_times(self, api_client):
        response = api_client.get("/api/horarios/?data=2025-12-24")
        assert response.status_code == 200
        assert response.json()[0] == "2025-12-24T09:00:00Z"
        assert response.json()[-1] == "2025-12-24T17:30:00Z"
