from datetime import datetime, timezone, date, timedelta
from .models import Agendamento
from typing import Iterable
from src.externals.api.brasil_api import feriados


def get_horarios_disponiveis(data: date) -> Iterable[datetime]:  # yyyy-mm-dd
    """
    Retorna uma lista com objetos do tipo datetime cujas datas são o mesmo dia passado (data)
    e os horários são os horários disponíveis para agendamento naquele dia.
    """
    if feriados.is_feriado(data):
        return set()
    start = datetime(
        year=data.year,
        month=data.month,
        day=data.day,
        hour=9,
        minute=0,
        tzinfo=timezone.utc,
    )
    end = datetime(
        year=data.year,
        month=data.month,
        day=data.day,
        hour=18,
        minute=0,
        tzinfo=timezone.utc,
    )
    delta = timedelta(minutes=30)
    horarios_disponiveis = set()
    while start < end:
        if not Agendamento.objects.filter(data_horario=start).exists():
            horarios_disponiveis.add(start)
        start += delta
    return horarios_disponiveis
