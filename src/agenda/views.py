from agenda.models import Agendamento
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .serializers import AgendamentoSerializer, AgendamentoPatchSerializer
from rest_framework.decorators import api_view


@api_view(["GET", "PATCH", "DELETE"])
def agendamento_detail(request, id):
    obj = get_object_or_404(Agendamento, id=id)
    if request.method == "GET":
        serializer = AgendamentoSerializer(obj)
        return JsonResponse(serializer.data)
    if request.method == "DELETE":
        obj.cancelado = True
        obj.save()
        return JsonResponse({"message": "Agendamento deletado com sucesso"}, status=204)
    if request.method == "PATCH":
        serializer = AgendamentoPatchSerializer(
            instance=obj, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=204)
        return JsonResponse(serializer.errors, status=400)


@api_view(["GET", "POST"])
def agendamento_list(request):
    if request.method == "GET":
        agendamentos = Agendamento.objects.filter(cancelado=False)
        serializer = AgendamentoSerializer(agendamentos, many=True)
        return JsonResponse(serializer.data, safe=False)
    if request.method == "POST":
        data = request.data

        serializer = AgendamentoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
