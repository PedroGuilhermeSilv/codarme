
import csv
import io
from django.contrib.auth.models import User
from src.tamarcado.agenda.serializers import PrestadorSerializer
from src.tamarcado.celery import app
from django.core.mail import send_mail

@app.task()
def gerar_relatorio_prestadores():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Prestador", "Nome cliente", "Email Cliente", "Telefone Cliente", "Cancelado"])
    prestadores = User.objects.all()
    serializer = PrestadorSerializer(prestadores, many=True)
    for prestador in serializer.data:
        agendamentos = prestador["agendamentos"]
        for agendamento in agendamentos:
            writer.writerow(
                [
                    agendamento["prestador"],
                    agendamento["nome_cliente"],
                    agendamento["email_cliente"],
                    agendamento["telefone_cliente"],
                    agendamento["cancelado"],
                ]
            )
    send_mail(
        "Relatório de prestadores",
        "Relatório em anexo",
        "test@hotmail.com",
        ["t@hotmail.com"],)
    print(output.getvalue())