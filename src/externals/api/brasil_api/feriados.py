from datetime import date
import requests
from django.conf import settings
import logging


def is_feriado(date: date) -> bool:
    """
    Está funcão irá receber uma data e retornar se é feriado ou não. Com base na API Brasil API.
    """
    logging.info("Executando consulta na API Brasil")
    if settings.TESTING:
        return date.day == 25 and date.month == 12

    
    ano = date.year
    r = requests.get(f"https://brasilapi.com.br/api/feriados/v1/{ano}")
    feriados = r.json()
    if r.status_code != 200:
        logging.error("Error na consulta da api brasil")
        return True
    for feriado in feriados:
        data_feriado_str = feriado["date"]
        data_feriado = date.fromisoformat(data_feriado_str)
        if date == data_feriado:
            return True
    return False
