from rest_framework import serializers


class AgendamentoSerializer(serializers.Serializer):
    data_horario = serializers.DateTimeField()
    nome_cliente = serializers.CharField(max_length=255)
    email_cliente = serializers.EmailField()
    telefone_cliente = serializers.CharField(max_length=20)


class AgendamentoPatchSerializer(serializers.Serializer):
    data_horario = serializers.DateTimeField(required=False)
    nome_cliente = serializers.CharField(max_length=255, required=False)
    email_cliente = serializers.EmailField(required=False)
    telefone_cliente = serializers.CharField(max_length=20, required=False)
