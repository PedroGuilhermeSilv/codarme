from agenda.models import Agendamento
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .serializers import AgendamentoSerializer, AgendamentoPatchSerializer
from rest_framework.decorators import api_view


@api_view(["GET", "PATCH"])
def agendamento_detail(request, id):
    if request.method == "GET":
        agendamento = get_object_or_404(Agendamento, id=id)
        serializer = AgendamentoSerializer(agendamento)
        return JsonResponse(serializer.data)
    if request.method == "PATCH":
        obj = get_object_or_404(Agendamento, id=id)
        serializer = AgendamentoPatchSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            v_data = serializer.validated_data
            obj.data_horario = v_data.get("data_horario", obj.data_horario)
            obj.nome_cliente = v_data.get("nome_cliente", obj.nome_cliente)
            obj.email_cliente = v_data.get("email_cliente", obj.email_cliente)
            obj.telefone_cliente = v_data.get("telefone_cliente", obj.telefone_cliente)
            obj.save()
            return JsonResponse(serializer.data, status=204)
        return JsonResponse(serializer.errors, status=400)


@api_view(["GET", "POST"])
def agendamento_list(request):
    if request.method == "GET":
        agendamentos = Agendamento.objects.all()
        serializer = AgendamentoSerializer(agendamentos, many=True)
        return JsonResponse(serializer.data, safe=False)
    if request.method == "POST":
        data = request.data

        serializer = AgendamentoSerializer(data=data)
        if serializer.is_valid():
            valide_data = serializer.validated_data
            Agendamento.objects.create(**valide_data)
            return JsonResponse(valide_data, status=201)
        return JsonResponse(serializer.errors, status=400)
