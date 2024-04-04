from agenda.models import Agendamento
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .serializers import AgendamentoSerializer

def agendamento_detail(request,id):
    agendamento = get_object_or_404(Agendamento, pk=id)
    serializer = AgendamentoSerializer(agendamento)
    return JsonResponse(serializer.data)

def agendamento_list(request):
    agendamentos = Agendamento.objects.all()
    serializer = AgendamentoSerializer(agendamentos, many=True)
    return JsonResponse(serializer.data, safe=False)
    
    