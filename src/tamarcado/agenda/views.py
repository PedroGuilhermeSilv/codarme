import csv

from src.tamarcado.agenda.tasks import gerar_relatorio_prestadores
from .models import Agendamento
from .serializers import AgendamentoSerializer, PrestadorSerializer
from rest_framework import permissions
from django.contrib.auth.models import User
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
)
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import (
    api_view,
    permission_classes as permission_classes_decorator,
)
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from datetime import date, datetime
from .utils import get_horarios_disponiveis


class IsOwnerOrCreateOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        username = request.query_params.get("username", None)
        return request.user.username == username


class IsPrestador(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.prestador


class AgendamentoDetail(RetrieveUpdateDestroyAPIView):  # api/agendamentos/<int:pk>
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer
    permission_classes = [IsPrestador]

    def perform_destroy(self, instance):
        instance.cancelado = True
        instance.save()


class AgendamentoList(ListCreateAPIView):  # api/agendamentos/?username=<username>
    serializer_class = AgendamentoSerializer
    permission_classes = [IsOwnerOrCreateOnly]

    def get_queryset(self):
        username = self.request.query_params.get("username", None)
        return Agendamento.objects.filter(prestador__username=username)


# class PrestadorList(ListAPIView):
#     serializer_class = PrestadorSerializer
#     queryset = User.objects.all()
#     permission_classes = [IsAdminUser]


@api_view(http_method_names=["GET"])
@permission_classes_decorator([IsAdminUser])
def get_prestadores(request):
    formato = request.query_params.get("formato")
    prestadores = User.objects.all()
    serializer = PrestadorSerializer(prestadores, many=True)

    if formato != "csv":
        return Response(serializer.data)
    # response = HttpResponse(
    #     content_type="text/csv",
    #     headers={"Content-Disposition": f'attachment; filename="relatorio{date.today()}.csv"'},
    # )
    # writer = csv.writer(response)
    # for prestador in serializer.data:
    #     agendamentos = prestador["agendamentos"]
    #     for agendamento in agendamentos:
    #         writer.writerow(
    #             [
    #                 agendamento["prestador"],
    #                 agendamento["nome_cliente"],
    #                 agendamento["email_cliente"],
    #                 agendamento["telefone_cliente"],
    #                 agendamento["cancelado"],
    #             ]
    #         )
    result = gerar_relatorio_prestadores.delay()
    return Response({"task_id": result.task_id})


@api_view(http_method_names=["GET"])
def get_horarios(request):
    data = request.query_params.get("data")
    data = datetime.fromisoformat(data).date() if data else datetime.now().date()

    horarios_disponiveis = sorted(list(get_horarios_disponiveis(data)))
    return JsonResponse(horarios_disponiveis, safe=False)
