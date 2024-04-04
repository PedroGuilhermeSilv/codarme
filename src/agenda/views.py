from agenda.models import Agendamento
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .serializers import AgendamentoSerializer
from rest_framework.decorators import api_view


@api_view(["GET"])
def agendamento_detail(request, id):
    agendamento = get_object_or_404(Agendamento, pk=id)
    serializer = AgendamentoSerializer(agendamento)
    return JsonResponse(serializer.data)


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
            return JsonResponse( status=201)
        return JsonResponse(serializer.errors, status=400)
