from rest_framework import serializers
from .models import Agendamento


class AgendamentoSerializer(serializers.Serializer):
    data_horario = serializers.DateTimeField()
    nome_cliente = serializers.CharField(max_length=255)
    email_cliente = serializers.EmailField()
    telefone_cliente = serializers.CharField(max_length=20)

    def create(self, validated_data):
        return Agendamento.objects.create(**validated_data)


class AgendamentoPatchSerializer(serializers.Serializer):
    data_horario = serializers.DateTimeField(required=False)
    nome_cliente = serializers.CharField(max_length=255, required=False)
    email_cliente = serializers.EmailField(required=False)
    telefone_cliente = serializers.CharField(max_length=20, required=False)
    cancelado = serializers.BooleanField(required=False)

    def update(self, instance, validated_data):
        instance.data_horario = validated_data.get(
            "data_horario", instance.data_horario
        )
        instance.nome_cliente = validated_data.get(
            "nome_cliente", instance.nome_cliente
        )
        instance.email_cliente = validated_data.get(
            "email_cliente", instance.email_cliente
        )
        instance.telefone_cliente = validated_data.get(
            "telefone_cliente", instance.telefone_cliente
        )
        instance.save()
        return instance
