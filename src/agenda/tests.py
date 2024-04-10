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
