
import csv
import io
from django.contrib.auth.models import User
from src.tamarcado.agenda.serializers import PrestadorSerializer
from src.tamarcado.celery import app
from django.core.mail import EmailMessage

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
    email = EmailMessage(
        "Relatório de prestadores",
        "Relatório em anexo",
        "test@homtmail.com",
        ["t@hotmail.com"],
    )
    email.attach("relatorio.csv", output.getvalue(), "text/csv")
    email.send()
