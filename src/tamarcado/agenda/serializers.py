from rest_framework import serializers
from src.tamarcado.agenda.models import Agendamento
from django.utils import timezone
from django.contrib.auth.models import User
from .utils import get_horarios_disponiveis


class AgendamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agendamento
        fields = [
            "id",
            "data_horario",
            "nome_cliente",
            "email_cliente",
            "telefone_cliente",
            "cancelado",
            "prestador",
        ]

    prestador = serializers.CharField()

    def validate_prestador(self, value):
        try:
            prestador = User.objects.get(username=value)
        except User.DoesNotExist as e:
            raise serializers.ValidationError("Prestador não encontrado.") from e
        return prestador

    def validate_data_horario(self, value):
        horarios_disponiveis = get_horarios_disponiveis(value.date())
        if value < timezone.now():
            raise serializers.ValidationError(
                "Não é possível agendar para um horário no passado."
            )
        if value not in get_horarios_disponiveis(value.date()):
            raise serializers.ValidationError("Horário indisponível.")
        return value


class AgendamentoPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agendamento
        fields = [
            "id",
            "data_horario",
            "nome_cliente",
            "email_cliente",
            "telefone_cliente",
            "cancelado",
        ]

    def validate_data_horario(self, value):
        if value < timezone.now():
            raise serializers.ValidationError(
                "Não é possível agendar para um horário no passado."
            )
        
        if value not in get_horarios_disponiveis(value.date()):
            raise serializers.ValidationError("Horário indisponível.")
        return value

    def validate(self, attrs):
        telefone_cliente = attrs.get("telefone_cliente", "")
        email_cliente = attrs.get("email_cliente", "")
        if (
            email_cliente.endswith(".br")
            and telefone_cliente.startswith("+")
            and not telefone_cliente.startswith("+55")
        ):
            raise serializers.ValidationError(
                "Telefone deve começar com +55 e email deve terminar com .br"
            )
        else:
            return attrs


class PrestadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "agendamentos"]

    agendamentos = AgendamentoSerializer(many=True, read_only=True)
