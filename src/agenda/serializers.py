from rest_framework import serializers
from .models import Agendamento
from django.utils import timezone


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
        ]
    # data_horario = serializers.DateTimeField()
    # nome_cliente = serializers.CharField(max_length=255)
    # email_cliente = serializers.EmailField()
    # telefone_cliente = serializers.CharField(max_length=20)

    # def create(self, validated_data):
    #     return Agendamento.objects.create(**validated_data)

    def validate_data_horario(self, value):
        if value < timezone.now():
            raise serializers.ValidationError(
                "Não é possível agendar para um horário no passado."
            )
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
    # data_horario = serializers.DateTimeField(required=False)
    # nome_cliente = serializers.CharField(max_length=255, required=False)
    # email_cliente = serializers.EmailField(required=False)
    # telefone_cliente = serializers.CharField(max_length=20, required=False)
    # cancelado = serializers.BooleanField(required=False)

    def validate_data_horario(self, value):
        if value < timezone.now():
            raise serializers.ValidationError(
                "Não é possível agendar para um horário no passado."
            )
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

    # def update(self, instance, validated_data):
    #     instance.data_horario = validated_data.get(
    #         "data_horario", instance.data_horario
    #     )
    #     instance.nome_cliente = validated_data.get(
    #         "nome_cliente", instance.nome_cliente
    #     )
    #     instance.email_cliente = validated_data.get(
    #         "email_cliente", instance.email_cliente
    #     )
    #     instance.telefone_cliente = validated_data.get(
    #         "telefone_cliente", instance.telefone_cliente
    #     )
    #     instance.save()
    #     return instance
